import base64
import csv
import os
import json
import logging
import re
from bson import ObjectId
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
from pymongo import MongoClient
from typing import Callable, Optional


logger = logging.getLogger("reanalyze-cued")
AV_WORK_ID_FINDER = re.compile(r"https:\/\/.*\.bmat\.com\/cuesheets\/view\/(.*)%3D%3D$")
FINAL_STATUS = "Removed matches and musicspeech_matches from audiovisual.result and root level"
MONGO_URI = "mongodb+srv://{mongodb_creds}@bmat-tvav-prod.yq6o5.mongodb.net/{mongo_db}?retryWrites=true&w=majority"

class Config:
    def __init__(self) -> None:
        mongodb_creds = os.getenv("MONGODB__CREDS")
        client_mongo_db = os.getenv("CLIENT_MONGO_DB")

        assert mongodb_creds is not None, "MONGODB__CREDS cannot be None"
        assert client_mongo_db is not None, "CLIENT_MONGO_DB cannot be None"

        self.client_mongo_uri = MONGO_URI.format(
            mongodb_creds=mongodb_creds,
            mongo_db=client_mongo_db,
        )

        self.tv_av_prod_mongo_uri = MONGO_URI.format(
            mongodb_creds=mongodb_creds,
            mongo_db="tv-av-prod",
        )

        if __name__ == "__main__":
            self.parent_dir = Path(__file__).parent
        else:
            self.parent_dir = Path(os.getcwd())

        self.input_csv = self.parent_dir / "input.csv"
        self.stats_csv = self.parent_dir / "stats.csv"
        self.files_to_reprocess_csv = self.parent_dir / "files_to_reprocess.csv"


@dataclass
class Stat:
    url: str
    av_work_id: str
    file_id: Optional[str] = None
    status: str = "UNTOUCHED"

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)


def set_status(stats: list[Stat], status: str, filter_fn: Optional[Callable[[Stat], bool]] = None):
    """Update all stats.status selectively using a filter_fn."""

    logger.info(status)

    if filter_fn is None:
        filter_fn = lambda _: True

    for stat in stats:
        if filter_fn(stat):
            stat.status = status


def run():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    )
    logger.info("START")

    config = Config()
    client_db = MongoClient(host=config.client_mongo_uri).get_default_database()
    tv_av_prod_db = MongoClient(host=config.tv_av_prod_mongo_uri).get_default_database()

    stats: list[Stat] = []
    unique_av_work_ids_set: set[ObjectId] = set()

    with config.input_csv.open() as f:
        for url in f.readlines():
            url = url.replace("\n", "")
            if not (match := AV_WORK_ID_FINDER.match(url)):
                raise RuntimeError(
                    "Could not get AvWork id from URL. "
                    "We expected URLs to follow Cuesheets URL pattern."
                )
            av_work_id = base64.b64decode((match.group(1) + "==").encode()).decode().replace("AvWork:", "")
            unique_av_work_ids_set.add(ObjectId(av_work_id))
            stats.append(Stat(url=url, av_work_id=av_work_id))

    unique_av_work_ids_list: list[ObjectId] = [_ for _ in unique_av_work_ids_set]

    client_db.av_work.update_many({"_id": {"$in": unique_av_work_ids_list}}, {"$set": {"imported": False, "populated": False}})
    set_status(stats, "Imported and populated set to false")

    client_db.av_work.update_many(
        {"_id": {"$in": unique_av_work_ids_list}}, {"$set": {"import_protected": False}, "$unset": {"import_protected_reason": None}}
    )
    client_db.schedule.update_many(
        {"av_work": {"$in": unique_av_work_ids_list}}, {"$set": {"import_protected": False}, "$unset": {"import_protected_reason": None}}
    )
    set_status(stats, "Removed import protection from AvWork and Schedule")

    aw_file_ids = {
        str(aw["_id"]): str(aw["file_info"])
        for aw in client_db.av_work.find(
            {"_id": {"$in": unique_av_work_ids_list}},
            {"file_info": "$file_import_info.file_info"}
        )
    }
    unique_file_ids_set: set[ObjectId] = set()

    for stat in stats:
        file_id = aw_file_ids.get(stat.av_work_id)

        # weird case but we've seen av_works without file_id due to bugs
        if file_id is None:
            continue

        unique_file_ids_set.add(ObjectId(file_id))
        stat.file_id = file_id

    unique_file_ids_list: list[ObjectId] = [_ for _ in unique_file_ids_set]

    tv_av_prod_db.file.update_many(
        {"_id": {"$in": unique_file_ids_list}},
        {"$unset": {"data.matches": 1, "data.music_speech": 1}}
    )
    set_status(
        stats,
        "Removed matches and music_speech from file.data",
        lambda s: ObjectId(s.file_id) in unique_file_ids_set
    )

    tv_av_prod_db.audiovisual.update_many(
        {"file_info": {"$in": unique_file_ids_list}},
        {"$unset": {
            "matches": 1,
            "musicspeech_matches": 1,
            "result.matches": 1,
            "result.musicspeech_matches": 1,
        }}
    )
    set_status(
        stats,
        FINAL_STATUS,
        lambda s: ObjectId(s.file_id) in unique_file_ids_set
    )

    logger.info("STATS:")
    pprint(stats)
    with config.stats_csv.open("wt") as f:
        writer = csv.writer(f)
        writer.writerow(stats[0].__dict__.keys())
        for stat in stats:
            writer.writerow(stat.__dict__.values())

    # only re-process those that reached the final status
    with config.files_to_reprocess_csv.open("wt") as f:
        for stat in stats:
            if stat.status == FINAL_STATUS:
                print(stat.av_work_id, file=f)

    logger.info("Use files_to_reprocess.csv file generated, to re-ingest them using the Jenkins script.")
    logger.info("END")


if __name__ == "__main__":
    load_dotenv()
    run()
