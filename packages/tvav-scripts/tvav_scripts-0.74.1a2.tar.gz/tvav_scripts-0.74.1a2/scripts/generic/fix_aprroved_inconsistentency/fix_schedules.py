import argparse
import logging
import os
import time
from itertools import islice

from celery import Celery
from dotenv import load_dotenv
from mongoengine import connect

logger = logging.getLogger(__name__)

load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
QUEUE = os.getenv("QUEUE")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))
TIMEOUT = float(os.getenv("TIMEOUT", 0.5))

app = Celery(broker=os.getenv("CELERY_BROKER"))


def calculate_schedule_aggregations_bulk_task(params):
    logger.info("sending task calculate_schedule_aggregations_bulk")
    task = app.signature(
        "calculate_schedule_aggregations_bulk",
        kwargs={
            "schedule_params": params,
        },
        queue=QUEUE,
    )
    task.apply_async(queue=QUEUE)


def get_scheduels_with_mismatced_approved_field(db):
    return db.schedule.aggregate(
        [
            {"$lookup": {"from": "av_work", "localField": "av_work", "foreignField": "_id", "as": "av_work"}},
            {"$match": {"$expr": {"$ne": ["$aggregations.approved", {"$arrayElemAt": ["$av_work.approved", 0]}]}}},
            {"$project": {"_id": 1}},
        ]
    )


def run(db):
    logger.info("starting")
    schedules = (s for s in get_scheduels_with_mismatced_approved_field(db))
    while True:
        batch = list(islice(schedules, BATCH_SIZE))
        if not batch:
            break
        calculate_schedule_aggregations_bulk_task(
            {
                "id__in": [str(schedule["_id"]) for schedule in batch],
            }
        )
        time.sleep(TIMEOUT)
    logger.info("finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        action="store",
        dest="loglevel",
        choices=["DEBUG", "INFO", "ERROR"],
        default="INFO",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.loglevel),
        format="%(asctime)s %(levelname)-8s %(funcName)-30s %(lineno)-5s %(message)s",
    )

    mongo_client = connect(host=MONGO_HOST)
    db = mongo_client.get_database()
    run(db)
