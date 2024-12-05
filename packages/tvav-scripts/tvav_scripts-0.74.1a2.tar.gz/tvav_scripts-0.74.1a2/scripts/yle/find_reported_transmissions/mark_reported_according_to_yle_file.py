import csv
import json
import os
from datetime import datetime, timedelta
from functools import lru_cache

import pytz
from bmat_mongoengine_history import HistoryInfoItem
from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, Channel, Report, Schedule


PRIMARY_RADIO_CHANNELS = ["r01", "r02", "r03", "r04", "r44", "r48"]


def main():
    helsinki_timezone = pytz.timezone("Europe/Helsinki")
    with open(os.getenv("YLE_REPORTED_FILENAME", "r")) as in_file:
        reported_data = csv.DictReader(in_file, delimiter=";")
        # Skip headers
        next(reported_data)
        for row in reported_data:
            channel_short_name = row["<kanava>"]
            yle_numerical_id = row["\ufeff<rapnro>"]
            start_date = row["<julk_pvm_a>"]
            start_time = row["<aklo>"]
            title = row["<nimi>"]
            radioman_programme_id = row["<car_ohjelma_id>"]
            start_datetime = helsinki_timezone.localize(datetime.strptime(f"{start_date} {start_time}", "%Y%m%d %H%M")).astimezone(pytz.UTC)
            channel = get_channel(channel_short_name)
            av_works = get_av_works(yle_numerical_id, title, radioman_programme_id)
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
                    # For some unknown reason, there are some programs for the exact same start time... Duplicates?
                    reportal_schedules = Schedule.objects(
                        channel=channel,
                        start_time__gte=start_datetime - timedelta(seconds=10),
                        start_time__lte=start_datetime + timedelta(seconds=10),
                        av_work__in=av_works
                    )
                    for reportal_schedule in reportal_schedules:
                        mark_schedule_as_reported(reportal_schedule, row)
                    continue
            mark_schedule_as_reported(reportal_schedule, row)

def mark_schedule_as_reported(reportal_schedule, row):
    reportal_schedule.av_work.reported = True
    if not reportal_schedule.av_work.history_info.reported_change:
        reportal_schedule.av_work.history_info.reported_change = HistoryInfoItem(
            who=ObjectId("5f86edf216382eb7b8d7be33"),
            who_name="bmat_processor",
            updated_at=datetime.strptime(row["<ajopvm>"], "%Y%m%d")
        )
    elif not reportal_schedule.av_work.history_info.reported_change.updated_at:
        reportal_schedule.av_work.history_info.reported_change.updated_at = datetime.strptime(row["<ajopvm>"], "%Y%m%d")
    reportal_schedule.av_work.save()
    reportal_schedule.reported = True
    reportal_schedule.save()
    if is_main_radio_channel_broadcast(schedule=reportal_schedule):
        # Register the Shared Schedules first hence the `channel__ne=schedule.channel`
        # Later the actual `schedule` gets registered
        for shared_schedule in Schedule.objects(
                av_work=reportal_schedule.av_work.id,
                start_time=reportal_schedule.start_time,
                channel__ne=reportal_schedule.channel
        ):
            # Only Mark as `reported` if the parallel transmissions are happening in the regional channels
            if not is_main_radio_channel_broadcast(schedule=shared_schedule):
                shared_schedule.reported = True
                shared_schedule.save()
    else:
        # YLE-1916 - Additional Feedback
        # When a program is reported for the regional channel, all parallel transmissions in regional channels should be marked as reported.
        for shared_schedule in Schedule.objects(
                av_work=reportal_schedule.av_work.id,
                start_time=reportal_schedule.start_time,
                channel__ne=reportal_schedule.channel
        ):
            # Only Mark as `reported` if the parallel transmissions are happening in the regional channels
            if not is_main_radio_channel_broadcast(schedule=shared_schedule):
                shared_schedule.reported = True
                shared_schedule.save()


def is_main_radio_channel_broadcast(schedule: Schedule):
    return schedule.channel.short_name in PRIMARY_RADIO_CHANNELS


@lru_cache
def get_channel(short_name: str) -> Channel:
    return Channel.objects.get(short_name=short_name)


@lru_cache
def get_av_works(yle_numerical_id: str, title: str, radioman_programme_id: str) -> AvWork:
    av_works = AvWork.objects(work_ids__yle_numerical_id=yle_numerical_id)
    if av_works.count() == 0:
        av_works = AvWork.objects(work_ids__radioman_programme_id=int(radioman_programme_id), titles__original_title=title)
    return av_works


if __name__ == "__main__":
    load_dotenv()
    connect(host=os.getenv("MONGO_URI"))
    main()
