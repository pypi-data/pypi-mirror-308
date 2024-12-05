import os

from celery import Celery
from datetime import datetime
from dotenv import load_dotenv
from product.util import get_logger
from pymongo import MongoClient
from tqdm import tqdm
from typing import Iterable


logger = get_logger(name="generate-reports")

# Generate generate_report_stg channels first and then regional channels
MAIN_CHANNEL_IDS = [
    "r01",
    "r02",
    "r03",
    "r04",
    "r44",
    "r48"
]
SUB_CHANNEL_IDS = [
    "r94",
    "r58",
    "r57",
    "r55",
    "r54",
    "r59",
    "r17",
    "r19",
    "r10",
    "r42",
    "r62",
    "r30",
    "r81",
    "r91",
    "r71",
    "r51",
    "r60",
    "r41",
    "r50",
    "r61",
    "r80",
    "r21",
    "r90",
    "r63",
    "r40",
    "r20",
    "r70",
    "r93",
    "syt",
    "sfb",
    "sig",
    "stw",
    "swa",
    "spc",
    "ssc",
    "stt",
    "fem",
    "yte",
    "tv1",
    "tv2",
    "are",
    "yle.fi",
    "svenska.yle.fi"
]


def send_generate_report_task(app, queue, channel, report, start_time, end_time, namespace, report_format):
    task = app.signature("generate_report", kwargs={
        "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        "end_time": end_time.strftime('%Y-%m-%dT%H:%M:%S'),
        "channel": str(channel["_id"]),
        "report_format": report_format,
        "namespace": namespace,
        "report": str(report.inserted_id),
    })
    task.apply_async(queue=queue)


def generate_report_for_channels(db, app, queue, user_id, channel_ids: Iterable[str], start_time, end_time, namespace, report_format):
    total = 0
    for channel_id in tqdm(channel_ids):
        channel = db.channel.find_one({'short_name': channel_id}, {"_id": 1})
        report = db.report.insert_one({
            "report_type": "bidw-daily",
            "reported_by": user_id,
            "report_status": "submitted"
        })
        send_generate_report_task(app, queue, channel, report, start_time, end_time, namespace, report_format)
        total += 1
    return total


def generate_report(
    mongo_uri: str,
    celery_broker: str,
    queue: str,
    username: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str,
    report_format: str
):
    db = MongoClient(host=mongo_uri).get_default_database()
    app = Celery(broker=celery_broker)

    user = db.user.find_one({"username": username})

    logger.info(f"Generating report as user {username} in time range: {start_time} - {end_time}")

    total_reports = 0
    logger.info("Generating reports for MAIN CHANNELS")
    total_reports += generate_report_for_channels(db, app, queue, user["_id"], MAIN_CHANNEL_IDS, start_time, end_time, namespace, report_format)
    logger.info("Generating reports for SUB CHANNELS")
    total_reports += generate_report_for_channels(db, app, queue, user["_id"], SUB_CHANNEL_IDS, start_time, end_time, namespace, report_format)

    logger.info(f"Total processed: {total_reports}")


if __name__ == "__main__":
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    mongo_user = os.getenv("MONGO_USER")
    mongo_db = os.getenv("MONGO_DB")
    celery_broker = os.getenv("CELERY_BROKER")
    celery_queue = os.getenv("CELERY_QUEUE")

    user = os.getenv("USER")
    start_time = os.getenv("START_TIME")
    end_time = os.getenv("END_TIME")
    report_format = os.getenv("REPORT_FORMAT")
    namespace = os.getenv("REPORT_SUBMIT_NAMESPACE")

    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error(f"Invalid datetime format {start_time} - {end_time} (Expected: %Y-%m-%d %H:%M:%S)")
        exit(-1)

    generate_report(
        mongo_uri=mongo_uri.format(mongo_user, mongo_db),
        celery_broker=celery_broker,
        queue=celery_queue,
        username=user,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        report_format=report_format
    )
