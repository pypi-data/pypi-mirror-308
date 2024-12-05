import logging
import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import Schedule
from tqdm import tqdm


logger = logging.getLogger(__name__)


def parse_args() -> tuple[Optional[datetime], Optional[datetime]]:
    datetime_format = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")
    start_time = os.getenv("START_TIME")
    end_time = os.getenv("END_TIME")
    start_time = datetime.strptime(start_time, datetime_format) if start_time else None
    end_time = datetime.strptime(end_time, datetime_format) if end_time else None
    return start_time, end_time


def correct_schedule_start_greater_than_end(start_time: Optional[datetime], end_time: Optional[datetime]):
    query = {"$expr": {"$or": [{"$gt": ["$start_time", "$end_time"]}, {"$gt": ["$parts.start_time", "$parts.end_time"]}]}}
    if start_time:
        query["start_time"] = {"$gte": start_time}
    if end_time:
        query["start_time"] = query.get("start_time", {})
        query["start_time"]["$lt"] = end_time

    schedules = Schedule.objects(__raw__=query)
    logger.info(f"Fixing {schedules.count()} schedules.")
    for schedule in tqdm(schedules):
        if schedule.end_time < schedule.start_time:
            schedule.end_time += timedelta(hours=1)
        for part in schedule.parts:
            if part["end_time"] < part["start_time"]:
                part["end_time"] += timedelta(hours=1)
        schedule.save()


if __name__ == '__main__':
    load_dotenv()
    connect(host=os.getenv("MONGO_URI"))
    start, end = parse_args()
    correct_schedule_start_greater_than_end(start, end)
