import logging
from datetime import datetime
from dotenv import load_dotenv
from pymongo.errors import BulkWriteError
from pymongo.operations import UpdateOne
from pymongo.mongo_client import MongoClient
from tqdm import tqdm

from scripts.generic.update_all_index_info.config import UpdateAllIndexInfoConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("update_index")


def update_all_index_info(mongo: str, timestamp: datetime):
    """This function connects to a MongoDB cluster and updates
    db.index_info.last_updated to `timestamp` for every DB existing
    in said cluster.
    """

    cluster = MongoClient(host=mongo)
    logger.info("Successfully connected to the MongoDB cluster")

    database_names = cluster.list_database_names()
    with tqdm(
        database_names,
        desc="Databases",
        postfix=f"- db_name: {database_names[0]}"
    ) as pbar:
        for db_name in pbar:
            pbar.postfix = f"- db_name: {db_name}"
            if "stg" not in db_name and "prod" not in db_name:
                continue
            db = cluster.get_database(db_name)

            index_info = [doc for doc in db.index_info.find()]
            if not index_info:
                continue

            operations = [
                UpdateOne(
                    {"_id": doc["_id"]},
                    {"$set": {"last_update": timestamp}}
                )
                for doc in index_info
            ]

            try:
                _ = db.index_info.bulk_write(operations, ordered=False)
            except BulkWriteError as bwe:
                raise RuntimeError(bwe.details)


    logger.info("Update index OK")


if __name__ == "__main__":
    load_dotenv()
    settings = UpdateAllIndexInfoConfig()  # type: ignore
    update_all_index_info(**settings.model_dump())
