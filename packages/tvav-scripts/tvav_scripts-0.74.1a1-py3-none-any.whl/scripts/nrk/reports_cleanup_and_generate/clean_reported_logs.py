import os
import re
import time
from datetime import datetime
from typing import List

from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from reportal_model import AvWork, DigitalUsage, Report, Schedule

load_dotenv()


class ReportedCleaner:
    def __init__(self):
        self.timezone = os.getenv("TIMEZONE", "UTC")
        os.environ["TZ"] = self.timezone
        time.tzset()
        self.valid_cleanup_types = ("date", "ids", "filename")
        self.mongo_uri = os.getenv("MONGO_URI")
        disconnect()
        connect(host=self.mongo_uri)
        self.datetime_format = os.getenv("DATETIME_FORMAT", "%Y-%m-%dT%H:%M:%S")
        clean_logs_from_day_str = os.getenv("CLEAN_LOGS_FROM_DAY", None)
        self.clean_logs_from_day = datetime.strptime(clean_logs_from_day_str, self.datetime_format) if clean_logs_from_day_str else None

    @staticmethod
    def cleanup(av_ids: List[ObjectId]):
        """
        This method updates the database to clean reported information from AvWorks, Schedules, and DigitalUsages.

        :param av_ids: A list of ObjectIds for all AvWorks that need to be cleaned.
        :return: None
        """

        # Clean AvWorks
        print("Cleaning AvWorks")
        AvWork.objects.filter(id__in=av_ids).update(
            set__reported=False,
            set__extras__cleaned_reported=True,
            unset__history_info__reported_change=True,
            unset__extras__reported_by=True,
            unset__extras__reported_daily=True,
        )
        print("AvWorks cleaned")

        # Clean Schedules
        print("Cleaning Schedules")
        Schedule.objects.filter(av_work__in=av_ids).update(
            set__reported=False,
            set__extras__cleaned_reported=True,
            unset__extras__reported_by=True,
        )
        print("Schedules cleaned")

        # Clean Digital usages
        print("Cleaning Digital usages")
        DigitalUsage.objects.filter(av_work__in=av_ids).update(
            set__reported=False,
            set__extras__cleaned_reported=True,
            unset__extras__reported_by=True,
            unset__extras__reported_daily=True,
        )
        print("Digital usages cleaned")

    def cleanup_by_date(self, start_time_to_clean: datetime, end_time_to_clean: datetime):
        """
        Clean reported information from AvWorks, Schedules, and DigitalUsages. Based on date.
        :param start_time_to_clean:
        :param end_time_to_clean:
        :return:
        """
        print("Getting all involved AvWorks")
        av_works_id = AvWork.objects.filter(
            reported=True,
            document_info__created_at__gte=start_time_to_clean,
            document_info__created_at__lt=end_time_to_clean,
        )
        schedule_av_ids_query = Schedule.objects.filter(
            reported=True,
            start_time__gte=start_time_to_clean,
            end_time__lt=end_time_to_clean
        )
        digital_usage_av_ids_query = DigitalUsage.objects.filter(
            reported=True,
            publication_start_time__gte=start_time_to_clean,
            publication_end_time__lt=end_time_to_clean
        )

        not_valid_av_ids = self.get_not_valid_av_ids(digital_usage_av_ids_query, schedule_av_ids_query)

        av_ids = list(set(schedule_av_ids_query.distinct(field="av_work")) | set(digital_usage_av_ids_query.distinct(field="av_work")) | set(av_works_id))
        av_ids = [av_work.id for av_work in av_ids if av_work.id not in not_valid_av_ids]
        print(f"Total of '{len(av_ids)}' involved AvWorks")
        self.cleanup(av_ids=av_ids)

    def get_not_valid_av_ids(self, digital_usage_av_ids_query, schedule_av_ids_query):
        """
        Get the av_work ids that we can not clean
        :param digital_usage_av_ids_query:
        :param schedule_av_ids_query:
        :return:
        """
        not_valid_av_ids = []
        if self.clean_logs_from_day:
            # Get all the schedules and digital usages reported before the clean logs from day
            for query in [schedule_av_ids_query, digital_usage_av_ids_query]:
                for entity in query:
                    if (
                        entity.report_history
                        and any([report.document_info.created_at < self.clean_logs_from_day for report in entity.report_history])
                    ):
                        not_valid_av_ids.append(entity.av_work.id)
        return not_valid_av_ids

    def cleanup_by_report_ids(self, report_ids: list):
        """
        Clean reported information from AvWorks, Schedules, and DigitalUsages. Based on a list of report ids.
        :param report_ids:
        :return:
        """
        print("Getting all involved AvWorks")
        schedule_av_ids = Schedule.objects.filter(reported=True, report_history__in=report_ids).distinct(field="av_work")
        digital_usage_av_ids = DigitalUsage.objects.filter(reported=True, report_history__in=report_ids).distinct(field="av_work")

        av_ids = list(set(schedule_av_ids) | set(digital_usage_av_ids))
        av_ids = [av_work.id for av_work in av_ids]

        print(f"Total of '{len(av_ids)}' involved AvWorks")
        self.cleanup(av_ids=av_ids)

    def cleanup_by_report_filename(self, report_regex_to_use: str):
        """
        Clean reported information from AvWorks, Schedules, and DigitalUsages. Based on a regex for reports files.

        May use it to clean for a specific date-range (which is contained in reports filename).

        :param report_regex_to_use:
        :return:
        """
        print("Getting all involved Reports")

        regex = re.compile(report_regex_to_use)
        report_ids = Report.objects.filter(extras__filename=regex)
        report_ids = [report.id for report in report_ids]

        print(f"Total of '{len(report_ids)}' involved Reports")
        self.cleanup_by_report_ids(report_ids=report_ids)

    def clean_reported_logs(self):
        """
        Get the cleanup type from the env and run the cleanup that corresponds. If not recognized the cleanup type it will raise a Value error
        :return:
        """
        cleanup_type = os.getenv("CLEANUP_TYPE", "date")
        if cleanup_type not in self.valid_cleanup_types:
            raise ValueError(f"Cleanup type '{cleanup_type}' is not valid")

        if cleanup_type == "date":
            start_time = datetime.strptime(os.getenv("START_TIME"), self.datetime_format)
            end_time = datetime.strptime(os.getenv("END_TIME"), self.datetime_format)
            print(f"Cleaning by dates: {start_time} until {end_time}")
            self.cleanup_by_date(start_time, end_time)
        elif cleanup_type == "ids":
            print("Cleaning by ids")
            report_ids = os.getenv("REPORT_IDS", "").split(",")
            self.cleanup_by_report_ids(report_ids)
        elif cleanup_type == "filename":
            report_regex = os.getenv("REPORT_REGEX")
            print(f"Cleaning by regex: {report_regex}")
            self.cleanup_by_report_filename(report_regex)


if __name__ == "__main__":
    ReportedCleaner().clean_reported_logs()
