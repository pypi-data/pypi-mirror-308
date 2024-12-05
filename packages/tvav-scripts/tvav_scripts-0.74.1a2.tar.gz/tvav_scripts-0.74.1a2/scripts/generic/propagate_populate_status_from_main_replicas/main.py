import logging
from datetime import UTC, datetime
from dotenv import load_dotenv
from mongoengine import connect
from pymongo import UpdateOne
from tqdm import tqdm

from reportal_model import  Schedule

from scripts.generic.propagate_populate_status_from_main_replicas.config import PropagatePopulateStatusFromMainReplicasSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("propagate_populate_to_reruns")


if __name__ == "__main__":
    load_dotenv()
    config = PropagatePopulateStatusFromMainReplicasSettings()  # type: ignore

    now = datetime.now(UTC)
    
    with connect(host=config.mongodb.get_mongo_db_uri()):
        logger.info("Starting...")
        orig_sch_and_rerun_list = Schedule.objects.aggregate([
            {"$match": {
                "start_time": {
                    "$gte": config.start_time_min,
                    "$lt": config.start_time_max,
                },
                "main_replica": False,
            }},
            {"$group": {"_id": "$av_work", "schedule_ids": {"$push": "$_id"}}},
            {"$lookup": {
                "from": "av_work",
                "as": "_id",
                "localField": "_id",
                "foreignField": "_id",
            }},
            {"$unwind": "$_id"},
            {"$match": {"_id.original_schedule": {"$ne": None}}},
            {"$lookup": {
                "from": "schedule",
                "as": "original_schedule",
                "localField": "_id.original_schedule",
                "foreignField": "_id",
            }},
            {"$unwind": "$original_schedule"},
            {"project": {"_id": 0}},
        ])

        operations = []

        for orig_sch_and_reruns in tqdm(orig_sch_and_rerun_list):
            orig_sch = orig_sch_and_reruns["original_schedule"]
            schedule_list = orig_sch_and_reruns["schedule_ids"]
            for sch_id in schedule_list:
                operations.append(UpdateOne(
                    {"_id": sch_id},
                    {"$set": {
                        "populated": orig_sch.get("populated", False),
                        "aggregations.updated_at": now,
                    }}
                ))
        logger.info(f"{len(operations)=}")
        Schedule._get_collection().bulk_write(operations, ordered=False)

    logger.info("Done")
