import csv
import json
import logging
import os
from celery import Celery
from collections import defaultdict
from dotenv import load_dotenv
from functools import lru_cache
from kafka import KafkaProducer
from mongoengine import connect
from pathlib import Path
from time import sleep
from tqdm import tqdm

from file_processor.model import File, User
from file_processor import FileProcessor

from scripts.utils.common_config_models import CelerySettings, KafkaSettings, MongoDBSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reprocess_files")

# mute external loggers
logging.getLogger("kafka.conn").setLevel(logging.ERROR)
logging.getLogger("pymongo.serverSelection").setLevel(logging.ERROR)


class Config:
    def __init__(self) -> None:
        self.mongodb = MongoDBSettings(
            creds=os.getenv("MONGODB__CREDS"),
            db_name="tv-av-prod"
        )
        self.kafka = KafkaSettings(
            sasl_plain_username=os.getenv("KAFKA__SASL_PLAIN_USERNAME"),
            sasl_plain_password=os.getenv("KAFKA__SASL_PLAIN_PASSWORD")
        )
        self.celery = CelerySettings(creds=os.getenv("CELERY__CREDS"))

        # input csv file
        if __name__ == "__main__":
            self.parent_dir = Path(__file__).parent
        else:
            self.parent_dir = Path(os.getcwd())

        self.input_file = self.parent_dir / "input.csv"
        self.error_file = self.parent_dir / "errors.csv"

        if not self.input_file.exists():
            raise FileNotFoundError("input.csv")

        # how many files to process at once
        self.max_batch_size = int(os.getenv("MAX_BATCH_SIZE") or 3)
        # how many seconds to wait between 2 consecutive batches
        self.backoff_timer = int(os.getenv("BACKOFF_TIMER") or 10)


class FileProcessMethod:
    CELERY = "CELERY"
    KAFKA = "KAFKA"


def celery_process(fp: FileProcessor, file: File):
    fp.process_file(file)


def kafka_process(producer: KafkaProducer, file: File):
    if "yle" in file.namespace:
        topic = "cuenator"
        payload = {
            "file": str(file.id),
            "profile": "yle",
            "vod": True,
            "fp": "mediaplayer" not in file.namespace,
        }
    else:
        topic = "new_file_registered_event"
        payload = {
            "file_id": str(file.id),
            "namespace": file.namespace,
        }
    producer.send(
        topic=topic,
        value=json.dumps(payload).encode()
    ).get(timeout=60)


@lru_cache()
def decide_method_to_use(namespace: str) -> str:
    user = next(User.objects(providers__namespace=namespace), None)

    if not user:
        raise RuntimeError(f"Could not find user with {namespace=}")

    chain = []
    for provider in user.providers:
        if provider.namespace != namespace:
            continue
        chain = provider.chain
        break

    method = (
        FileProcessMethod.CELERY
        if len(chain) > 0
        else FileProcessMethod.KAFKA
    )

    return method


def re_process_files():
    """Triggers the right Celery task / Kafka event for both Reportal and Cued
    files.

    We first decide which FileProcessMethod to use (CELERY vs KAFKA) by
    looking at the user providers' task chain by matching the file namespace.

    Then we either use the FileProcessor class for CELERY or trigger the right
    Kafka event.

    This script even considers yle special set ups (changes the Kafka event to use
    based on mediaplayer too).
    """

    load_dotenv()
    # constant DB
    config = Config()

    stats = defaultdict(list)
    
    with config.input_file.open() as f:
        file_ids = [
            file_id.replace("\n", "")
            for file_id in f.readlines()
            if file_id
        ]

    with connect(host=config.mongodb.get_mongo_db_uri()):
        logger.info("Running re-process for %d files" % len(file_ids))

        fp = None
        producer = None

        if config.celery.is_ready():
            app = Celery(broker=config.celery.get_celery_uri())
            fp = FileProcessor(app=app)

        if config.kafka.is_ready():
            producer = KafkaProducer(**config.kafka.model_dump())

        counter = 0
        for file_id in tqdm(file_ids):
            try:
                file = File.objects.get(id=file_id)

                method = decide_method_to_use(file.namespace)

                if method == FileProcessMethod.CELERY:
                    if not fp:
                        raise RuntimeError("Missing Celery configuration")
                    celery_process(fp, file)
                else:
                    # method is KAFKA
                    if not producer:
                        raise RuntimeError("Missing Kafka configuration")
                    kafka_process(producer, file)
            except Exception as e:
                stats[str(e)].append(file_id)

            counter += 1
            if (counter % config.max_batch_size) == 0:
                sleep(config.backoff_timer)

    with config.error_file.open("wt") as f:
        writer = csv.writer(f)
        writer.writerow(stats.keys())

        for error, f_ids in stats.items():
            for f_id in f_ids:
                writer.writerow([f_id, error])

    logger.info("Done")


if __name__ == "__main__":
    re_process_files()
