import base64
import csv
import os
from datetime import datetime
from typing import Dict, List, Union

from dotenv import load_dotenv
from bson import ObjectId
from mongoengine import connect
from reportal_model import DigitalUsage


DATETIME_OUTPUT_FORMAT = "%d/%m/%Y %H:%M:%S"
PERFORMER_ROLES = {"main artist", "interpreter", "performer"}
HEADERS = (
    "Program Title",
    "Episode Title",
    "Publication Start Time",
    "Publication End Time",
    "Start Time",
    "End Time",
    "Program ID",
    "Music Source",
    "Track Title",
    "Track ID",
    "Duration",
    "Cue start",
    "Cue end",
    "Performer",
    "Label",
    "Music Usage",
    "Cuesheet URL"
)


class IFPIReportsGenerator:
    def __init__(self, start_time: str, end_time: str, reportal_base_url: str, output_filename: str):
        self.start_time = start_time
        self.end_time = end_time
        self.output_filename = output_filename
        self.cuesheet_url = f"{reportal_base_url}/cuesheets/view/{{}}"

    def get_cues(self):
        return DigitalUsage.objects.aggregate([
            {"$match": {"publication_start_time": {"$gte": ISODate(self.start_time), "$lt": ISODate(self.end_time)}}},
            {"$lookup": {"from": "av_work", "localField": "av_work", "foreignField": "_id", "as": "av_work"}},
            {"$unwind": "$av_work"},
            {"$unwind": "$av_work.cuesheet.cues"},
            {"$lookup": {"from": "music_work", "localField": "av_work.cuesheet.cues.music_work", "foreignField": "_id", "as": "music_work"}},
            {"$unwind": "$music_work"},
            {"$match": {"music_work.source": "Commercial"}}
        ])

    def run(self):
        with open(self.output_filename, "w+", newline="", encoding="utf-8") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=HEADERS)
            writer.writeheader()
            for du in self.get_cues():
                writer.writerow({
                    "Program Title": du["av_work"]["titles"].get("original_title") or du["av_work"]["titles"].get("full_name"),
                    "Episode Title": du["av_work"]["titles"].get("episode_title"),
                    "Publication Start Time": du["publication_start_time"].strftime(DATETIME_OUTPUT_FORMAT) if du["publication_start_time"] else None,
                    "Publication End Time": du.get("publication_end_time").strftime(DATETIME_OUTPUT_FORMAT) if du.get("publication_end_time") else None,
                    "Start Time": du["start_time"].strftime(DATETIME_OUTPUT_FORMAT) if du["start_time"] else None,
                    "End Time": du["end_time"].strftime(DATETIME_OUTPUT_FORMAT) if du["end_time"] else None,
                    "Program ID": du["work_ids"].get("program_id"),
                    "Music Source": du["music_work"]["source"],
                    "Track Title": du["music_work"]["title"],
                    "Track ID": str(du["music_work"]["_id"]),
                    "Duration": du["av_work"]["cuesheet"]["cues"]["duration"],
                    "Cue start": du["av_work"]["cuesheet"]["cues"]["relative_start_time"],
                    "Cue end": du["av_work"]["cuesheet"]["cues"]["relative_start_time"] + du["av_work"]["cuesheet"]["cues"]["duration"],
                    "Performer": self.get_performer(du["music_work"].get("contributors")) if du["music_work"].get("contributors") else None,
                    "Label": du["music_work"]["work_ids"].get("label"),
                    "Music Usage": du["av_work"]["cuesheet"]["cues"]["use"],
                    "Cuesheet URL": self.get_cuesheet_url(du["av_work"]["_id"])
                })

    def get_cuesheet_url(self, av_work_id: Union[str, ObjectId]) -> str:
        return self.cuesheet_url.format(base64.b64encode(f"AvWork:{av_work_id}".encode()).decode().replace("=", "%3D"))

    def get_performer(self, contributors: List[Dict[str, str]]) -> str:
        for contributor in contributors:
            if contributor["role"] in PERFORMER_ROLES:
                return self.format_name(contributor)
        return None

    @staticmethod
    def format_name(contributor: Dict[str, str]) -> str:
        if contributor.get("first_name") and contributor.get("last_name"):
            return f"{contributor['first_name']} {contributor['last_name']}"
        if contributor.get("first_name"):
            return contributor["first_name"]
        return contributor.get("name")

    @classmethod
    def main_run(cls):
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        connect(host=mongo_uri)
        start_time = os.getenv("START_TIME")
        end_time = os.getenv("END_TIME")
        reportal_base_url = os.getenv("REPORTAL_BASE_URL")
        output_filename = os.getenv("OUTPUT_FILENAME")
        cls(start_time, end_time, reportal_base_url, output_filename).run()


def ISODate(datetime_string: str, format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Having this specific name, I can use the same aggregate here or in Robo/Studio 3T without having to change the name XD"""
    return datetime.strptime(datetime_string, format)


if __name__ == "__main__":
    IFPIReportsGenerator.main_run()
