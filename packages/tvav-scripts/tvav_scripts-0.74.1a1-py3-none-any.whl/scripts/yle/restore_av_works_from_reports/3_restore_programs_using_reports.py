"""
Code a script that restores DB programs using Reports 1-3 as input
  - report 1 (overwrite happened after last report)
    --> restore from reports
    compare YLE XML Cuesheet against PROD Cuesheet cue by cue
    - if comparison is different --> update PROD to match reported version
    - if cue is missing in PROD --> create new Cue from parsing reported version
    - if cue is missing in XML --> remove cue in PROD

  - report 2 (overwrite happened before 1 report)
    --> restore from backup
  - report 3 (overwrite happened in between reports)
    --> ignore
"""
import csv
import openpyxl
import pytz
from bson import ObjectId
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import parse
from dotenv import load_dotenv
from typing import Any, Iterable, Iterator, Optional, Union
from pathlib import Path
from pymongo import InsertOne, MongoClient, UpdateMany, UpdateOne
from pymongo.database import Database
from tqdm import tqdm

from scripts.utils.decorators import ntfy
from scripts.yle.restore_av_works_from_reports.config import Config
from scripts.yle.restore_av_works_from_reports.queries import REPORTS
from scripts.yle.restore_av_works_from_reports.single_view_client import SingleViewAPIClient
from scripts.yle.restore_av_works_from_reports.xml_like_orm import ReportFile


DEFAULT_DECISION = "Program did not fall in any of the previous scenarios. WEIRD. Will not update in Reportal."
MATCH_IMPORT_HISTORY_START_DATE = datetime(2022, 12, 5)


@dataclass(frozen=True)
class ProgramInfo:
    yle_numerical_id: str
    decision: str
    av_work_operation: Optional[UpdateOne]
    music_work_operations: Optional[list[Union[UpdateMany, InsertOne]]]


@dataclass(frozen=True)
class RestoreInfo:
    av_work_operation: UpdateOne
    music_work_operations: list[Union[UpdateMany, InsertOne]]


def safe_datetime(v: Union[str, datetime]) -> datetime:
    if isinstance(v, str):
        return parse(v)
    return v


def write_report(report_file: Path, rows: Iterable, headers: Optional[Iterable] = None):
    with report_file.open("wt") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in rows:
            if isinstance(row, str):
                row = [row]
            writer.writerow(row)


def link_prod_music_work_by_work_id(
    music_work_dict: dict[str, Any],
    work_id: str,
    prod_db: Database
) -> Optional[str]:
    """Tries to find a MusicWork in PROD DB using a work_id.
    Returns None if could not find it, or the MusicWork _id if it could.
    """

    work_id_value = music_work_dict.get("work_ids", {}).get(work_id)

    if not work_id_value:
        # we cannot find the prod music_work using this work_id
        return None

    if (
        prod_mw := prod_db.music_work.find_one(
            {f"work_ids.{work_id}": work_id_value},
            {"_id": 1}
        )
    ):
        return prod_mw["_id"]

    return None


def get_restore_info(
    yle_numerical_id: str,
    prod_db: Database,
    backup_db: Database,
    sv_client: SingleViewAPIClient,
    config: Config,
    report_filename: Optional[str] = None,
    restore_from_backup: bool = False,
) -> Optional[RestoreInfo]:
    """Returns the list of cues to use when replacing PROD cues.

    1. Find the MusicWork using the ids
    2. For every cue try to link to the best match for music_work using (in prio descending order)
      - music_work_id
      - single_view_id (only for backup)
      - isrc
      - custom_id
    3. If we found the music_work, we link it. UPDATE MUSIC WORK EXTRAS WITH A TAG SO WE CAN RE-ENRICH AFTERWARDS
    4. If we did not find the music_work, create a new MusicWork:
      - from BACKUP copy paste MUSIC WORK + TAG
      - from XML create incomplete MusicWork with single_view_id and ISRC. How to find the single_view_id?
        - By ISRC (isrc specific endpoint)
        - By CustomID (specific code endpoint)
        - By title+performer (do not use composer, because that would give a work) (/sound-recordings endpoint)
        - PARSE XML + TAG WITH SPECIAL TAG + REPORT AS EDGE CASE

    SV API DOCS: http://sv-api.data.bmat.com/docs#

    # Extra considerations
    - Only latin characters TRUE always
    - Pause the aggregations and enable before we re-enrich
    - Do not re-enrich cue level
    - Watch out for relative start_times. If the relative start_time (HHMM) matches previous relative end_time, add the seconds from the previous cue, otherwise start at second 0
    - cue uses: there can be 7 combinations --> truth table with is_jingle, b_v, tunnari
    """

    if config.third_script_dry_run:
        return None

    # this list might contain UpdateMany (just tagging with YLE_2180)
    # or InsertOne operations (when creating new MusicWorks)
    music_work_operations: list[Union[UpdateMany, InsertOne]] = []

    # Find identifiers for the program we want to restore
    prod_av_work = prod_db.av_work.find_one({"work_ids.yle_numerical_id": yle_numerical_id})
    # we should find it, because the yle_numerical_id comes from PROD, but this is just to double check
    assert prod_av_work is not None, f"Could not find {yle_numerical_id=} in PROD DB"

    prod_av_work_id = prod_av_work["_id"]

    cues_to_use: list[dict[str, Any]] = []
    if restore_from_backup:
        backup_aw = backup_db.av_work.find_one({"work_ids.yle_numerical_id": yle_numerical_id}, {"cues": "$cuesheet.cues"})
        assert backup_aw is not None, f"Could not find AvWork {yle_numerical_id=} in BACKUP DB"
        cues_to_use = backup_aw["cues"]
    else:
        assert report_filename is not None
        # we need to find the cues in the report file and get the reportal-model version of those
        plasma_id = prod_av_work["work_ids"].get("plasma_id")
        report_file = ReportFile(config.xml_reports_dir / report_filename)
        
        for program in report_file.programs:
            if program.is_filler:
                continue

            if program.yle_numerical_id == yle_numerical_id:
                break
            
            if plasma_id and program.plasma_id == plasma_id:
                break
        else:
            program = None

        assert program is not None, (
            f"Could not find the program ({yle_numerical_id=}, {plasma_id=}) in {report_filename=}"
        )
        cues_to_use = [cue.as_reportal() for cue in program.cues]

    ###

    # Build the fixed cues list
    fixed_cues_list: list[dict[str, Any]] = []
    music_works_to_tag: list[ObjectId] = []

    def link_mw_to_cue(fixed_cue_dict: dict, linked_mw_id: Union[str, ObjectId]):
        if isinstance(linked_mw_id, str):
            linked_mw_id = ObjectId(linked_mw_id)

        fixed_cue_dict["music_work"] = linked_mw_id
        fixed_cues_list.append(fixed_cue_dict)
        music_works_to_tag.append(linked_mw_id)

    for cue in cues_to_use:
        # re-use all cue info for the new cue
        fixed_cue = cue.copy()

        if restore_from_backup and "music_work" not in fixed_cue:
            fixed_cues_list.append(fixed_cue)
            continue

        # we need to better link this MusicWork, so we remove it from the fixed cue
        del fixed_cue["music_work"]

        # 1 - Link already existing MusicWork by searching by its trusted ids in prio desc order
        # music_work_id
        mw_id = cue["music_work"]
        if not restore_from_backup:
            # reported has music_work level info
            mw_id = mw_id["_id"]

        if prod_db.music_work.count_documents({"_id": mw_id}) == 1:
            # we found the same mw_id, no need to keep searching!
            link_mw_to_cue(fixed_cue, mw_id)
            continue

        backup_mw: Optional[dict[str, Any]] = None
        if restore_from_backup:
            # single_view_id (just for backup)
            backup_mw = backup_db.music_work.find_one({"_id": mw_id})
            assert backup_mw is not None, f"Could not find MusicWork:{mw_id} in backup db"
            music_work_dict = backup_mw
        else:
            # from reported cue
            music_work_dict = cue["music_work"]

        for work_id in [
            "single_view_id",
            "isrc",
            "custom_id"
        ]:
            if (
                mw_id := link_prod_music_work_by_work_id(music_work_dict, work_id, prod_db)
            ):
                # we found a MusicWork in PROD DB
                break
        else:
            # we did not find the PROD MusicWork using ids
            mw_id = None

        if mw_id:
            link_mw_to_cue(fixed_cue, mw_id)
            continue

        # 2 - We need to create a new MusicWork
        if restore_from_backup:
            # from backup it is a direct copy+paste
            assert backup_mw is not None

            # tag
            backup_extras = backup_mw.get("extras", {})
            backup_extras["YLE_2180"] = datetime.now(pytz.UTC)
            backup_mw["extras"] = backup_extras

            music_work_operations.append(InsertOne(backup_mw))

            link_mw_to_cue(fixed_cue, backup_mw["_id"])
            continue

        # from reported info --> we create an impartial MusicWork with single_view_id + ISRC
        # so the re-enrichment can later on fill the metadata from SV API
        # we need to try to find the SOUND RECORDING ID using SV API

        # By ISRC
        if (
            (
                isrc := cue["music_work"].get("work_ids", {}).get("isrc")
            ) and (
                sound_recording := sv_client.get_sound_recording_by_isrc(isrc)
            )
        ):
            mw_id = ObjectId()
            music_work_operations.append(InsertOne({
                "_id": mw_id,
                "work_ids": {
                    "single_view_id": sound_recording["_id"],
                    "isrc": isrc,
                },
                "extras": {"YLE_2180": datetime.now(pytz.UTC)}
            }))
            link_mw_to_cue(fixed_cue, mw_id)
            continue

        # By CustomID
        if (
            (
                custom_id := cue["music_work"].get("work_ids", {}).get("custom_id")
            ) and (
                sound_recordings := sv_client.get_sound_recordings_by_internal_code(
                    custom_id,
                    "CustomID",
                    "crawler_yle"
                )
            )
        ):
            if len(sound_recordings) == 1:
                # if it is just one, go for it, this is the best match we got
                single_view_id = sound_recordings[0]["_id"]

                mw_id = ObjectId()
                music_work_operations.append(InsertOne({
                    "_id": mw_id,
                    "work_ids": {
                        "single_view_id": single_view_id,
                        "custom_id": custom_id,
                    },
                    "extras": {"YLE_2180": datetime.now(pytz.UTC)}
                }))
                link_mw_to_cue(fixed_cue, mw_id)
                continue

        # By title + performer
        mw_title = cue["music_work"]["title"]
        mw_interpreter = next(
            (
                f"{cont.get('first_name', '')} {cont.get('last_name', '')}".strip()
                for cont in cue["music_work"].get("contributors", [])
                if cont["role"] == "interpreter"
            ),
            None
        )

        if mw_title and mw_interpreter and (
            sound_recordings := sv_client.get_sound_recordings_by_q(f"{mw_title} {mw_interpreter}")
        ):
            if len(sound_recordings) == 1:
                # if it is just one, go for it, this is the best match we got
                single_view_id = sound_recordings[0]["_id"]

                mw_id = ObjectId()
                music_work_operations.append(InsertOne({
                    "_id": mw_id,
                    "work_ids": {
                        "single_view_id": single_view_id,
                    },
                    "extras": {"YLE_2180": datetime.now(pytz.UTC)}
                }))
                link_mw_to_cue(fixed_cue, mw_id)
                continue

        # 3 - We could not find the sound_recording in SV --> use parsed information
        music_work_operations.append(InsertOne(cue["music_work"]))
        link_mw_to_cue(fixed_cue, cue["music_work"]["_id"])

    # tag already existing MusicWorks with extras.YLE_2180
    music_work_operations.append(UpdateMany(
            filter={"_id": {"$in": music_works_to_tag}},
            update={"$set": {"extras.YLE_2180": datetime.now(pytz.UTC)}},
        )
    )
    
    return RestoreInfo(
        av_work_operation=UpdateOne(
            filter={"_id": prod_av_work_id},
            update={"$set": {
                "cuesheet.cues": fixed_cues_list,
                "extras.YLE_2180": datetime.now(pytz.UTC),
            }},
        ),
        music_work_operations=music_work_operations
    )


def restore_using_report_1(
    headers: tuple,
    rows: Iterator[tuple],
    prod_db: Database,
    backup_db: Database,
    single_view_client: SingleViewAPIClient,
    config: Config,
) -> list[ProgramInfo]:
    """
    This report contains a comparison between
    - last reported version
    - production

    So we should find just 1 comparison per yle_numerical_id.
    """

    program_info_list: list[ProgramInfo] = []
    programs_already_checked = set()

    max_date_report_date_yes_populated_needs_review = set()
    max_date_report_date_yes_populated_needs_review_file = (
        config.third_script_reports_dir / "1st_list_max_date_report_date_yes_populated_needs_review.csv"
    )

    max_date_last_populated_at_with_edit_after_report_date = set()
    max_date_last_populated_at_with_edit_after_report_date_file = (
        config.third_script_reports_dir / "1st_list_max_date_last_populated_at_with_edit_after_report_date.csv"
    )
    
    for row in tqdm(rows, unit="row", leave=False):
        row = dict(zip(headers, row))

        decision = "LIST 1. " + DEFAULT_DECISION
        restore_info: Optional[RestoreInfo] = None

        if not (
            yle_numerical_id := row["yle_numerical_id"]
        ) or yle_numerical_id in programs_already_checked:
            # this report has 1 comparison per program,
            # so this is just another cue in the same program
            continue

        programs_already_checked.add(yle_numerical_id)

        last_report_date = safe_datetime(row["last_reported_date"])

        last_edited_at = (
            safe_datetime(row["production_last_edited_at"])
            if row["production_last_edited_at"]
            else None
        )
        last_populated_at = (
            safe_datetime(row["production_last_populated_at"])
            if row["production_last_populated_at"]
            else None
        )

        max_date = max(
            last_report_date,
            last_edited_at or datetime.min,
            last_populated_at or datetime.min,
        )

        if last_populated_at:
            if max_date == last_report_date:
                max_date_report_date_yes_populated_needs_review.add(yle_numerical_id)
                decision = (
                    "LIST 1. Populated but report date happened last. "
                    f"WILL IGNORE. CHECK --> {max_date_report_date_yes_populated_needs_review_file.name}"
                )
            elif max_date == last_edited_at:
                decision = "LIST 1. Populated but user edition happened last. KEEP REPORTAL VERSION"
            elif max_date == last_populated_at:
                if (
                    not last_edited_at or
                    last_edited_at and last_edited_at < last_report_date
                ):
                    decision = (
                        "LIST 1. Populate action happened last AND last user edit happened before report_date or is missing. "
                        "REVERT TO LAST REPORTED VERSION"
                    )
                    restore_info = get_restore_info(
                        yle_numerical_id=yle_numerical_id,
                        prod_db=prod_db,
                        backup_db=backup_db,
                        sv_client=single_view_client,
                        config=config,
                        report_filename=row["last_reported_filename"],
                    )
                else:
                    max_date_last_populated_at_with_edit_after_report_date.add(yle_numerical_id)
                    decision = (
                        "LIST 1. Populate action happened last AND last user edit happened after report_date. "
                        f"WILL IGNORE. CHECK --> {max_date_last_populated_at_with_edit_after_report_date_file.name}"
                    )
        else:
            if max_date == last_report_date:
                decision = "LIST 1. NO populate action AND CMO report happened last. REVERT TO LAST REPORTED VERSION"
                restore_info = get_restore_info(
                    yle_numerical_id=yle_numerical_id,
                    prod_db=prod_db,
                    backup_db=backup_db,
                    sv_client=single_view_client,
                    config=config,
                    report_filename=row["last_reported_filename"],
                )
            elif max_date == last_edited_at:
                assert last_edited_at is not None, "Should not be None inside this if"

                if last_edited_at <= MATCH_IMPORT_HISTORY_START_DATE:
                    decision = (
                        "LIST 1. NO populate action AND last user edit happened last BEFORE MATCH_IMPORT_HISTORY_START_DATE. "
                        "REVERT TO LAST REPORTED VERSION"
                    )
                    restore_info = get_restore_info(
                        yle_numerical_id=yle_numerical_id,
                        prod_db=prod_db,
                        backup_db=backup_db,
                        sv_client=single_view_client,
                        config=config,
                        report_filename=row["last_reported_filename"],
                    )
                else:
                    decision = (
                        "LIST 1. NO populate action AND last user edit happened last AFTER MATCH_IMPORT_HISTORY_START_DATE. "
                        "KEEP REPORTAL VERSION"
                    )

        program_info_list.append(ProgramInfo(
            yle_numerical_id=yle_numerical_id,
            decision=decision,
            av_work_operation=(
                restore_info.av_work_operation
                if restore_info
                else None
            ),
            music_work_operations=(
                restore_info.music_work_operations
                if restore_info
                else None
            )
        ))

    write_report(
        report_file=max_date_report_date_yes_populated_needs_review_file,
        rows=max_date_report_date_yes_populated_needs_review
    )
    write_report(
        report_file=max_date_last_populated_at_with_edit_after_report_date_file,
        rows=max_date_last_populated_at_with_edit_after_report_date
    )

    return program_info_list


def restore_using_report_2(
    headers: tuple,
    rows: Iterator[tuple],
    prod_db: Database,
    backup_db: Database,
    single_view_client: SingleViewAPIClient,
    config: Config,
) -> list[ProgramInfo]:
    """
    This report contains a comparison between
    - first reported version after backup date
    - backup version

    So we should find just 1 comparison per yle_numerical_id.
    """

    BACKUP_DATE = datetime(2023, 8, 31)

    program_info_list: list[ProgramInfo] = []
    programs_already_checked = set()

    # programs where the BACKUP_DATE is the most recent date need to be reviewed manually
    programs_backup_date_max_to_be_reviewed = set()
    programs_backup_date_max_to_be_reviewed_file = (
        config.third_script_reports_dir / "2nd_list_programs_backup_date_max_to_be_reviewed.csv"
    )

    for row in tqdm(rows, unit="rows", leave=False):
        row = dict(zip(headers, row))
        
        decision = "LIST 2. " + DEFAULT_DECISION
        restore_info: Optional[RestoreInfo] = None

        if not (
            yle_numerical_id := row["yle_numerical_id"]
        ) or yle_numerical_id in programs_already_checked:
            # this report has 1 comparison per program,
            # so this is just another cue in the same program
            continue

        programs_already_checked.add(yle_numerical_id)

        report_date = safe_datetime(row["first_reported_date"])
        last_edited_at = (
            safe_datetime(row["production_last_edited_at"])
            if row["production_last_edited_at"]
            else None
        )
        last_populated_at = (
            safe_datetime(row["production_last_populated_at"])
            if row["production_last_populated_at"]
            else None
        )

        max_date = max(
            BACKUP_DATE,
            last_edited_at or datetime.min, # Jan 1st 1 AD
            last_populated_at or datetime.min
        )

        if max_date == BACKUP_DATE:
            programs_backup_date_max_to_be_reviewed.add(yle_numerical_id)
            decision = (
                "LIST 2. Max date is backup_date. WILL IGNORE. "
                f"CHECK --> {programs_backup_date_max_to_be_reviewed_file.name}"
            )
        elif max_date == last_edited_at:
            decision = "LIST 2. Max date is last_edited_at. KEEP REPORTAL VERSION"
        elif max_date == last_populated_at:
            assert last_populated_at is not None, "last_populated_at should not be None inside this if"

            if last_populated_at < report_date:
                decision = (
                    "LIST 2. Max date is last_populated_at AND happened BEFORE report date. "
                    "REVERT TO BACKUP VERSION"
                )
                restore_info = get_restore_info(
                    yle_numerical_id=yle_numerical_id,
                    prod_db=prod_db,
                    backup_db=backup_db,
                    sv_client=single_view_client,
                    config=config,
                    restore_from_backup=True
                )
            else:
                decision = (
                    "LIST 2. Max date is last_populated_at AND happened AFTER report date. "
                    "KEEP REPORTAL VERSION"
                )

        program_info_list.append(ProgramInfo(
            yle_numerical_id=yle_numerical_id,
            decision=decision,
            av_work_operation=(
                restore_info.av_work_operation
                if restore_info
                else None
            ),
            music_work_operations=(
                restore_info.music_work_operations
                if restore_info
                else None
            )
        ))

    # dump programs where the backup_date is the most recent
    write_report(
        programs_backup_date_max_to_be_reviewed_file,
        programs_backup_date_max_to_be_reviewed
    )

    return program_info_list


def restore_using_report_3(
    headers: tuple,
    rows: Iterator[tuple],
    prod_db: Database,
    backup_db: Database,
    single_view_client: SingleViewAPIClient,
    config: Config,
) -> list[ProgramInfo]:
    """
    This report contains a comparison between
    - first reported version
    - every other reported version

    So it is expected to find MULTIPLE comparisons for
    every yle_numerical_id.
    
    This requires caching all comparisons for the same first reported version
    and then 
    """

    program_info_list: list[ProgramInfo] = []
    programs_already_checked = set()

    populated_with_first_reported_last = set()
    populated_with_first_reported_last_file = (
        config.third_script_reports_dir / "3rd_list_populated_with_first_reported_last.csv"
    )

    populated_after_user_edited_after_first_report = set()
    populated_after_user_edited_after_first_report_file = (
        config.third_script_reports_dir / "3rd_list_populated_after_user_edited_after_first_report.csv"
    )

    for row in tqdm(rows, unit="rows", leave=False):
        row = dict(zip(headers, row))

        decision = "LIST 3. " + DEFAULT_DECISION
        restore_info: Optional[RestoreInfo] = None

        if not (
            yle_numerical_id := row["yle_numerical_id"]
        ) or yle_numerical_id in programs_already_checked:
            continue

        programs_already_checked.add(yle_numerical_id)

        first_reported_date = safe_datetime(row["first_reported_date"])
        last_edited_at = (
            safe_datetime(row["production_last_edited_at"])
            if row["production_last_edited_at"]
            else None
        )
        last_populated_at = (
            safe_datetime(row["production_last_populated_at"])
            if row["production_last_populated_at"]
            else None
        )

        max_date = max(
            first_reported_date,
            last_edited_at or datetime.min,
            last_populated_at or datetime.min,
        )

        if last_populated_at:
            if max_date == first_reported_date:
                populated_with_first_reported_last.add(yle_numerical_id)
                decision = (
                    "LIST 3. Populate happened BUT first reported date happened last. "
                    f"WILL IGNORE. CHECK --> {populated_with_first_reported_last_file.name}"
                )
            elif max_date == last_edited_at:
                decision = (
                    "LIST 3. Populate happened BUT last user edit was the last action. "
                    "KEEP REPORTAL VERSION"
                )
            elif max_date == last_populated_at:
                if last_edited_at:
                    if last_edited_at < first_reported_date:
                        decision = (
                            "LIST 3. Last user edit --> first report --> last populate action. "
                            "REVERT TO FIRST REPORTED VERSION"
                        )
                        restore_info = get_restore_info(
                            yle_numerical_id=yle_numerical_id,
                            prod_db=prod_db,
                            backup_db=backup_db,
                            sv_client=single_view_client,
                            config=config,
                            report_filename=row["first_reported_filename"],
                        )
                    else:
                        populated_after_user_edited_after_first_report.add(yle_numerical_id)
                        decision = (
                            "LIST 3. first report --> Last user edit --> last populate action. "
                            f"WILL IGNORE. CHECK --> {populated_after_user_edited_after_first_report_file.name}"
                        )
        else:
            if max_date == first_reported_date:
                decision = (
                    "LIST 3. No populate action. First report was last. "
                    "REVERT TO FIRST REPORTED VERSION"
                )
                restore_info = get_restore_info(
                    yle_numerical_id=yle_numerical_id,
                    prod_db=prod_db,
                    backup_db=backup_db,
                    sv_client=single_view_client,
                    config=config,
                    report_filename=row["first_reported_filename"],
                )
            elif max_date == last_edited_at:
                if last_edited_at:
                    if last_edited_at <= MATCH_IMPORT_HISTORY_START_DATE:
                        decision = (
                            "LIST 3. No populate action. Last user edit was last. BEFORE MATCH_IMPORT_HISTORY_START_DATE. "
                            "WILL IGNORE."
                        )
                    else:
                        decision = (
                            "LIST 3. No populate action. Last user edit was last. AFTER MATCH_IMPORT_HISTORY_START_DATE. "
                            "KEEP REPORTAL VERSION."
                        )

        program_info_list.append(ProgramInfo(
            yle_numerical_id=yle_numerical_id,
            decision=decision,
            av_work_operation=(
                restore_info.av_work_operation
                if restore_info
                else None
            ),
            music_work_operations=(
                restore_info.music_work_operations
                if restore_info
                else None
            )
        ))

    # dump programs listed
    write_report(
        populated_with_first_reported_last_file,
        populated_with_first_reported_last
    )
    write_report(
        populated_after_user_edited_after_first_report_file,
        populated_after_user_edited_after_first_report
    )

    return program_info_list


RESTORE_FN_MAPPING = {
    1: restore_using_report_1,
    2: restore_using_report_2,
    3: restore_using_report_3,
}


def report_intersections(programs_in_reports: dict[int, list[ProgramInfo]], config: Config) -> set[str]:
    """
    1. Find intersections between the 3 reports.
    2. Report said intersections.
    3. Return list of programs to blacklist in DB operations (do not commit these programs to PROD).
    """

    # DETECT INTERSECTIONS
    one = set(program.yle_numerical_id for program in programs_in_reports[1])
    two = set(program.yle_numerical_id for program in programs_in_reports[2])
    three = set(program.yle_numerical_id for program in programs_in_reports[3])

    one_n_two = one.intersection(two)
    one_n_three = one.intersection(three)
    two_n_three = two.intersection(three)
    one_n_two_n_three = one_n_two.intersection(three)

    intersection_rows = []
    for intersection, program_list in [
        ("1-2", one_n_two),
        ("1-3", one_n_three),
        ("2-3", two_n_three),
        ("1-2-3", one_n_two_n_three),
    ]:
        for yle_numerical_id in program_list:
            intersection_rows.append([intersection, yle_numerical_id])

    # Report intersections
    write_report(
        report_file=config.third_script_reports_dir / "intersections.csv",
        headers=["intersection", "yle_numerical_id"],
        rows=intersection_rows,
    )

    # return programs not to report due to intersections
    return (
        one_n_two.union(one_n_three).union(two_n_three).union(one_n_two_n_three)
    )


@ntfy(topic="zimmer")
def run() -> None:
    """The MAIN body for the script.

    """

    print("### START ###")

    load_dotenv()
    config = Config()

    if not config.third_script_dry_run:
        while input(
            "WARNING: Have you paused YLE's aggregations processor before running this script? [y/N]: "
        ) != "y":
            # we need to make sure the aggs processor is paused before running this script
            # but only if not in dry run mode
            pass

    prod_db = MongoClient(host=config.prod_mongo_uri).get_default_database()
    backup_db = MongoClient(host=config.backup_mongo_uri).get_default_database()

    single_view_client = SingleViewAPIClient(config)

    # this will hold the ProgramInfo for every stats_report
    programs_in_reports: dict[int, list[ProgramInfo]] = {}

    reports_in_fix_order = zip([1, 3, 2], [REPORTS[0], REPORTS[2], REPORTS[1]])
    stats_reports_pbar = tqdm(reports_in_fix_order, total=3)

    for report_idx, report_params in stats_reports_pbar:
        report_filename = report_params["report_filename"].replace("csv", "xlsx")
        stats_reports_pbar.set_description_str(report_filename)

        stats_report: Path = (config.stats_reports_dir / report_filename)
        if (
            not stats_report.exists() or
            not stats_report.is_file()
        ):
            raise RuntimeError(f"Could not find report {report_filename}")

        restore_fn = RESTORE_FN_MAPPING[report_idx]

        wb = openpyxl.load_workbook(stats_report.absolute())
        ws = wb.worksheets[0]
        rows = ws.iter_rows(values_only=True)
        headers = next(rows)

        programs_in_reports[report_idx] = restore_fn(
            headers=headers,
            rows=rows,
            prod_db=prod_db,
            backup_db=backup_db,
            single_view_client=single_view_client,
            config=config,
        )


    print("Remove intersections from final ProgramInfos + generate 2 lists with final PROD operations")
    programs_to_not_commit_into_prod = report_intersections(programs_in_reports, config)

    final_av_work_db_operations: list[UpdateOne] = []
    final_music_work_db_operations: list[Union[UpdateMany, InsertOne]] = []

    for report_index in programs_in_reports.keys():
        clean_list = []
        for program_info in programs_in_reports[report_index]:
            if program_info.yle_numerical_id in programs_to_not_commit_into_prod:
                continue

            clean_list.append(program_info)

            if program_info.av_work_operation:
                final_av_work_db_operations.append(program_info.av_work_operation)

            if program_info.music_work_operations:
                final_music_work_db_operations += program_info.music_work_operations

        programs_in_reports[report_index] = clean_list

    if not config.third_script_dry_run and (
        not final_av_work_db_operations or
        not final_music_work_db_operations
    ):
        raise RuntimeError("No operations for DB!")

    decision_count = defaultdict(int)
    dry_run_rows = []
    for key in programs_in_reports.keys():
        for program_info in programs_in_reports[key]:
            dry_run_rows.append([program_info.yle_numerical_id, program_info.decision])
            decision_count[program_info.decision] += 1

    total_programs_to_report = len(programs_in_reports[1]) + len(programs_in_reports[2]) + len(programs_in_reports[3])
    print(f"Report decisions taken for each program (total={total_programs_to_report})")
    write_report(
        report_file=config.third_script_reports_dir / "dry_run.csv",
        headers=["yle_numerical_id", "decision"],
        rows=dry_run_rows,
    )

    print("Report program counts grouped by decision")
    write_report(
        report_file=config.third_script_reports_dir / "dry_run_counts_grouped_by_reason.csv",
        headers=["decision", "program_count"],
        rows=sorted(decision_count.items(), key=lambda x: x[1]),
    )

    if not config.third_script_dry_run:
        print("Commit final operations to DB")
        prod_update_pbar = tqdm(total=2)

        prod_update_pbar.set_description_str(
            f"Updating {len(final_music_work_db_operations)} MusicWorks"
        )
        prod_db.music_work.bulk_write(final_music_work_db_operations, ordered=False)
        prod_update_pbar.update(1)

        prod_update_pbar.set_description_str(
            f"Updating {len(final_av_work_db_operations)} AvWorks"
        )
        prod_db.av_work.bulk_write(final_av_work_db_operations, ordered=False)
        prod_update_pbar.update(1)


        if config.third_script_generate_post_reports:
            print("Report updated AvWorks in PROD")
            write_report(
                report_file=config.third_script_reports_dir / "updated_av_works.csv",
                headers=["reportal_id", "yle_numerical_id"],
                rows=(
                    (str(aw["_id"]), aw["yle_numerical_id"])
                    for aw in
                    prod_db.av_work.find(
                        {"extras.YLE_2180": {"$ne": None}},
                        {"_id": 1, "yle_numerical_id": "$work_ids.yle_numerical_id"}
                    )
                )
            )
            print("Report updated MusicWorks in PROD that need to be re-enriched (tagged with extras.YLE_2180 and with single_view_id)")
            write_report(
                report_file=config.third_script_reports_dir / "updated_music_works_to_be_re_enriched.csv",
                rows=(
                    str(mw["_id"])
                    for mw in
                    prod_db.music_work.find(
                        {"extras.YLE_2180": {"$ne": None}},
                        {"_id": 1}
                    )
                )
            )
            print("Report updated MusicWorks in PROD that have at least 1 contributor with role=other_contributor")
            write_report(
                report_file=config.third_script_reports_dir / "updated_music_works_with_other_contributor_as_role.csv",
                rows=(
                    str(mw["_id"])
                    for mw in
                    prod_db.music_work.find(
                        {"extras.YLE_2180": {"$ne": None}, "contributors.role": "other_contributor"},
                        {"_id": 1}
                    )
                )
            )

    print("### END ###")


if __name__ == "__main__":
    run()
