from __future__ import annotations

import dataclasses
import enum
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Iterable, Optional

from celery import Celery
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


load_dotenv()


class ReportType(enum.Enum):
    MONTHLY = "monthly_online"
    DAILY_TV = "daily_tv"
    DAILY_RADIO = "daily_radio"
    DAILY_PODCAST = "daily_podcast"
    DAILY_VOD = "daily_vod"

    @classmethod
    def values(cls):
        return {t.value for t in cls}


@dataclasses.dataclass
class ReportOptions:
    report_type: ReportType
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    channel_id: Optional[str] = None

    @classmethod
    def for_monthly_online(cls, month: int, year: Optional[int] = None, channel_id: Optional[str] = None) -> ReportOptions:
        current_date = datetime.utcnow()
        start_time, end_time = cls.get_time_range_for_month(month or current_date.month, year or current_date.year)
        return cls(report_type=ReportType.MONTHLY, start_time=start_time, end_time=end_time, channel_id=channel_id)

    @staticmethod
    def get_time_range_for_month(month: int, year: int) -> (datetime, datetime):
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        return datetime(year, month, day=1), datetime(next_year, next_month, day=1)

    @classmethod
    def for_daily_tv(cls, day: datetime, channel_id: Optional[str] = None) -> ReportOptions:
        return cls(report_type=ReportType.DAILY_TV, start_time=day, end_time=day + timedelta(days=1), channel_id=channel_id)

    @classmethod
    def for_daily_radio(cls, day: datetime, channel_id: Optional[str] = None) -> ReportOptions:
        return cls(report_type=ReportType.DAILY_RADIO, start_time=day, end_time=day + timedelta(days=1), channel_id=channel_id)

    @classmethod
    def for_daily_vod(cls, day: datetime, channel_id: Optional[str] = None) -> ReportOptions:
        return cls(report_type=ReportType.DAILY_VOD, start_time=None, end_time=day + timedelta(days=1), channel_id=channel_id)

    @classmethod
    def for_daily_podcast(cls, day: datetime, channel_id: Optional[str] = None) -> ReportOptions:
        return cls(report_type=ReportType.DAILY_PODCAST, start_time=None, end_time=day + timedelta(days=1), channel_id=channel_id)

    def to_params(self, datetime_format: str):
        return {
            'start_time': self.start_time.strftime(datetime_format) if self.start_time else None,
            'end_time': self.end_time.strftime(datetime_format) if self.end_time else None,
            'default_report_type': self.report_type.value,
            'channel_id': self.channel_id
        }


class ReportGenerator:
    def __init__(self):
        self.datetime_format = os.getenv("DATETIME_FORMAT", "%Y-%m-%dT%H:%M:%S")
        self.start_time = datetime.strptime(os.getenv("START_TIME"), self.datetime_format)
        self.end_time = datetime.strptime(os.getenv("END_TIME"), self.datetime_format)

        self.report_type = os.getenv("REPORT_TYPE", "daily_tv")
        if self.report_type not in ReportType.values():
            raise ValueError(f"Report type '{self.report_type}' is not valid")
        if self.report_type == ReportType.MONTHLY.value:
            if self.start_time.day != 1:
                logger.warning(f"Requested monthly report. Date info from provided start time: {self.start_time}, will be ignored and replaced with day 01.")
                self.start_time = self.start_time.replace(day=1)
            if self.end_time is not None:
                logger.warning(
                    f"Requested monthly report. Day from provided end time: {self.end_time}, will be ignored. Month and year will be used."
                )

        self.channel_id = os.getenv("CHANNEL_ID") or None

        self.sleep_time_between_tasks = int(os.getenv("SLEEP_TIME_BETWEEN_TASKS", "3"))

        self.celery_broker = os.getenv("CELERY_BROKER")
        self.reports_queue = os.getenv("REPORTS_QUEUE")
        self.app = Celery(broker=self.celery_broker)

    def generate_reports(self):
        for start_time, end_time in self.iter_dates_for_reports():
            if self.report_type == ReportType.MONTHLY.value:
                report_options = ReportOptions.for_monthly_online(start_time.month, start_time.year, channel_id=self.channel_id)
            elif self.report_type == ReportType.DAILY_TV.value:
                report_options = ReportOptions.for_daily_tv(start_time, channel_id=self.channel_id)
            elif self.report_type == ReportType.DAILY_RADIO.value:
                report_options = ReportOptions.for_daily_radio(start_time, channel_id=self.channel_id)
            elif self.report_type == ReportType.DAILY_PODCAST.value:
                report_options = ReportOptions.for_daily_podcast(start_time, channel_id=self.channel_id)
            elif self.report_type == ReportType.DAILY_VOD.value:
                report_options = ReportOptions.for_daily_vod(start_time, channel_id=self.channel_id)
            else:
                logger.error(f"Report type {self.report_type} is invalid. Should have failed on __init__. This code should be unreachable!")
                sys.exit(1)
            logger.info(f"Generating report for {start_time} - {end_time} with type {self.report_type}")
            self.app.signature("generate_default_report", kwargs=report_options.to_params(self.datetime_format)).apply_async(queue=self.reports_queue)
            time.sleep(self.sleep_time_between_tasks)

    def iter_dates_for_reports(self) -> Iterable[tuple[datetime, datetime]]:
        return _DateRangeIterator(self.start_time, self.end_time, self.report_type)


class _DateRangeIterator:
    def __init__(self, start_time: datetime, end_time: datetime, report_type: str):
        self.start_time = start_time
        self.end_time = end_time
        self._get_next_datetime = self._add_a_month if report_type == ReportType.MONTHLY.value else self._add_a_day
        self.current_dates = (self.start_time, self.start_time)

    @staticmethod
    def _add_a_month(start_time: datetime) -> datetime:
        return start_time + relativedelta(months=1)

    @staticmethod
    def _add_a_day(start_time: datetime) -> datetime:
        return start_time + timedelta(days=1)

    def __iter__(self) -> Iterable[tuple[datetime, datetime]]:
        return self

    def __next__(self) -> tuple[datetime, datetime]:
        if self.current_dates[1] >= self.end_time:
            raise StopIteration
        self.current_dates = (self.current_dates[1], self._get_next_datetime(self.current_dates[1]))
        return self.current_dates


if __name__ == "__main__":
    ReportGenerator().generate_reports()
