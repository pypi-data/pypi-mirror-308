import json
import os
from datetime import timedelta, datetime
from functools import lru_cache

import pytz
from bazaar import FileSystem
from defusedxml.ElementTree import parse
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, Channel, Schedule


REPORT_NAME_REGEX = "20231101"


def main():
    NAMESPACE = os.getenv("NAMESPACE")
    fs = FileSystem(db_uri=os.getenv("BAZAAR_MONGO_URI"), storage_uri=os.getenv("BAZAAR_STORAGE_URI"))
    files = fs.db.find({"namespace": NAMESPACE, "name": {"$regex": REPORT_NAME_REGEX}})
    reported = {}
    helsinki_timezone = pytz.timezone("Europe/Helsinki")
    for file in files:
        reported[file["name"]] = []
        with fs.open(file["name"], "r", namespace=NAMESPACE) as in_file:
            xml = parse(in_file)
        for schedule in xml.findall("ohjelma_esitys"):
            channel_short_name = schedule.find("kanava").text
            yle_numerical_id = schedule.find("rapnro").text
            start_date = schedule.find("julk_pvm_a").text
            start_time = schedule.find("aklo").text
            start_datetime = helsinki_timezone.localize(datetime.strptime(f"{start_date} {start_time}", "%Y%m%d %H%M")).astimezone(pytz.UTC)
            channel = get_channel(channel_short_name)
            av_works = get_av_works(yle_numerical_id)
            try:
              reportal_schedule = Schedule.objects.get(
                channel=channel,
                start_time__gte=start_datetime - timedelta(minutes=1),
                start_time__lte=start_datetime + timedelta(minutes=1),
                av_work__in=av_works
              )
            except Exception:
                # It might be that some schedules are closer in start/end than the minute threshold, and we still need to get only one.
                try:
                  reportal_schedule = Schedule.objects.get(
                    channel=channel,
                    start_time__gte=start_datetime - timedelta(seconds=10),
                    start_time__lte=start_datetime + timedelta(seconds=10),
                    av_work__in=av_works
                  )
                except Exception:
                    # For some unknown reason, there are some programs for the exact same start time (but different end). Try to catch them by broadcast_id
                    broadcast_id = schedule.find("plasma_lahetys_id").text
                    reportal_schedule = Schedule.objects.get(
                        channel=channel,
                        start_time__gte=start_datetime - timedelta(seconds=10),
                        start_time__lte=start_datetime + timedelta(seconds=10),
                        av_work__in=av_works,
                        schedule_ids__broadcast_id=broadcast_id
                    )
            reported[file["name"]].append(str(reportal_schedule.id))
    with open("FOUND_TRANSMISSIONS.json", "w") as out_file:
        json.dump(reported, out_file, indent=4)


@lru_cache
def get_channel(short_name: str) -> Channel:
    return Channel.objects.get(short_name=short_name)


@lru_cache
def get_av_works(yle_numerical_id: str) -> AvWork:
    return AvWork.objects(work_ids__yle_numerical_id=yle_numerical_id)


if __name__ == "__main__":
    load_dotenv()
    connect(host=os.getenv("MONGO_URI"))
    main()
