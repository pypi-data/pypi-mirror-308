import argparse
import datetime
import json
import logging
import os
import time
from typing import List

import boto3
from bson import ObjectId
from celery import Celery
from dotenv import load_dotenv
from file_processor.model import File
from mongoengine import connect

logger = logging.getLogger(__name__)

load_dotenv()

S3 = os.getenv("S3")

MONGO_HOST = os.getenv("MONGO_HOST")

app = Celery(broker=os.getenv("CELERY_BROKER"))

TIMEOUT = float(os.getenv("TIMEOUT", 0.5))


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        else:
            return super().default(o)


def encode_audiovisual_task(file_id):
    logger.info("encoding")
    task = app.signature(
        "encode_audiovisual",
        kwargs={
            "file": file_id,
        },
        queue="cuenator-matcher",
    )
    task.apply_async(queue="cuenator-matcher")


def register_audiovisual_task(file_id):
    task = app.signature(
        "register_audiovisual",
        kwargs={
            "file": file_id,
        },
        queue="cuenator-matcher",
    )
    task.apply_async(queue="cuenator-matcher")


def generate_vod(file_id):
    logger.info("generating vod")
    task = app.signature(
        "generate_vod",
        kwargs={
            "file": file_id,
        },
        queue="cuenator-matcher",
    )
    task.apply_async(queue="cuenator-matcher")


def upload_audiovisual(file_id):
    logger.info("uploading")
    task = app.signature(
        "upload_audiovisual",
        kwargs={
            "file": file_id,
        },
        queue="cuenator-matcher",
    )
    task.apply_async(queue="cuenator-matcher")


def extract_music_speech(file_id):
    task = app.signature(
        "extract_music_speech",
        kwargs={
            "file": file_id,
        },
        queue="cuenator-matcher",
    )
    task.apply_async(queue="cuenator-matcher")


class TaskRunner:
    TASKS = {
        "encode_audiovisual": (encode_audiovisual_task, "encoded"),
        "generate_vod": (generate_vod, "vod_generated"),
        "upload_audiovisual": (upload_audiovisual, "uploaded"),
    }

    def __init__(self, *tasks) -> None:
        self.now = datetime.datetime.utcnow()
        self.tasks = []
        for task in tasks:
            t = self.TASKS.get(task)
            if t:
                self.tasks.append(t)
            else:
                raise ValueError("Unknown task: {}".format(task))

    def run(self, file: File) -> None:
        file_id = str(file.id)
        for task, status in self.tasks:
            task(file_id)
            while not check_status(file, status, self.now):
                logger.info("waiting for %s", status)
                time.sleep(TIMEOUT)


def check_status(file: File, status: str, now: datetime.datetime) -> bool:
    file.reload("history")
    return bool([h for h in file.history if h.created > now and h.status == status])


def get_s3_client():
    credentials, bucket = S3.split("@")
    s3_key, s3_secret = credentials.split(":")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret,
    )
    return s3_client, bucket


def delete_s3_files(audiovisual):
    client, bucket_name = get_s3_client()
    for f in client.list_objects(Bucket=bucket_name, Prefix=str(audiovisual["_id"])).get("Contents", []):
        logger.info("Deleting %s", f)
        client.delete_object(Bucket=bucket_name, Key=f["Key"])


def clean_audiovisual(db, audiovisual, backup=True):
    logger.info("cleaning audiovisual %s", audiovisual["_id"])
    if backup:
        with open(f"backup_av_{audiovisual['_id']}.json", "w") as f:
            json.dump(audiovisual, f, indent=4, cls=Encoder)

    delete_s3_files(audiovisual)
    unset_params = {"result": 1, "matches": 1, "music_speech": 1, "job_id": 1}
    db.audiovisual.update_one({"_id": audiovisual["_id"]}, {"$unset": unset_params})


def reanalyse_file(mongo_client, file: File, tasks: List[str], clean_av: bool = True) -> None:
    logger.info("Reanalyzing file: %s", file.id)
    if clean_av:
        db = mongo_client.get_database()
        audiovisual = db.audiovisual.find_one({"file_info": file.id})
        clean_audiovisual(db, audiovisual)
        time.sleep(1.5)

    runner = TaskRunner(*tasks)
    runner.run(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        action="store",
        dest="loglevel",
        choices=["DEBUG", "INFO", "ERROR"],
        default="INFO",
    )
    parser.add_argument("-i", "--ids", nargs="+", type=str)
    parser.add_argument("-t", "--tasks", nargs="+", type=str, default=list(TaskRunner.TASKS.keys()))
    parser.add_argument("-c", "--clean_audiovisual", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.loglevel),
        format="%(asctime)s %(levelname)-8s %(funcName)-30s %(lineno)-5s %(message)s",
    )

    params = {
        "id__in": args.ids,
    }

    mongo_client = connect(host=MONGO_HOST)
    total = File.objects(**params).count()
    logger.info("Starting. Total files: %s", total)
    i = 0
    for file in File.objects(**params):
        reanalyse_file(mongo_client, file, args.tasks, args.clean_audiovisual)
        i += 1
        logger.info("Finished %s/%s", i, total)
