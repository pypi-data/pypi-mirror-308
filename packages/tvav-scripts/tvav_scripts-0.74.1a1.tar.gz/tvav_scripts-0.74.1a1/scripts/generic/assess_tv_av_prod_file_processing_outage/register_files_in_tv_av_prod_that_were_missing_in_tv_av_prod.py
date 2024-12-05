import csv
import pytz
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

from scripts.generic.assess_tv_av_prod_file_processing_outage.config import Config, bazaar_prod_files_missing_in_tv_av_prod_report


def register_files_in_tv_av_prod_that_were_missing_in_tv_av_prod():
    """Inserts files into tv-av-prod.

    This script is to be executed after main.py, and will use bazaar_prod_files_missing_in_tv_av_prod_report
    to get the filename and namespace to insert new documents into the file colleciton.
    """

    load_dotenv()
    config = Config()

    tv_av_prod = MongoClient(host=config.tv_av_prod_mongo_uri).get_default_database()
    now = datetime.now(pytz.UTC)

    with bazaar_prod_files_missing_in_tv_av_prod_report.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            inserted_id = tv_av_prod.file.insert_one({
                "path": row["name"],
                "namespace": row["namespace"],
                "data": {},
                "history": [{"status": "received", "created": now}],
                "error": False,
                "status": "received",
                "created": now,
                "updated": now,
                "is_removed": False
            }).inserted_id
            print(str(row), "-->", inserted_id)


if __name__ == "__main__":
    register_files_in_tv_av_prod_that_were_missing_in_tv_av_prod()
