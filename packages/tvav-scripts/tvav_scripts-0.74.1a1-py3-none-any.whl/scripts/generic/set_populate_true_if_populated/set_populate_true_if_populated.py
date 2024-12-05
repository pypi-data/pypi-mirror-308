import base64
import os

from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, Schedule
from tqdm import tqdm

load_dotenv()


def fix_unpopulated():
    with connect(host=os.getenv("MONGO_HOST")):
        av_work_query = AvWork.objects.filter(populated=False, cuesheet__cues__0__exists=True)
        total_av_works = av_work_query.count()
        updated_av_works = []
        with open("updated_av_works.csv", "a") as updated_av_works_file:
            for av_work in tqdm(av_work_query, total=total_av_works, unit="AvWork"):
                av_work.populated = True
                av_work.extras["unpopulated_fixed"] = True
                av_work.save()
                # To avoid do a ton of queries we will save the different affected av_works to later update the schedules
                updated_av_works.append(av_work.id)

                # Write into the updated_av_works file a line
                updated_av_works_file.write(f"{av_work.id},\n")

        # To avoid failing queries for too long input we will slice the updated av works
        updated_av_works_sliced = [updated_av_works[i: i + 1000] for i in range(0, len(updated_av_works), 1000)]
        for updated_av_works_to_check in tqdm(updated_av_works_sliced, total=len(updated_av_works_sliced), unit="UpdatedAvWorkSlices"):
            schedule_query = Schedule.objects.filter(
                av_work__in=updated_av_works_to_check,
                populated=False,
            )
            total_schedules = schedule_query.count()
            with open("updated_schedules.csv", "a") as updated_schedules_file:
                for schedule in tqdm(schedule_query, total=total_schedules, unit="Schedule"):
                    schedule.populated = True
                    schedule.extras["unpopulated_fixed"] = True
                    schedule.save()
                    message_to_encode = f"Schedule:{schedule.id}"
                    updated_schedules_file.write(f"{schedule.id},{base64.b64encode(message_to_encode.encode())}\n")


if __name__ == "__main__":
    fix_unpopulated()
