import csv
import datetime
import logging
from celery import Celery
from dotenv import load_dotenv
from mongoengine import connect
from time import sleep
from tqdm import tqdm
from typing import Generator

from file_processor import FileProcessor
from file_processor.model import File

from scripts.generic.bulk_import_same_cuesheet.config import BulkImportSameCuesheetConfig


logging.basicConfig(level=logging.INFO)


class BulkImportSameCuesheet:
    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = BulkImportSameCuesheetConfig()

    def get_file_to_use(self) -> dict:
        file = File.objects.get(id=self.config.file_id_to_use).to_mongo().to_dict()

        del file["_id"]
        file["history"] = []
        file["data"]["schedule_id"] = None
        file["data"][self.config.flag] = True

        return file

    def get_schedule_ids(self) -> Generator[str, None, None]:
        with open(
            self.config.input_file_with_schedule_ids_as_str,
            encoding="utf-8",
            mode="rt"
        ) as f:
            reader = csv.reader(f.readlines())
            for line in reader:
                yield line[0]

    @staticmethod
    def prepare_new_file(file_to_use: dict, schedule_id: str) -> File:
        file_to_use["data"]["schedule_id"] = schedule_id
        now = datetime.datetime.now()
        file_to_use["created"] = now
        file_to_use["updated"] = now
        return File(**file_to_use).save()

    def run(self):
        app = Celery(broker=self.config.get_celery_uri())
        fp = FileProcessor(app=app)

        files_to_process = []
        with connect(host=self.config.get_mongodb_connection_string()):
            file_to_use = self.get_file_to_use()
            self.logger.info("Cloning files...")
            for schedule_id in self.get_schedule_ids():
                new_file = self.prepare_new_file(file_to_use, schedule_id)
                files_to_process.append(new_file)

        self.logger.info("Processing files...")
        for file in tqdm(files_to_process):
            fp.process_file(file)
            sleep(0.1)

        self.logger.info("DONE")


if __name__ == "__main__":
    script = BulkImportSameCuesheet()
    script.run()
