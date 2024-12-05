import logging
import os

from celery import Celery
from dotenv import load_dotenv
from pymongo import MongoClient


logging.basicConfig(level=logging.INFO)

# Generate main channels first and then regional channels
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

# Go live date
START_TIME = "2022-01-25T00:00:00"
END_TIME = "2023-11-01T00:30:47"
REPORT_FORMAT = "yle-gramex-teosto"
REPORT_NAMESPACE = "yle-reports-fortnightly"
TASK_NAME = "generate_report"
QUEUE = "yle-reports-submit"


def main():
    db = MongoClient(host=os.environ["MONGO_URI"]).get_default_database()
    app = Celery(broker=os.environ["CELERY"])

    user = db.user.find_one({"username": "bmat_processor"})
    total = 0

    for channel_id in MAIN_CHANNEL_IDS:
        channel = db.channel.find_one({'short_name': channel_id}, {"_id": 1})

        report = db.report.insert_one({
            "report_type": "cmo-biweekly",
            "reported_by": user["_id"],
            "report_status": "submitted"
        })

        task = app.signature(TASK_NAME, kwargs={
            "start_time": START_TIME,
            "end_time": END_TIME,
            "channel": str(channel["_id"]),
            "report_format": REPORT_FORMAT,
            "namespace": REPORT_NAMESPACE,
            "report": str(report.inserted_id),
        })
        task.apply_async(queue=QUEUE)
        total += 1

    for channel_id in SUB_CHANNEL_IDS:
        channel = db.channel.find_one({'short_name': channel_id}, {"_id": 1})

        report = db.report.insert_one({
            "report_type": "cmo-biweekly",
            "reported_by": user["_id"],
            "report_status": "submitted"
        })

        task = app.signature(TASK_NAME, kwargs={
            "start_time": START_TIME,
            "end_time": END_TIME,
            "channel": str(channel["_id"]),
            "report_format": REPORT_FORMAT,
            "namespace": REPORT_NAMESPACE,
            "report": str(report.inserted_id),
        })
        task.apply_async(queue=QUEUE)
        total += 1

    print("Total processed:", total)

    return {
        'statusCode': 200,
        'body': f'Total processed {total}'
    }


if __name__ == "__main__":
    load_dotenv()
    main()
