import csv
import logging
import os
import json
import re
import sqlite3
import time
from bazaar import FileSystem
from datetime import date, datetime
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, field_validator
from pymongo import MongoClient
from typing import Any, Optional, Union
from tqdm import tqdm

from scripts.nrk.rcdev_392_overwritten_cuesheets.queries import DIFF_REPORT_SQL_QUERIES
from scripts.utils.decorators import ntfy


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        arg_pattern = re.compile(r'%\((\w+)\)')
        arg_names = [x.group(1) for x in arg_pattern.finditer(self._fmt)]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = None

        return super().format(record)


sh = logging.StreamHandler()
fh = logging.FileHandler("rcdev_392.log")

logger = logging.getLogger("RCDEV-392")
logger.setLevel(logging.INFO)
logger.handlers.append(fh)

formatter = CustomFormatter("%(asctime)s - %(levelname)s:%(name)s: %(message)s - %(info)s")
for handler in logger.handlers:
    handler.setFormatter(formatter)


DEFAULT_REPORT_NAMESPACES = "nrk-daily-reports,nrk-monthly-reports,nrk-schedules-daily-reports"


class Config:
    def __init__(self) -> None:
        if __name__ == "__main__":
            self.parent_dir = Path(__file__).parent
        else:
            self.parent_dir = Path(os.getcwd())

        self.reports_dir = self.parent_dir / "reports"
        self.diff_reports = self.parent_dir / "diff_reports"

        self.diff_reports.mkdir(parents=True, exist_ok=True)

        bazaar_mongo_uri = os.getenv("BAZAAR_MONGO_URI")
        bazaar_storage_uri = os.getenv("BAZAAR_STORAGE_URI")
        nrk_mongo_uri = os.getenv("NRK_MONGO_URI")

        assert bazaar_mongo_uri is not None
        assert bazaar_storage_uri is not None
        assert nrk_mongo_uri is not None

        self.bazaar_mongo_uri = bazaar_mongo_uri
        self.bazaar_storage_uri = bazaar_storage_uri
        self.nrk_mongo_uri = nrk_mongo_uri

        self.report_namespaces = os.getenv("REPORT_NAMESPACES", DEFAULT_REPORT_NAMESPACES).split(",")
        self.sqlite_db_name = os.getenv("SQLITE_DB_NAME", "program_info.db")


class ReportCue(BaseModel):
    cue_nr: int
    musicwork_id: str
    musicwork_title: str
    usage_duration: int
    music_source: Optional[str]

    @field_validator("usage_duration", mode="before")
    @classmethod
    def validate_usage_duration(cls, v: str) -> int:
        """Duration is expressed as hh:mm:ss, we need total seconds."""

        hh, mm, ss = v.split(":")
        return int(ss) + int(mm) * 60 + int(hh) * 3600


class Production(BaseModel):
    program_id: str
    title: Optional[str]
    cues: list[ReportCue]

    @field_validator("cues", mode="before")
    @classmethod
    def validate_cues(cls, v: Optional[list[dict[str, Any]]]) -> list:
        if v is None:
            return []
        return v

class Transmission(BaseModel):
    production: Production


class ReportFile(BaseModel):
    file_date: str
    transmissions: list[Transmission]


class SQLiteDBManager:
    def __init__(self, config: Config) -> None:
        self.config = config

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

        self.con = sqlite3.connect(config.sqlite_db_name)
        self.cur = self.con.cursor()
        self.client_db = MongoClient(host=config.nrk_mongo_uri).get_default_database()

    def vacuum(self):
        logger.info("Cleaning dust... (VACUUM)")
        _ = self.cur.execute("VACUUM").fetchone()
        logger.info("Cleaning dust... (VACUUM) - OK")

    @ntfy()
    def ingest_reports(self) -> None:
        logger.info("Ingesting reports...")

        self.cur.execute("drop table if exists reported_program")
        self.cur.execute("drop table if exists reported_mw_info")
        self.cur.execute("drop table if exists reported_cuesheet")

        self.cur.execute("""
            create table reported_program(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id,
                report_filename,
                report_date,
                program_title
            )
        """)
        self.cur.execute("create index idx_reported_program_program_id on reported_program (program_id)")

        self.cur.execute("""
            create table reported_mw_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mw_id,
                mw_title,
                cue_duration,
                mw_source,
                reported_program_row_id,
                FOREIGN KEY(reported_program_row_id) REFERENCES reported_program(id)
            )
        """)

        self.cur.execute("""
            create table reported_cuesheet (
                reported_program_row_id integer,
                data string,
                FOREIGN KEY(reported_program_row_id) REFERENCES reported_program(id)
            )
        """)
        self.cur.execute("create index idx_reported_cuesheet_reported_program_row_id on reported_cuesheet (reporteD_program_row_id)")

        report_files = [_ for _ in self.config.reports_dir.iterdir()]
        for report_file in tqdm(report_files, unit="Report files"):
            report_file_obj = ReportFile.model_validate_json(report_file.read_text())

            for program in report_file_obj.transmissions:
                # From Slack conv with Xhon: we should ignore all monthly with no cues
                # monthly reports have "digital_usages" in the filename
                if "digital_usages" in report_file.name and not program.production.cues:
                    continue

                reported_program_row_id = next(self.cur.execute("""
                    insert into reported_program (
                        program_id,
                        report_filename,
                        report_date,
                        program_title
                    ) values (?,?,?,?)
                        returning id
                    """,
                    (
                        program.production.program_id,
                        report_file.name,
                        report_file_obj.file_date,
                        program.production.title,
                    )
                ))[0]

                for cue in program.production.cues:
                    self.cur.execute("""
                        INSERT INTO reported_mw_info (
                            mw_id,
                            mw_title,
                            cue_duration,
                            mw_source,
                            reported_program_row_id
                        ) VALUES (?,?,?,?,?)
                        """,
                        (
                            cue.musicwork_id,
                            cue.musicwork_title,
                            cue.usage_duration,
                            cue.music_source,
                            reported_program_row_id,
                        )
                    )
        self.con.commit()

        self.cur.execute("""
            insert into reported_cuesheet (reported_program_row_id, data)
            select
                reported_program_row_id,
                group_concat(mw_id order by mw_id) as data
            from
                reported_mw_info
            group by
                reported_program_row_id
        """)
        self.con.commit()

        logger.info("Ingesting reports...DONE")

        self._populate_last_reported_table()
        self._populate_first_reported_table()

    @ntfy()
    def ingest_prod_db(self) -> None:
        logger.info("Ingesting prod DB...")

        self.cur.execute("drop table if exists production_program")
        self.cur.execute("drop table if exists production_mw_info")
        self.cur.execute("drop table if exists production_cuesheet")

        self.cur.execute("""
            create table production_program (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id,
                program_title,
                last_edited_at,
                last_populated_at,
                approved
            )
        """)
        self.cur.execute(
            "create index idx_production_program_program_id on production_program (program_id)"
        )

        self.cur.execute("""
            create table production_mw_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id,
                production_program_row_id,
                program_title,
                mw_id,
                mw_title,
                mw_source,
                cue_duration,
                last_edited_at,
                last_populated_at,
                approved,
                FOREIGN KEY(production_program_row_id) REFERENCES production_program(id)
            )
        """)
        self.cur.execute("create index idx_production_mw_info_program on production_mw_info (program_id, production_program_row_id)")
        self.cur.execute("""
            create table production_cuesheet (
                program_id string,
                production_program_row_id int,
                data string
                FOREIGN KEY(production_program_row_id) REFERENCES production_program(id)
            )
        """)

        self.cur.execute("select distinct program_id from reported_program")
        reported_program_ids = [_[0] for _ in self.cur.fetchall()]
        total_reported_program_ids = len(reported_program_ids)

        logger.info(f" - {total_reported_program_ids=} that we need to retrieve from production DB")

        query = {"work_ids.program_id": {"$in": reported_program_ids}}
        total_prod_program_ids = self.client_db.av_work.count_documents(query)

        logger.info(f" - {total_prod_program_ids=} found out of {total_reported_program_ids=}")

        cue_info = self.client_db.av_work.aggregate([
            {"$match": query},
            {"$unwind": {"path": "$cuesheet.cues", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "program_title": {"$ifNull": ["$titles.original_title", "$titles.full_name"]},
                "program_id": "$work_ids.program_id",
                "cue": "$cuesheet.cues",
                "last_edited_at": "$history_info.last_editor.updated_at",
                "last_populated_at": "$import_status.populated.created_at",
                "approved": 1,
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
                "program_id": 1,
                "program_title": 1,
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
            total=total_prod_program_ids,
            unit="cues",
            desc="Populating local DB with PROD data"
        ):
            program_id = cue["program_id"]
            program_title = cue.get("program_title")
            last_edited_at = cue.get("last_edited_at")
            last_populated_at = cue.get("last_populated_at")
            approved = cue.get("approved", False)

            if program_id not in saved_programs:
                production_program_row_id = next(self.cur.execute(
                    """
                    insert into production_program (
                        program_id,
                        program_title,
                        last_edited_at,
                        last_populated_at,
                        approved
                    ) values (?,?,?,?,?)
                        returning id
                    """, (
                        program_id,
                        program_title,
                        last_edited_at,
                        last_populated_at,
                        approved
                    )
                ))[0]

                saved_programs[program_id] = production_program_row_id

            # We've set preserveNullAndEmptyArrays to true when unwinding in the aggregation
            # pipeline so we need to check a field we know cannot be null, to detect that the
            # collection was empty
            if not (mw_id := cue.get("mw_id")):
                continue

            self.cur.execute("""
                insert into production_mw_info (
                    program_id,
                    production_program_row_id,
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
                    program_id,
                    saved_programs[program_id],
                    program_title,
                    str(mw_id),
                    cue.get("mw_title"),
                    cue.get("mw_source"),
                    cue.get("cue_duration"),
                    last_edited_at,
                    last_populated_at,
                    approved
                )
            )
        self.con.commit()

        self.cur.execute("""
            insert into production_cuesheet (program_id, production_program_row_id, data)
                select
                    program_id,
                    production_program_row_id,
                    group_concat(mw_id order by mw_id) as data
                from
                    production_mw_info
                group by
                    program_id, production_program_row_id;
        """)
        self.con.commit()

        logger.info("Ingesting prod DB...DONE")

    def _populate_last_reported_table(self):
        """Populates last_reported_version table with reported info
        to contain only the last appearance of a program among all reports.
        """

        logger.info("Generating last_reported_version table from reported_program table...")

        self.cur.execute("drop table if exists last_reported_version")
        self.cur.execute("""
            create table last_reported_version (
                program_id,
                reported_program_row_id,
                report_date,
                FOREIGN KEY(reported_program_row_id) REFERENCES reported_program(id)
            )
        """)
        self.cur.execute("""
            insert into last_reported_version (program_id, reported_program_row_id, report_date)
                select distinct
                    program_id,
                    last_value(id) over (
                        partition by program_id
                        order by report_date, id
                        range between unbounded preceding
                        and unbounded following
                    ) as last_id,
                    last_value(report_date) over (
                        partition by program_id order by report_date, id
                        range between unbounded preceding
                        and unbounded following
                    ) as last_report_date
                from
                    reported_program
                order by program_id asc
        """)
        self.con.commit()

        logger.info("Generating last_reported_version table from reported_program table...OK")

    def _populate_first_reported_table(self):
        """Populates first_reported_version table with reported info
        to contain only the first appearance of a program among all reports.
        """

        logger.info("Generating first_reported_version table from reported_program table...")

        self.cur.execute("drop table if exists first_reported_version")
        self.cur.execute("""
            create table first_reported_version (
                program_id,
                reported_program_row_id,
                report_date,
                FOREIGN KEY(reported_program_row_id) REFERENCES reported_program(id)
            )
        """)
        self.cur.execute("""
            insert into first_reported_version (program_id, reported_program_row_id, report_date)
                select distinct
                    program_id,
                    first_value(id) over (
                        partition by program_id
                        order by report_date, id
                        range between unbounded preceding
                        and unbounded following
                    ) as first_id,
                    first_value(report_date) over (
                        partition by program_id
                        order by report_date, id
                        range between unbounded preceding
                        and unbounded following
                    ) as first_report_date
                from
                    reported_program
                order by program_id asc
        """)
        self.con.commit()

        logger.info("Generating first_reported_version table from reported_program table...OK")
        
    def _print_execution_plan(self, name: str, sql: str):
        rows = []
        indent_levels = {}

        for node_id, parent_id, _, detail in self.cur.execute("explain query plan {}".format(sql)):
            indent_level = 0 if parent_id not in indent_levels else indent_levels[parent_id] + 1
            indent_levels[node_id] = indent_level
            rows.append("   " * indent_level + detail)

        logger.info(f"*** Execution plan for {name}: {'\n'.join(rows)}")

    @ntfy()
    def generate_diff_reports(self):
        max_cues_per_program = next(self.cur.execute("""
            select max(cue_count)
            from
              (select count(1) as cue_count
               from production_mw_info
               group by program_id

               union select count(1) as cue_count
               from reported_mw_info
               group by reported_program_row_id)
        """))[0] + 1

        logger.info(f"*** Generating reports with {max_cues_per_program} max queues per program ***")

        for report_name, columns, query in DIFF_REPORT_SQL_QUERIES:
            query = query.format(max_cues_per_program)

            self._print_execution_plan(report_name, query)

            start = time.time()
            res = self.cur.execute(query)

            report_file = self.config.diff_reports / report_name
            report_file.touch(exist_ok=True)

            with report_file.open(mode="wt") as f:
                writer = csv.writer(f)
                writer.writerow(columns)

                while row_values := res.fetchone():
                    writer.writerow([v or "" for v in row_values])

            end = time.time()

            logger.info(f"*** Generated report {report_name} in {end - start} seconds ***")


@ntfy()
def handle_reports_download(config: Config):
    do_download_reports = False
    config.reports_dir.mkdir(exist_ok=True)

    if (existing_files_in_report_dir := len([_ for _ in config.reports_dir.iterdir()])) == 0:
        do_download_reports = True
    elif input(
        f"There are {existing_files_in_report_dir} files in report dir. "
        "Do you want to download reports? [y/N]: "
    ).strip() == "y":
        do_download_reports = True

    if not do_download_reports:
        return

    query = {"namespace": {"$in": config.report_namespaces}}

    fs = FileSystem(db_uri=config.bazaar_mongo_uri, storage_uri=config.bazaar_storage_uri)
    total_files_to_download = fs.db.count_documents(query)

    logger.info(f"Downloading {total_files_to_download} files... Will send a NTFY message when done.")

    @ntfy(notify_if_ok=False)
    def download_file(file: dict[str, Any], filename: str):
        with fs.open(
            file["name"],
            "r",
            namespace=file["namespace"]
        ) as in_file, (
            config.reports_dir  / filename
        ).open("w") as out_file:
            out_file.write(in_file.read())

    for file in tqdm(fs.db.find(query), total=total_files_to_download):
        filename: str = file["name"].split("/")[-1]

        try:
            download_file(file, filename)
        except Exception as e:
            logger.error(e, extra={"info": json.dumps({"filename": filename})})


def main():
    load_dotenv()
    config = Config()
    sqlite_man = SQLiteDBManager(config)

    logger.info("### START ###")

    # if input("Download reports from S3? [y/N]: ") == "y":
    #     handle_reports_download(config)

    if input("Populate local db with REPORTS data? [y/N]: ") == "y":
        sqlite_man.ingest_reports()
            
    if input("Populate local db with PRODUCTION data? [y/N]: ") == "y":
        sqlite_man.ingest_prod_db()

    if input("Vacuum? [y/N]: ") == "y":
        sqlite_man.vacuum()

    # if input("Generate diff reports? [y/N]: ") == "y":
    #     sqlite_man.generate_diff_reports()

    logger.info("### END ###")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    main()
