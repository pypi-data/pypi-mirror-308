import base64
import csv
import logging
import os
import re
import requests
from bson import ObjectId
from dataclasses import dataclass
from dateutil.parser import parse
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint
from pymongo.synchronous.database import Database
from pathlib import Path
from pymongo.mongo_client import MongoClient, UpdateOne
from tqdm import tqdm
from typing import Optional


MONGO_URI = "mongodb+srv://{mongodb_creds}@bmat-tvav-prod.yq6o5.mongodb.net/{mongodb_name}?retryWrites=true&w=majority"
SCHEDULE_ID_FINDER = re.compile(r"https:\/\/.*\.bmat\.com\/programs\/view\/(.*)")
logger = logging.getLogger("update-schedule-timeshift")


class Config:
    def __init__(self) -> None:
        mongodb_creds = os.getenv("MONGODB_CREDS")
        mongodb_name = os.getenv("MONGODB_NAME")

        assert mongodb_creds is not None, "MONGODB_CREDS cannot be None"
        assert mongodb_name is not None, "MONGODB_NAME cannot be None"

        self.mongo_uri = MONGO_URI.format(
            mongodb_creds=mongodb_creds,
            mongodb_name=mongodb_name
        )
        
        epg_sync_username = os.getenv("EPG_SYNC_USERNAME")
        epg_sync_password = os.getenv("EPG_SYNC_PASSWORD")
        epg_sync_hostname = os.getenv("EPG_SYNC_HOSTNAME", "rdqa.bmat.com")

        assert epg_sync_username is not None, "EPG_SYNC_USERNAME cannot be None"
        assert epg_sync_password is not None, "EPG_SYNC_PASSWORD cannot be None"

        self.epg_sync_get_timeshift_url = (
            f"https://{epg_sync_username}:{epg_sync_password}@"
            f"{epg_sync_hostname}/epgsynch/rest_api/get_timeshift/"
        )

        min_start_time = os.getenv("MIN_START_TIME")
        max_start_time = os.getenv("MAX_START_TIME")

        if min_start_time and max_start_time:
            self.min_start_time = parse(min_start_time)
            self.max_start_time = parse(max_start_time)
        else:
            self.min_start_time = None
            self.max_start_time = None

        if __name__ == "__main__":
            self.parent_dir = Path(__file__).parent
        else:
            self.parent_dir = Path(os.getcwd())

        self.input_csv = self.parent_dir / "input.csv"
        self.stats_csv = self.parent_dir / "stats.csv"


@dataclass
class Stat:
    id: ObjectId
    start_time: datetime
    channel_keyname: Optional[str] = None
    time_shift: Optional[float] = None


def get_timeshift(config: Config, stat: Stat) -> float:
    res = requests.get(
        url=config.epg_sync_get_timeshift_url,
        params={
            "datetime": stat.start_time.strftime("%Y%m%d_%H%M%S"),
            "channel_keyname": stat.channel_keyname,
            "scope_minutes": 360,
        }
    ).json()

    return res["near_annotations"][0]["timeshift"]


def get_schedule_ids(config: Config, mongodb: Database) -> set[ObjectId]:
    schedule_ids: set[ObjectId] = set()
    with config.input_csv.open() as f:
        for url in f.readlines():
            url = url.replace("\n", "")

            if not url:
                continue

            if not (match := SCHEDULE_ID_FINDER.match(url)):
                raise RuntimeError(
                    "Could not get Schedule id from URL. "
                    "We expected URLs to follow Programs URL pattern."
                )
            schedule_id = base64.b64decode((match.group(1)).encode()).decode().replace("Schedule:", "")
            schedule_ids.add(ObjectId(schedule_id))

    if config.min_start_time is not None and config.max_start_time is not None:
        schedule_ids = schedule_ids.union(set(mongodb.schedule.distinct(
            "_id",
            {"start_time": {"$gte": config.min_start_time, "$lt": config.max_start_time}}
        )))

    return schedule_ids


def main():
    config = Config()
    client_db = MongoClient(host=config.mongo_uri).get_default_database()

    schedule_ids: set[ObjectId] = get_schedule_ids(config, client_db)
   
    logger.info(f"{len(schedule_ids)} unique Schedules")
    if not schedule_ids:
        return

    stats: list[Stat] = []

    for sch in tqdm(
        client_db.schedule.aggregate([
            {"$match": {"_id": {"$in": [s_id for s_id in schedule_ids]}}},
            {"$lookup": {
                "from": "channel",
                "as": "channel",
                "localField": "channel",
                "foreignField": "_id",
            }},
            {"$unwind": "$channel"},
            {"$project": {"start_time": 1, "channel_keyname": "$channel.keyname"}}
        ]),
        total=len(schedule_ids),
    ):
        stat = Stat(
            id=sch["_id"],
            start_time=sch["start_time"],
            channel_keyname=sch["channel_keyname"],
        )
        stat.time_shift = get_timeshift(config, stat)
        stats.append(stat)

    operations = [
        UpdateOne({"_id": stat.id}, {"$set": {"time_shift": stat.time_shift}})
        for stat in stats
    ]
    client_db.schedule.bulk_write(operations, ordered=False)

    logger.info("STATS:")
    pprint(stats)
    with config.stats_csv.open("wt") as f:
        writer = csv.writer(f)
        writer.writerow(stats[0].__dict__.keys())
        for stat in stats:
            writer.writerow(stat.__dict__.values())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    main()
