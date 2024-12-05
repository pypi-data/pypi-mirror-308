import base64
import csv
from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import Schedule
from tqdm import tqdm
import pytz
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Union


class Settings(BaseSettings):
    mongo_uri: str = Field(..., alias="MONGO_URI")
    build_number: str = Field(..., alias="BUILD_NUMBER")
    input_start_time: datetime = Field(..., alias="PERIOD_START_TIME")
    input_end_time: datetime = Field(..., alias="PERIOD_END_TIME")


HEADERS = (
    "channel",
    "program_title",
    "program_id",
    "unique_id",
    "client_id",
    "program_url",
    "broadcast_start_time",
    "last_edited_time",
    "last_approved_time",
    "last_reported_time",
)
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
OUTPUT_FILE_DATE_FORMAT = "%Y-%m-%d"
user_timezone = pytz.timezone("Europe/Helsinki")


def generate_output_filename(start_time: datetime, end_time: datetime, build: str) -> str:
    start_time_str = start_time.strftime(OUTPUT_FILE_DATE_FORMAT)
    end_time_str = end_time.strftime(OUTPUT_FILE_DATE_FORMAT)
    filename = f"YLE_reported-but-unapproved_{start_time_str}_{end_time_str}_build-{build}.csv"
    return filename


def url_constructor(schedule_id) -> str:
    def is_valid_object_id(oid) -> bool:
        try:
            if isinstance(oid, ObjectId):
                return True
            else:
                ObjectId(str(oid))
                return True
        except (InvalidId, TypeError, ValueError):
            return False

    if not is_valid_object_id(schedule_id):
        return "-"

    raw_schedule_string = f"Schedule:{schedule_id}"
    return base64.b64encode(raw_schedule_string.encode()).decode("utf-8")


class ReportedButUnapproved:
    def __init__(self, config: Union[Settings, BaseSettings]):
        self.config = config
        self.base_url = "https://yle-reportal.bmat.com/programs/view/"
        self.build_number = self.config.build_number
        self.start_time = self.config.input_start_time
        self.end_time = self.config.input_end_time
        self.filename = generate_output_filename(self.start_time, self.end_time, self.build_number)
        self.pipeline = [
            {"$match": {"start_time": {"$gte": self.start_time, "$lt": self.end_time}}},
            {"$match": {"$and": [{"reported": True}, {"aggregations.approved": False}]}},
            {"$lookup": {"from": "av_work", "localField": "av_work", "foreignField": "_id", "as": "_av_work"}},
            {"$unwind": "$_av_work"},
            {"$lookup": {"from": "channel", "localField": "channel", "foreignField": "_id", "as": "_channel"}},
            {"$unwind": "$_channel"},
            {
                "$project": {
                    "_id": 1,
                    "channel_display_name": "$_channel.display_name",
                    "program_title": "$_av_work.titles.original_title",
                    "alt_title": "$_av_work.titles.full_name",
                    "program_id": "$_av_work._id",
                    "unique_id": "$_av_work.work_ids.yle_numerical_id",
                    "client_id": "$_av_work.work_ids.plasma_id",
                    "broadcast_start_time": "$start_time",
                    "last_edited_time": "$_av_work.history_info.last_editor.updated_at",
                    "last_approved_time": "$_av_work.history_info.approved_change.updated_at",
                    "last_reported_time": "$_av_work.history_info.reported_change.updated_at",
                }
            },
        ]

    def generator(self):
        connect(host=self.config.mongo_uri)

        matching_schedules = list(Schedule.objects.aggregate(*self.pipeline, allowDiskUse=True))
        self.write_output_csv(matching_schedules)

    def write_output_csv(self, matching_schedules: list):
        with open(self.filename, "w", encoding="utf-8", newline="") as out_file:
            csv_writer = csv.DictWriter(out_file, fieldnames=HEADERS)
            csv_writer.writeheader()

            for match in tqdm(matching_schedules, total=len(matching_schedules)):
                sch_ui_id = url_constructor(match["_id"])

                csv_writer.writerow(
                    {
                        "channel": (match["channel_display_name"] if "channel_display_name" in match and match["channel_display_name"] != "" else "-"),
                        "program_title": (
                            match["program_title"]
                            if "program_title" in match and match["program_title"] != ""
                            else match["alt_title"]
                            if "alt_title" in match and match["alt_title"] != ""
                            else "-"
                        ),
                        "program_id": (str(match["program_id"]) if "program_id" in match and str(match["program_id"]) != "" else "-"),
                        "unique_id": match["unique_id"] if "unique_id" in match and match["unique_id"] != "" else "-",
                        "client_id": match["client_id"] if "client_id" in match and match["client_id"] != "" else "-",
                        "program_url": str(self.base_url + sch_ui_id),
                        "broadcast_start_time": (
                            user_timezone.localize(match["broadcast_start_time"]).strftime("%d/%m/%Y %H:%M:%S")
                            if "broadcast_start_time" in match and isinstance(match["broadcast_start_time"], datetime)
                            else "-"
                        ),
                        "last_edited_time": (
                            user_timezone.localize(match["last_edited_time"]).strftime("%d/%m/%Y %H:%M:%S")
                            if "last_edited_time" in match and isinstance(match["last_edited_time"], datetime)
                            else "-"
                        ),
                        "last_approved_time": (
                            user_timezone.localize(match["last_approved_time"]).strftime("%d/%m/%Y %H:%M:%S")
                            if "last_approved_time" in match and isinstance(match["last_approved_time"], datetime)
                            else "-"
                        ),
                        "last_reported_time": (
                            user_timezone.localize(match["last_reported_time"]).strftime("%d/%m/%Y %H:%M:%S")
                            if "last_reported_time" in match and isinstance(match["last_reported_time"], datetime)
                            else "-"
                        ),
                    }
                )


def load_env_variables():
    load_dotenv(".env")


if __name__ == "__main__":
    load_env_variables()
    reported_but_unapproved = ReportedButUnapproved(config=Settings())
    reported_but_unapproved.generator()
