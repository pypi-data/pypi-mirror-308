import csv
from bson import ObjectId
from datetime import timedelta
from dotenv import load_dotenv
from tqdm import tqdm
from typing import Iterable, Optional
from pathlib import Path
from pymongo import MongoClient

from scripts.generic.assess_tv_av_prod_file_processing_outage.config import (
    BLACKLIST_STATUSES,
    STATUS_FN_MAPPING,
    Config,
    unexpected,
    bazaar_prod_files_missing_in_tv_av_prod_report
)


def write_report(report_file: Path, rows: Iterable, headers: Optional[Iterable] = None):
    with report_file.open("wt") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in rows:
            if isinstance(row, str):
                row = [row]
            writer.writerow(row)


def run():
    load_dotenv()
    config = Config()

    tv_av_prod = MongoClient(host=config.tv_av_prod_mongo_uri).get_default_database()
    bazaar_prod = MongoClient(host=config.bazaar_prod_mongo_uri).get_default_database()

    query_programs_created_within_range = {
        "_id": {"$gte": ObjectId.from_datetime(config.start_time), "$lt": ObjectId.from_datetime(config.end_time)},
    }

    # 1. Have we processed all the files across all Reportal & Cued namespaces we received?
    query = query_programs_created_within_range.copy()
    query |= {"status": {"$nin": BLACKLIST_STATUSES}}

    files_grouped_by_status = tv_av_prod.file.aggregate([
      {"$match": query},
      {"$group": {"_id": "$status", "file_ids": {"$push": "$_id"}}}
    ])

    for status_group in files_grouped_by_status:
        status = status_group["_id"]
        file_ids = [str(f_id) for f_id in status_group["file_ids"]]

        write_report(STATUS_FN_MAPPING.get(status, unexpected), file_ids)

    # 2. Do we have any files in bazaar-prod DB that are not in tv-av-prod DB because the file scheduler didn't process the message?
    bazaar_prod_files = bazaar_prod.file.find(query_programs_created_within_range, {"namespace": 1, "name": 1, "created": 1})
    total = bazaar_prod.file.count_documents(query_programs_created_within_range)

    files_missing_list = []
    for doc in tqdm(bazaar_prod_files, total=total, desc="Searching for bazaar files missing in tv-av-prod"):
        query = {
            "created": {"$gte": doc["created"] - timedelta(days=1)},
            "namespace": doc["namespace"],
            "path": doc["name"],
        }

        if tv_av_prod.file.count_documents(query) == 0:
            files_missing_list.append(doc)

    if files_missing_list:
        files_missing_list = sorted(files_missing_list, key=lambda x: x["_id"])
        write_report(
            report_file=bazaar_prod_files_missing_in_tv_av_prod_report,
            rows=[file.values() for file in files_missing_list],
            headers=files_missing_list[0].keys(),
        )


if __name__ == "__main__":
    run()
