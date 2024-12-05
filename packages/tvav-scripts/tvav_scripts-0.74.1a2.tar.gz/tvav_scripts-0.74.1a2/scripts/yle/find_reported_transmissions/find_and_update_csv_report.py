import csv
import os
import pytz

from bazaar import FileSystem
from datetime import datetime
from defusedxml.ElementTree import fromstring
from dotenv import load_dotenv
from itertools import filterfalse
from mongoengine import connect
from pydantic.fields import Field
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional, List, Iterable
from xml.etree.ElementTree import Element

from reportal_model import AvWork, Schedule

from scripts.utils.file_operations import CSVDictUpdater, download_bazaar_files
from scripts.utils.slack_notifier import ClassWithSlackLogger

helsinki_timezone = pytz.timezone("Europe/Helsinki")


class YLEReport(BaseModel):
    filename: str
    channel_sender_id: str = None
    start_time: datetime = None
    end_time: datetime = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        filename_split = self.filename.rstrip(".xml").split("_")

        self.channel_sender_id = filename_split[1]
        self.start_time = datetime.strptime(filename_split[2], "%Y%m%d%H%M%S")
        self.end_time = datetime.strptime(filename_split[3], "%Y%m%d%H%M%S")


class YLEReportGuesser(BaseModel):
    reports: list[YLEReport] = Field(default_factory=list)

    def guess_report_candidates_for_schedule(self, schedule: Schedule) -> List[str]:
        """Returns a list of report filenames that could contain the specified Schedule.

        The list of reports is ordered by most recent first.

        It uses the Channel and start_time to determine the best candidates among all possible reports.
        """
        candidates = filterfalse(
            lambda x: not (
                x.channel_sender_id == schedule.sender_id
                and schedule["start_time"] < x.end_time
            ),
            self.reports
        )
        candidates = sorted(candidates, key=lambda x: x.end_time, reverse=True)
        return [report.filename for report in candidates]

    def delete_2022(self):
        self.reports = [
            report
            for report in self.reports
            if report.end_time > datetime(2023, 4, 1)
        ]


class YLEFDUpdateCSVReport(ClassWithSlackLogger):
    """Class that takes a CSV report and updates it with data from YLE's
    gramex-teosto-combined reports.

    This class expects the reports to exist in the report_dir specified as a relative path.

    The CSV report needs to contain the following columns:
    - Report filename
    - Channel
    - Total music duration in the reports
    - Total music duration in the UI
    - Discrepancy with report?
    - Program ID

    """
    yle_report_guesser: YLEReportGuesser

    def __init__(self, filename: str):
        load_dotenv()
        super().__init__()
        self.filename = filename

        connect(host=os.getenv("MONGO_URI"))
        self.mongo_bazaar = MongoClient(os.getenv("BAZAAR_MONGO_URI")).get_database()
        self.fs = FileSystem(db_uri=os.getenv("BAZAAR_MONGO_URI"), storage_uri=os.getenv("BAZAAR_STORAGE_URI"))

        self._init_yle_report_guesser()

    def _init_yle_report_guesser(self):
        guesser = YLEReportGuesser()
        for report_filename in self._get_yle_fortnightly_reports_filenames():
            rf = YLEReport(filename=report_filename)
            guesser.reports.append(rf)
        self.yle_report_guesser = guesser
        self.yle_report_guesser.delete_2022()

    def _get_yle_fortnightly_reports_filenames(self) -> Iterable[str]:
        """Get all report filenames in yle-reports-fortnightly."""
        # report_filenames = os.listdir(self.report_dir)
        report_filenames = self.mongo_bazaar.file.distinct("name", {
            "namespace": "yle-reports-fortnightly",
        })
        return report_filenames

    @staticmethod
    def _get_db_total_music_duration(schedule: Schedule = None) -> int:
        """Returns the sum of all rounded cues durations.
        It is the sum of the rounded cue durations because the report contains only rounded cue durations,
        we need to check that the sum in the report matches the sum in the DB.
        """
        return sum([
            round(cue.duration)
            for cue in schedule.av_work.cuesheet.cues
            if schedule.av_work.cuesheet and schedule.av_work.cuesheet.cues
        ])

    def _get_schedule_from_report(self, schedule: Schedule, report_candidate: str) -> Optional[Element]:
        if report_candidate.lstrip("/") in os.listdir("./reports/"):
            with open(f"reports{report_candidate}", mode="r") as in_file:
                xml_content = in_file.read()
        else:
            with self.fs.open(
                report_candidate, "r", namespace="yle-reports-fortnightly",
            ) as in_file:
                xml_content = in_file.read()

        xml = fromstring(xml_content)

        for transmission in xml.findall("ohjelma_esitys"):
            yle_numerical_id = transmission.find("rapnro").text
            if yle_numerical_id != schedule.av_work.work_ids.get("yle_numerical_id"):
                continue

            plasma_id = transmission.find("plasma_ohjelma_id").text or ""
            radioman_programme_id = transmission.find("car_ohjelma_id").text or ""

            tv_match = plasma_id == schedule.av_work.work_ids.get("plasma_id")
            radio_match = radioman_programme_id == str(schedule.av_work.work_ids.get("radioman_programme_id"))

            if not tv_match and not radio_match:
                continue

            start_date = transmission.find("julk_pvm_a").text
            start_time = transmission.find("aklo").text
            start_datetime = helsinki_timezone.localize(
                datetime.strptime(f"{start_date} {start_time}", "%Y%m%d %H%M")
            ).astimezone(pytz.UTC)

            try:
                start_time_does_not_match = abs(start_datetime - pytz.utc.localize(schedule.start_time)).seconds > 60
            except ValueError as e:
                import ipdb; ipdb.set_trace()
                raise e
            if start_time_does_not_match:
                continue

            return transmission

    @staticmethod
    def _get_report_total_music_duration(reported_schedule: Element) -> int:
        """Extracts cue durations and calculates the sum.

        Cue durations are stored in MMMSS format (like 00110 would be 01:10) in:
        `program.cues[].works.work.music_work_identifiers.kesto`

        Where:

        - cues = "aanite"
        - works = "teokset"
        - work = "teos"
        - music_work_identifiers = "aanite_teos"
        - kesto = "kesto"
        """
        total_music_duration = 0
        cues = reported_schedule.findall("aanite")
        for cue in cues:
            works = cue.find("teokset")
            work = works.find("teos")
            music_work_identifiers = work.find("aanite_teos")
            cue_duration = music_work_identifiers.find("kesto").text
            if cue_duration:
                cue_duration = int(cue_duration[:3]) * 60 + int(cue_duration[3:])
                total_music_duration += cue_duration
        return total_music_duration

    @staticmethod
    def _get_discrepancy_with_report(schedule: Schedule, reported_schedule: Element) -> Optional[str]:
        """Tries to find discrepancies between report and DB.

        If it finds any, will return a str with more data.
        """
        reported_cues = reported_schedule.findall("aanite")
        db_cues = schedule.av_work.cuesheet.cues

        reported_length = len(reported_cues)
        db_length = len(db_cues)

        if reported_length != db_length:
            return f"Cuesheet length does not match\nReport: {reported_length} vs DB: {db_length}"

        db_titles = [
            cue.music_work.title.replace("\n", ". ").replace("\r", ". ")
            for cue in db_cues
            if cue.music_work
        ]

        db_isrcs = [
            cue.music_work.work_ids.get("isrc")
            for cue in db_cues
            if cue.music_work
        ]

        for reported_cue in reported_cues:
            works = reported_cue.find("teokset")
            work = works.find("teos")

            reported_title = work.find("teos_nimi").text
            if reported_title and reported_title not in db_titles:
                return f"MusicWork TITLE {reported_title} not found in DB"

            reported_isrc = work.find("isrc").text
            if reported_isrc and reported_isrc not in db_isrcs:
                return f"MusicWork ISRC {reported_isrc} not found in DB"

    def run(self):
        REPORT_HEADERS = [
            "Program ID",
            "Report filename",
            "Channel",
            "Total music duration in the reports",
            "Total music duration in the UI",
            "Discrepancy with report?",
        ]

        plasma_ids = self._get_plasma_ids_from_init_report()
        schedules_by_plasma_id = Schedule.objects(
            av_work__in=AvWork.objects(
                work_ids__plasma_id__in=plasma_ids,
            )
        )

        with open(
            "output_report.csv", mode="wt"
        ) as out_file:
            writer = csv.DictWriter(out_file, fieldnames=REPORT_HEADERS)
            writer.writeheader()

        plasma_ids_unique = set()
        for schedule in self.tqdm(schedules_by_plasma_id, total=schedules_by_plasma_id.count()):
            plasma_id = schedule.av_work.work_ids.get("plasma_id")
            plasma_id_already_reported = plasma_id in plasma_ids_unique

            if plasma_id_already_reported:
                continue

            row = {
                "Program ID": plasma_id,
                "Total music duration in the UI": self._get_db_total_music_duration(schedule)
            }

            report_candidates = self.yle_report_guesser.guess_report_candidates_for_schedule(schedule)
            self.logger.debug("Found %d report_candidates for Schedule:%s", len(report_candidates), str(schedule.id))

            if not report_candidates:
                continue

            # We may have multiple candidates
            for report_candidate in report_candidates:
                reported_schedule = self._get_schedule_from_report(schedule, report_candidate)

                if not reported_schedule:
                    continue

                self.logger.debug("Schedule found in report!")

                row["Report filename"] = report_candidate
                row["Channel"] = schedule.channel.display_name
                row["Total music duration in the reports"] = self._get_report_total_music_duration(reported_schedule)
                row["Discrepancy with report?"] = self._get_discrepancy_with_report(schedule, reported_schedule)

                with open(
                    "output_report.csv", mode="at"
                ) as out_file:
                    writer = csv.DictWriter(out_file, fieldnames=REPORT_HEADERS)
                    writer.writeheader()
                    writer.writerow(row)

                plasma_ids_unique.add(plasma_id)
                break

    def _get_plasma_ids_from_init_report(self) -> list[str]:
        plasma_ids = []
        with open(self.filename, mode="rt") as file:
            reader = csv.DictReader(file)
            for row in reader:
                plasma_ids.append(row.get("Program ID"))

        return plasma_ids


if __name__ == "__main__":
    FILENAME = "OVERWRITTEN_CUESHEETS.csv"
    load_dotenv()

    # download_bazaar_files(
    #     db_uri=os.getenv("BAZAAR_MONGO_URI"),
    #     storage_uri=os.getenv("BAZAAR_STORAGE_URI"),
    #     query={"namespace": "yle-reports-fortnightly"},
    #     output_dir="./reports"
    # )

    script = YLEFDUpdateCSVReport(
        filename=FILENAME,
    )
    script.run()
