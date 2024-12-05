"""
# cuesheet = [mw.id and mw.title (editado) for cue in av_work.cuesheet]

initial_versions = {}
for each report sorted by date:
  for each cuesheet in the report:
     if cuesheet not in initial_versions:
       initial_versions[cuesheet.rapnro] = cuesheet
     else:
       if initial_versions[cuesheet.rapnro] != cuesheet:
          add to badly reported cuesheets
"""
import sys
import time
import csv
from datetime import date, datetime
import sqlite3
from typing import Union
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from tqdm import tqdm
from tqdm.contrib import tenumerate

from scripts.utils.decorators import ntfy
from scripts.yle.restore_av_works_from_reports.config import Config
from scripts.yle.restore_av_works_from_reports.queries import (
    SQL_REPORT_3,
    REPORTS,
)
from scripts.yle.restore_av_works_from_reports.xml_like_orm import MUSIC_SOURCE, ProgramFinder



def parse_xml_files(
    program_finder: ProgramFinder,
    cur: sqlite3.Cursor,
    con: sqlite3.Connection
):
    """

    """

    print("Parsing XML files to populate local reported_program table...")

    cur.execute("drop table if exists reported_program")
    cur.execute("drop table if exists mw_info")
    cur.execute("drop table if exists cuesheet")

    cur.execute("""
        create table reported_program(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yle_numerical_id,
            plasma_id,
            report_filename,
            report_date,
            program_title,
            is_filler
        )
    """)
    cur.execute("create index idx_reported_program_yle_numerical_id on reported_program (yle_numerical_id)")

    cur.execute("""
        create table mw_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mw_id,
            mw_title,
            cue_duration,
            mw_source,
            reported_program_id,
            FOREIGN KEY(reported_program_id) REFERENCES reported_program(id)
        )
    """)

    cur.execute("create table cuesheet (reported_program_id integer, data string)")
    cur.execute("create index idx_cuesheet_reported_program_id on cuesheet (reported_program_id)")

    for report_file in tqdm(
        program_finder.report_files,
        total=program_finder.total_report_files,
        unit="XML report file"
    ):
        for program in report_file.programs:
            cur.execute("""
                insert into reported_program (
                    yle_numerical_id,
                    plasma_id,
                    report_filename,
                    report_date,
                    program_title,
                    is_filler
                ) values (?,?,?,?,?,?)
                """,
                (
                    program.yle_numerical_id,
                    program.plasma_id,
                    report_file.name,
                    program.report_date,
                    program.title,
                    program.is_filler
                )
            )
            reported_program = cur.lastrowid

            for cue in program.cues:
                cur.execute("""
                    INSERT INTO mw_info (
                        mw_id,
                        mw_title,
                        cue_duration,
                        mw_source,
                        reported_program_id
                    ) VALUES (?,?,?,?,?)
                    """,
                    (
                        cue.music_work_id,
                        cue.music_work_title,
                        cue.cue_duration,
                        cue.music_work_source,
                        reported_program,
                    )
                )

    con.commit()

    cur.execute("""
        insert into cuesheet (reported_program_id, data)
        select
            reported_program_id,
            group_concat(mw_id order by mw_id) as data
        from
            mw_info
        group by
            reported_program_id;
    """)
    con.commit()

    print("Done\n")


def populate_with_prod_data(
    cur: sqlite3.Cursor,
    con: sqlite3.Connection,
    mongo_db: Database
):
    """Populates local DB with Reportal PROD current cuesheet info."""

    print("Populating local DB with YLE prod programs current status...")

    cur.execute("drop table if exists production_program")
    cur.execute("drop table if exists production_mw_info")
    cur.execute("drop table if exists production_cuesheet")

    cur.execute("""
        create table production_program (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yle_numerical_id,
            program_title,
            last_edited_at,
            last_populated_at,
            approved,
            is_filler
        )
    """)
    cur.execute("create index idx_production_program_yle_numerical_id on production_program (yle_numerical_id)")

    cur.execute("""
        create table production_mw_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yle_numerical_id,
            production_program_id,
            program_title,
            mw_id,
            mw_title,
            cue_duration,
            mw_source,
            last_edited_at,
            last_populated_at,
            approved
        )
    """)
    cur.execute("create index idx_production_mw_info_program on production_mw_info (yle_numerical_id, production_program_id)")

    cur.execute("create table production_cuesheet (yle_numerical_id string, production_program_id, data string)")

    cur.execute("select distinct yle_numerical_id from reported_program")
    yle_numerical_ids = [_[0] for _ in cur.fetchall()]

    print(f"{len(yle_numerical_ids)} unique programs parsed that we need to check in production DB")

    query = {"work_ids.yle_numerical_id": {"$in": yle_numerical_ids}}
    total = mongo_db.av_work.count_documents(query)

    print(f"{total} found out of {len(yle_numerical_ids)} reported programs")

    cue_info = mongo_db.av_work.aggregate([
        {"$match": query},
        {"$unwind": {"path": "$cuesheet.cues", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "program_title": {"$ifNull": ["$titles.original_title", "$titles.full_name"]},
            "yle_numerical_id": "$work_ids.yle_numerical_id",
            "cue": "$cuesheet.cues",
            "last_edited_at": "$history_info.last_editor.updated_at",
            "last_populated_at": "$import_status.populated.created_at",
            "approved": 1,
            "is_filler": "$extras.filler"
        }},
        {"$lookup": {
            "from": "music_work",
            "as": "mw",
            "localField": "cue.music_work",
            "foreignField": "_id",
        }},
        {"$unwind": {"path": "$mw", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "program_title": 1,
            "yle_numerical_id": 1,
            "mw_id": "$mw._id",
            "mw_title": "$mw.title",
            "mw_source": "$mw.source",
            "cue_index": "$cue.cue_index",
            "cue_duration": "$cue.duration",
            "last_edited_at": 1,
            "last_populated_at": 1,
            "approved": 1,
            "is_filler": 1,
        }},
    ])

    saved_programs = {}

    for cue in tqdm(
        cue_info,
        total=total,
        unit="cues",
        desc="Populating local DB with YLE PROD data"
    ):
        yle_numerical_id = cue["yle_numerical_id"]
        program_title = cue.get("program_title")
        last_edited_at = cue.get("last_edited_at")
        last_populated_at = cue.get("last_populated_at")
        approved = cue.get("approved")

        if yle_numerical_id not in saved_programs:
            is_filler = get_is_filler(cue)

            program_id = next(cur.execute(
                """
            insert into production_program (
                yle_numerical_id,
                program_title,
                last_edited_at,
                last_populated_at,
                approved,
                is_filler
            ) values (?,?,?,?,?,?)
                returning id
            """, (yle_numerical_id, program_title, last_edited_at, last_populated_at, approved, is_filler)
            ))[0]

            saved_programs[yle_numerical_id] = program_id

        mw_id = cue.get("mw_id")

        # We've set preserveNullAndEmptyArrays to true when unwinding in the aggregation
        # pipeline so we need to check a field we know cannot be null, to detect that the
        # collection was empty
        if not mw_id:
            continue

        cur.execute("""
            insert into production_mw_info (
                yle_numerical_id,
                production_program_id,
                program_title,
                mw_id,
                mw_title,
                mw_source,
                cue_duration,
                last_edited_at,
                last_populated_at,
                approved
            ) values (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                yle_numerical_id,
                saved_programs[yle_numerical_id],
                program_title,
                str(mw_id),
                cue.get("mw_title"),
                MUSIC_SOURCE.get(cue.get("mw_source")),
                cue.get("cue_duration"),
                last_edited_at,
                last_populated_at,
                approved
            )
        )
    con.commit()

    cur.execute("""
        insert into production_cuesheet (yle_numerical_id, production_program_id, data)
            select
                yle_numerical_id,
                production_program_id,
                group_concat(mw_id order by mw_id) as data
            from
                production_mw_info
            group by
                yle_numerical_id, production_program_id;
    """)
    con.commit()

    print("Done\n")


def populate_with_backup_data(
    cur: sqlite3.Cursor,
    con: sqlite3.Connection,
    mongo_db: Database
):
    """Populates local DB with Reportal BACKUP cuesheet info."""

    cur.execute("drop table if exists backup_program")
    cur.execute("drop table if exists backup_mw_info")
    cur.execute("drop table if exists backup_cuesheet")

    cur.execute("""
        create table backup_program (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yle_numerical_id,
            program_title,
            approved,
            is_filler
        )
    """)
    cur.execute("create index idx_backup_program_yle_numerical_id on backup_program (yle_numerical_id)")

    cur.execute("""
        create table backup_mw_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_title,
            yle_numerical_id,
            backup_program_id,
            mw_id,
            mw_title,
            cue_duration,
            mw_source,
            approved
        )
    """)
    cur.execute("create index idx_backup_mw_info_program on backup_mw_info (yle_numerical_id, backup_program_id)")

    cur.execute("create table backup_cuesheet (yle_numerical_id string, backup_program_id, data string)")

    print("Populating local DB with YLE BACKUP programs status")

    cur.execute("select distinct yle_numerical_id from reported_program")
    yle_numerical_ids = [_[0] for _ in cur.fetchall()]

    print(f"{len(yle_numerical_ids)} unique programs parsed that we need to check in BACKUP DB")

    query = {"work_ids.yle_numerical_id": {"$in": yle_numerical_ids}}
    total = mongo_db.av_work.count_documents(query)

    print(f"{total} / {len(yle_numerical_ids)} programs found in backup")

    cue_info = mongo_db.av_work.aggregate([
        {"$match": query},
        {"$unwind": {"path": "$cuesheet.cues", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "program_title": {"$ifNull": ["$titles.original_title", "$titles.full_name"]},
            "yle_numerical_id": "$work_ids.yle_numerical_id",
            "cue": "$cuesheet.cues",
            "last_edited_at": "$history_info.last_editor.updated_at",
            "last_populated_at": "$import_status.populated.created_at",
            "approved": 1,
            "is_filler": "$extras.filler"
        }},
        {"$lookup": {
            "from": "music_work",
            "as": "mw",
            "localField": "cue.music_work",
            "foreignField": "_id",
        }},
        {"$unwind": {"path": "$mw", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "program_title": 1,
            "yle_numerical_id": 1,
            "mw_id": "$mw._id",
            "mw_title": "$mw.title",
            "mw_source": "$mw.source",
            "cue_index": "$cue.cue_index",
            "cue_duration": "$cue.duration",
            "approved": 1,
            "is_filler": 1,
        }},
    ])

    saved_programs = {}

    for cue in tqdm(
        cue_info,
        total=total,
        unit="cues",
        desc="Populating local DB with YLE BACKUP data"
    ):
        yle_numerical_id = cue["yle_numerical_id"]
        program_title = cue.get("program_title")
        approved = cue.get("approved")

        if yle_numerical_id not in saved_programs:
            is_filler = get_is_filler(cue)

            program_id = next(cur.execute(
                """
            insert into backup_program (
                yle_numerical_id,
                program_title,
                approved,
                is_filler
            ) values (?,?,?,?)
                returning id
            """, (yle_numerical_id, program_title, approved, is_filler)
            ))[0]

            saved_programs[yle_numerical_id] = program_id

        mw_id = cue.get("mw_id")

        # We've set preserveNullAndEmptyArrays to true when unwinding in the aggregation
        # pipeline so we need to check a field we know cannot be null, to detect that the
        # collection was empty
        if not mw_id:
            continue

        cur.execute("""
            INSERT INTO backup_mw_info (
                yle_numerical_id,
                backup_program_id,
                program_title,
                mw_id,
                mw_title,
                mw_source,
                cue_duration,
                approved
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                yle_numerical_id,
                saved_programs[yle_numerical_id],
                program_title,
                str(mw_id),
                cue.get("mw_title"),
                MUSIC_SOURCE.get(cue.get("mw_source")),
                cue.get("cue_duration"),
                approved,
            )
        )
    con.commit()

    cur.execute("""
        insert into backup_cuesheet (yle_numerical_id, backup_program_id, data)
            select
                yle_numerical_id,
                backup_program_id,
                group_concat(mw_id order by mw_id) as data
            from
                backup_mw_info
            group by
                yle_numerical_id, backup_program_id;
    """)
    con.commit()

    print("Done\n")


def get_is_filler(cue_with_program_info) -> bool:
    if cue_with_program_info.get("is_filler", False):
        return True
    return False


def generate_reports(cur: sqlite3.Cursor, con: sqlite3.Connection, config: Config):
    """Generates the reports using local sqlite DB."""

    # Get max cues per program. This is an important optimization since join on generated
    # series based on this value
    max_cues_per_program = next(cur.execute("""
        select max(cue_count)
        from
          (select count(1) as cue_count
           from production_mw_info
           group by yle_numerical_id

           union select count(1) as cue_count
           from backup_mw_info
           group by yle_numerical_id

           union select count(1) as cue_count
           from mw_info
           group by reported_program_id)
    """))[0]

    max_cues_per_program += 1

    print("\n*** Generating reports with {} max queues per program ***\n".format(max_cues_per_program), file=sys.stderr)

    def _gen_report(
        report_filename: str,
        sql: str,
        fields: list[str],
        remove_last_value: bool = False,
    ):
        start = time.time()
        final_sql = sql.format(max_cues_per_program)

        print_execution_plan(report_filename, cur, final_sql)

        res = cur.execute(final_sql)

        report_file = config.stats_reports_dir / report_filename
        report_file.touch(exist_ok=True)

        with report_file.open(mode="wt") as f:
            # header
            writer = csv.writer(f)
            writer.writerow(fields)

            while row_values := res.fetchone():
                # we discard the last value
                row_values = list([v or "" for v in row_values])
                if remove_last_value:
                    row_values = row_values[:-1]
                writer.writerow(row_values)

        end = time.time()
        print("\n*** Generated report {} in {} seconds ***\n".format(report_filename, end - start), file=sys.stderr)

    def store_report_3_in_local_db():
        print("Storing report 3 results in local DB, this will take time.")

        start = time.time()
        cur.execute("drop table if exists report_3")
        cur.execute("""
            create table report_3 (
                yle_numerical_id,
                first_reported_program_title,
                first_reported_id,
                first_reported_date,
                first_reported_filename,
                first_reported_cue_id,
                first_reported_cue_title,
                first_reported_cue_duration,
                first_reported_music_source,
                other_reported_program_title,
                other_reported_id,
                other_reported_date,
                other_reported_filename,
                other_reported_cue_id,
                other_reported_cue_title,
                other_reported_cue_duration,
                other_reported_music_source,
                production_last_edited_at,
                production_last_populated_at
            )
        """)

        final_sql = f"""
            insert into report_3
                {SQL_REPORT_3.format(max_cues_per_program)}
        """

        query_name = "store_report_3"
        print_execution_plan(query_name, cur, final_sql)

        cur.execute(final_sql)

        con.commit()

        end = time.time()

        print("\n*** Stored report 3 results in {} seconds ***\n".format(end - start), file=sys.stderr)

    print("Generating reports...")
    stored_report_3_in_memory = False

    for rep_idx, report_params in tenumerate(REPORTS, start=1, unit="reports"):
        if getattr(config, f"do_report_{rep_idx}") is not True:
            continue

        if rep_idx in [1, 3] and not stored_report_3_in_memory:
            # report 1 and 3 require this report to be stored in memory
            # but we just need to do it once
            store_report_3_in_local_db()
            stored_report_3_in_memory = True

        _gen_report(**report_params)

    print("Done\n")


def print_execution_plan(name: str, cur: sqlite3.Cursor, sql: str):
    rows = []
    indent_levels = {}

    for node_id, parent_id, _, detail in cur.execute("explain query plan {}".format(sql)):
        indent_level = 0 if parent_id not in indent_levels else indent_levels[parent_id] + 1
        indent_levels[node_id] = indent_level
        rows.append("   " * indent_level + detail)

    print("\n*** Execution plan for {}:\n".format(name), file=sys.stderr)
    result = '\n'.join(rows)
    print(result, file=sys.stderr)


def fix_pre_yle_numerical_id_using_plasma_id(
    cur: sqlite3.Cursor,
    con: sqlite3.Connection,
    mongo_db: Database
):
    """Updates yle_numerical_id using plasma_id for those programs it could not find.

        Some program rows come from pre-yle_numerical_id reports, so we need to use the plasma_id
        to find a match in Reportal PROD DB and update the yle_numerical_id so we can later on
        join by said column.
    """

    print("Fixing pre-yle_numerical_id by matching their plasma_id...")

    cur.execute("""
        select distinct
          yle_numerical_id,
          plasma_id
        from reported_program
        where
          plasma_id != '' and
          plasma_id is not null
        order by plasma_id
    """)

    yle_numerical_id__plasma_id = list(cur.fetchall())

    total = len(yle_numerical_id__plasma_id)

    print(f"{total} rows that we are going to check in PROD.")

    prod_yle_numerical_id__plasma_id = set()

    for yle_identifiers in tqdm(yle_numerical_id__plasma_id, total=total):
        """
            Try to find in DB the AvWork by matching the `yle_numerical_id`
        """
        query = {"work_ids.yle_numerical_id": yle_identifiers[0]}
        project = {
            "yle_numerical_id": "$work_ids.yle_numerical_id",
            "plasma_id": "$work_ids.plasma_id",
            "legacy_yle_id": "$work_ids.legacy_yle_id"
        }

        av_work = mongo_db.av_work.find_one(query, project)

        if av_work is None:
            """
                Try to find av_work using other means
            """
            other_query = {
                "$or": [
                    {"work_ids.plasma_id": yle_identifiers[1]},
                    # # could be in the legacy_yle_id. eg: Ceiton_X --> X
                    {"work_ids.legacy_yle_id": yle_identifiers[1]},
                ],
            }
            av_work = mongo_db.av_work.find_one(other_query, project)

        if av_work is not None:
            prod_yle_numerical_id__plasma_id.add((
                av_work["yle_numerical_id"],
                av_work["plasma_id"],
                av_work.get("legacy_yle_id")
            ))
        else:
            print(f"{yle_identifiers[0]} not found in prod using {yle_identifiers[1]}")

    total_found = len(prod_yle_numerical_id__plasma_id)

    print(
        f"{total_found} / {total} programs found --> we cannot find {total - total_found} via yle_numerical_ids"
    )

    """
        Get a list of yle_numerical_id that we have when fetching programs from Production.
        Compare that against the yle_numerical_id list we have from the XMLs
        
        Calculate the set containing the `(yle_numerical_id, plasma_id, legacy_yle_id)` which needs to be fixed 
            by removing the overlapping yle_numerical_ids.
    """
    prod_yle_numerical_id_items = {p_row[0] for p_row in tqdm(prod_yle_numerical_id__plasma_id, total=total_found)}

    need_to_fix_yle_numerical_id__plasma_id = [
        row
        for row in tqdm(yle_numerical_id__plasma_id, total=total)
        if row[0] not in prod_yle_numerical_id_items
    ]

    actual_values = {}
    for row in prod_yle_numerical_id__plasma_id:
        actual_values[row[1]] = row[0]
        if row[2] and row[2]:
            actual_values[row[2]] = row[0]

    print(f"{len(need_to_fix_yle_numerical_id__plasma_id)} rows need fixing for yle_numerical_id")

    for yle_numerical_id, plasma_id in tqdm(
        need_to_fix_yle_numerical_id__plasma_id,
        unit="row",
        desc="Fixing pre-yle_numerical_id"
    ):
        actual_yle_numerical_id = actual_values.get(plasma_id)
        if not actual_yle_numerical_id:
            print(f"{yle_numerical_id=} not found in prod using {plasma_id=}")
            continue

        # update only mismatches
        cur.execute("""
            update reported_program
            set yle_numerical_id = ?
            where
                plasma_id = ?
        """, (
            actual_yle_numerical_id,
            plasma_id,
        ))

    con.commit()

    print("Done\n")


def populate_first_reported_version_table(
    cur: sqlite3.Cursor,
    con: sqlite3.Connection
):
    """Populates first_reports_version table
    with XML programs so that this table only contains
    the first appearance of a program in a report ever.
    """

    print("Generating first_reported_version table from reported_program table...", end="")

    cur.execute("drop table if exists first_reported_version")
    cur.execute("""
        create table first_reported_version (
            yle_numerical_id,
            id,
            report_date
        )
    """)
    cur.execute("""
        insert into first_reported_version (yle_numerical_id, id, report_date)
            select
                yle_numerical_id,
                id,
                report_date
            from (
                select
                    yle_numerical_id,
                    id,
                    report_date,
                    rank() over (
                        partition by
                            yle_numerical_id
                        order by
                            report_date, id
                    ) as row_rank
                from
                    reported_program
            )
            where
                row_rank = 1
    """)
    con.commit()

    print("Done\n")


def populate_last_reported_version_table(
    cur: sqlite3.Cursor,
    con: sqlite3.Connection
):
    """Populates last_reports_version table
    with XML programs so that this table only contains
    the first appearance of a program in a report ever.
    """

    print("Generating last_reported_version table from reported_program table...", end="")

    cur.execute("drop table if exists last_reported_version")
    cur.execute("""
        create table last_reported_version (
            yle_numerical_id,
            id,
            report_date
        )
    """)
    cur.execute("""
        insert into last_reported_version (yle_numerical_id, id, report_date)
            select distinct
                yle_numerical_id,
                last_value(id) over (
                    partition by yle_numerical_id
                    order by report_date, id
                    range between unbounded preceding
                    and unbounded following
                ) as last_id,
                last_value(report_date) over (
                    partition by yle_numerical_id
                    order by report_date, id
                    range between unbounded preceding
                    and unbounded following
                ) as last_report_date
            from
                reported_program
            order by yle_numerical_id asc
    """)
    con.commit()

    print("Done\n")


@ntfy()
def run() -> None:
    """The MAIN body for the script.

    1. Init setup
        - Read config from env
        - MongoDB Backup connection
        - MongoDB PROD connection
        - Local sqlite3 reported_programs connection
    2. Ask the user to populate local SQLite DB parsing XML files
    2.1. If reports dir is empty OR user anwsers `y` to download reports from bazaar
    2.1.1. Download reports from bazaar
    2.2. Start parsing XML files to populate local DB with reported programs info
    3. If we just parsed new XML files OR user answers `y` to fix pre yle_numerical_id programs
    3.1. Try and find all programs in PROD DB, then update local DB to ensure all yle_numerical_ids
         map to PROD programs
    4. Populate local DB with a new table with all first reported versions of each program
    5. Populate local DB with a new table with all last reported versions of each program
    6. If user answers `y` to populate local DB with PROD data
    6.1. Populate local DB with PROD data
    7. If user answers `y` to populate local DB with BACKUP data
    7.1. Populate local DB with BACKUP data
    8. Generate reports
    """

    print("### START ###")

    def adapt_datetime_iso(v: datetime) -> str:
        return v.isoformat()

    def adapt_date_iso(v: date) -> str:
        return v.isoformat()

    def convert_datetime(v: Union[bytes, str]) -> datetime:
        if isinstance(v, bytes):
            v = v.decode()
        return datetime.fromisoformat(v)  # type: ignore

    def convert_date(v: Union[bytes, str]) -> datetime:
        if isinstance(v, bytes):
            v = v.decode()
        return date.fromisoformat(v)  # type: ignore

    sqlite3.register_adapter(datetime, adapt_datetime_iso)
    sqlite3.register_adapter(date, adapt_date_iso)
    sqlite3.register_converter("datetime", convert_datetime)
    sqlite3.register_converter("date", convert_date)

    load_dotenv()
    config = Config()

    con = sqlite3.connect("reported_programs.db")
    cur = con.cursor()
    prod_db = MongoClient(host=config.prod_mongo_uri).get_default_database()
    backup_db = MongoClient(host=config.backup_mongo_uri).get_default_database()
    do_fix_yle_numerical_ids = False

    if input("- Populate local SQLite DB with XML files data? [y/N]: ") == "y":
        program_finder = ProgramFinder(config)
        parse_xml_files(program_finder, cur, con)
        do_fix_yle_numerical_ids = True

    if (
        do_fix_yle_numerical_ids or
        input("- Fix yle_numerical_ids using plasma_id? [y/N]: ") == "y"
    ):
        fix_pre_yle_numerical_id_using_plasma_id(cur, con, prod_db)

    populate_first_reported_version_table(cur, con)
    populate_last_reported_version_table(cur, con)

    if input("- Populate local SQLite DB with PROD data? [y/N]: ") == "y":
        populate_with_prod_data(cur, con, prod_db)

    if input("- Populate local SQLite DB with BACKUP data? [y/N]: ") == "y":
        populate_with_backup_data(cur, con, backup_db)

    _ = cur.execute("VACUUM").fetchone()

    generate_reports(cur, con, config)

    con.close()

    print("### END ###")


if __name__ == "__main__":
    run()
