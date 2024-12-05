import json
import os

from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, Channel, Report, Schedule
from typing import Dict, List


PRIMARY_RADIO_CHANNELS = ["r01", "r02", "r03", "r04", "r44", "r48"]


def main():
    with open(os.getenv("FILE_TO_CLEAN", "r")) as in_file:
        schedules_to_clean: Dict[str, List[str]] = json.load(in_file)
    schedule_ids = []
    for ids in schedules_to_clean.values():
        schedule_ids.extend(ids)
    schedules = Schedule.objects(id__in=schedule_ids)
    schedules.update(set__reported=False, set__report_history=[])
    av_ids = [a.id for a in schedules.values_list("av_work")]
    AvWork.objects(id__in=av_ids, history_info__reported_change__updated_at__gte="2023-11-01").update(unset__history_info__reported_change=1, set__reported=True)

    with open(os.getenv("FILE_TO_KEEP"), "r") as in_file:
        schedules_to_keep = json.load(in_file)
    for report_filename, schedule_ids in schedules_to_keep.items():
        report = Report.objects(extras__filename=report_filename).order_by("-id").first()
        for schedule in Schedule.objects(id__in=schedule_ids):
            schedule.reported = True
            schedule.report_history.append(report)
            schedule.report_history = list(set(schedule.report_history))
            schedule.save()
            if is_main_radio_channel_broadcast(schedule=schedule):
                # Register the Shared Schedules first hence the `channel__ne=schedule.channel`
                # Later the actual `schedule` gets registered
                for shared_schedule in Schedule.objects(
                        av_work=schedule.av_work.id,
                        start_time=schedule.start_time,
                        channel__ne=schedule.channel
                ):
                    # Only Mark as `reported` if the parallel transmissions are happening in the regional channels
                    if not is_main_radio_channel_broadcast(schedule=shared_schedule):
                        shared_schedule.reported = True
                        shared_schedule.report_history.append(report)
                        shared_schedule.report_history = list(set(schedule.report_history))
                        shared_schedule.save()
            else:
                # YLE-1916 - Additional Feedback
                # When a program is reported for the regional channel, all parallel transmissions in regional channels should be marked as reported.
                for shared_schedule in Schedule.objects(
                        av_work=schedule.av_work.id,
                        start_time=schedule.start_time,
                        channel__ne=schedule.channel
                ):
                    # Only Mark as `reported` if the parallel transmissions are happening in the regional channels
                    if not is_main_radio_channel_broadcast(schedule=shared_schedule):
                        shared_schedule.reported = True
                        shared_schedule.report_history.append(report)
                        shared_schedule.report_history = list(set(schedule.report_history))
                        shared_schedule.save()


def is_main_radio_channel_broadcast(schedule: Schedule):
    return schedule.channel.short_name in PRIMARY_RADIO_CHANNELS


if __name__ == "__main__":
    load_dotenv()
    connect(host=os.getenv("MONGO_URI"))
    main()
