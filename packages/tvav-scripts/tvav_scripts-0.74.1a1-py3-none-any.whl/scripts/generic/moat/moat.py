import base64
import csv
import json
import logging
import os
import pika
import sys
from bson import ObjectId
from celery import Celery
from dotenv import load_dotenv
from json import JSONDecodeError
from mongoengine import connect
from mongoengine.errors import DoesNotExist
from pathlib import Path
from time import sleep
from tqdm import tqdm

from reportal_model import AvWork, Schedule

from scripts.utils import count_lines

from scripts.generic.moat.utils.config import MoatConfig, ENV_MAPPING
from scripts.generic.moat.utils.tasks import ReportalTasks


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("moat")

# Lowering level for pika loggers bc of the SPAM in Jenkins tasks
logging.getLogger("pika.connection").setLevel(logging.ERROR)
logging.getLogger("pika.channel").setLevel(logging.ERROR)
logging.getLogger("pika.adapters.utils.").setLevel(logging.ERROR)
logging.getLogger("pika.adapters.blocki").setLevel(logging.ERROR)

if "3.6" in sys.version:
    logger.info("Running moat for v1")
    from gema.database_model import Broadcast
else:
    logger.info("Running moat for v2")


class MotherOfAllTasks:
    def __init__(self, **kwargs):
        load_dotenv()
        # Clean kwargs before getting config
        for config_prop, env_var_type_cast in ENV_MAPPING.items():
            env_var, type_cast = env_var_type_cast
            # Task params can either be a Dict or a JSON encoded dict as a String, so if it already is a dict, skip
            if config_prop == "task_params" and isinstance(kwargs.get("task_params"), dict):
                continue
            kwargs[config_prop] = type_cast(kwargs.get(config_prop, os.getenv(env_var)))

        self.config = MoatConfig(**kwargs)
        self._check_config()
        # Reports
        self.output_file = Path("output.csv")
        self.error_file = Path("error.csv")
        self.output_headers = ["ObjectId", "Reportal URL"]
        self.error_headers = ["ObjectId", "Error description"]

    def _check_config(self):
        """Checks if the configuration is valid + updates some configs."""
        check_kwargs_exceptions = [
            (
                all([self.config.mongo_uri, self.config.mongo_credentials, self.config.mongo_db]),
                "MongoDB values missing"
            ),
            (
                all([self.config.celery_uri, self.config.celery_credentials, self.config.celery_queue]),
                "Celery values missing"
            ),
            (
                self.config.input_file,
                "Input file value missing"
            ),
            (
                self.config.chosen_task and self.config.chosen_task in ReportalTasks.values(),
                "Chosen task value missing or invalid",
            ),
            (
                self.config.task_params,
                "Task params value missing",
            ),
        ]
        for kwargs_ok, exception_msg in check_kwargs_exceptions:
            if not kwargs_ok:
                raise ValueError(exception_msg)

        # Clean root configs
        self.config.mongo_uri = self.config.mongo_uri.format(self.config.mongo_credentials, self.config.mongo_db)
        self.config.input_file = Path(str(self.config.input_file))
        self.config.reportal_url = self.config.reportal_url.rstrip("/")

        if not (self.config.input_file.exists() and self.config.input_file.is_file()):
            raise ValueError("Check your input file")

        if not isinstance(self.config.task_params, dict):
            try:
                self.config.task_params = dict(json.loads(self.config.task_params))
            except (JSONDecodeError, TypeError) as e:
                raise ValueError("Check your TASK_PARAMS_AS_JSON_DICT") from e

        # Extras
        doc_type = self._get_doc_type(str(self.config.chosen_task))
        self.config.extras["doc_type"] = doc_type
        self.config.extras["id_field"] = self._get_id_field(doc_type)
        self.config.extras["endpoint"] = self._get_endpoint(doc_type)
        self.config.extras["file_processor_uri"] = self.config.celery_uri.format(self.config.celery_credentials)

    def _init_reports(self):
        """Initializes CSV reports"""
        for file, headers in [
            (self.output_file, self.output_headers),
            (self.error_file, self.error_headers),
        ]:
            file.touch()
            with file.open("wt") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    @staticmethod
    def _get_doc_type(task_name: str):
        """Gets the doc type from the chosen task name"""
        return (
            "".join(
                task_doc.capitalize()
                for task_doc in task_name.replace("import_", "").replace("populate_", "").split("_")
            ).replace("Jp", "")  # To remove import_schedule_jp
        )

    @staticmethod
    def _get_id_field(doc_type: str):
        if doc_type == "AvWork":
            return "av_work_id"
        if doc_type == "Schedule":
            return "schedule_id"
        if doc_type == "Broadcast":
            return "broadcast_id"
        raise ValueError("Unexpected doc_type '%s'", doc_type)

    @staticmethod
    def _get_endpoint(doc_type: str):
        if doc_type == "AvWork":
            return "cuesheets"
        if doc_type == "Schedule":
            return "programs"
        raise ValueError("Unexpected doc_type '%s'", doc_type)

    @staticmethod
    def _get_mongo_doc(doc_type: str, o_id: str):
        """Returns a database document depending on doc_type"""
        query = {"id": ObjectId(o_id)}
        if doc_type == "AvWork":
            return AvWork.objects(**query)
        if doc_type == "Schedule":
            return Schedule.objects(**query)
        if doc_type == "Broadcast":
            return Broadcast.objects(**query)

    def _wait_for_queue_count_to_lower(self):
        """
        Checks how many queued tasks there are.
        If it exceeds MAX_QUEUE_LOAD it will wait 1 minute and check again.
        """
        def get_queue_count() -> int:
            pika_conn = pika.BlockingConnection(pika.connection.URLParameters(self.config.extras["file_processor_uri"]))
            pika_channel = pika_conn.channel()
            pika_queue = pika_channel.queue_declare(
                queue=self.config.celery_queue,
                durable=True,
                exclusive=False,
                auto_delete=False
            )
            queue_counts = int(pika_queue.method.message_count)
            pika_conn.close()
            return queue_counts

        while get_queue_count() > self.config.max_queue_load:
            logger.info("Queue %s above %d. Waiting for 1 minute...", self.config.celery_queue, self.config.max_queue_load)
            sleep(60)
        else:
            logger.info("Queue %s below %d", self.config.celery_queue, self.config.max_queue_load)
            sleep(self.config.backoff_timer)

    def _report_error(self, o_id, error_msg):
        """Adds 1 row to the error report"""
        logger.error(error_msg)
        with self.error_file.open("at") as f:
            writer = csv.writer(f)
            writer.writerow([o_id, error_msg])

    def _report_document(self, o_id: str):
        """Adds 1 row to the output report"""
        encoded_id = base64.b64encode(f"{self.config.extras['doc_type']}:{o_id}".encode("utf-8")).decode("utf-8").replace("=", "%3D")
        reportal_url = f"{self.config.reportal_url}/{self.config.extras['endpoint']}/view/{encoded_id}"

        with self.output_file.open("at") as f:
            writer = csv.writer(f)
            writer.writerow([o_id, reportal_url])

    def run_task(self):
        """
        Inits reports, connects to mongoengine, keeps track of Celery queue count,
        sends celery task for each Document specified.

        Generates 2 reports:

        - output_report: Report with Document's ObjectIds and ReportalURLs
        - error_report: Report with Document's ObjectIds and Error messages
        """
        self._init_reports()

        app = Celery(broker=self.config.extras["file_processor_uri"] + "?ssl=true")

        with connect(host=self.config.mongo_uri), self.config.input_file.open("rt") as input_file:
            n_docs = count_lines(self.config.input_file)
            logger.info("Task %s on queue %s for %d %ss", self.config.chosen_task, self.config.celery_queue, n_docs, self.config.extras["doc_type"])
            counter = 0
            for line in tqdm(input_file.read().splitlines(), total=n_docs):
                counter += 1
                if counter >= self.config.trigger_queue_count:
                    self._wait_for_queue_count_to_lower()
                    counter = 0

                try:
                    doc = self._get_mongo_doc(self.config.extras["doc_type"], line)
                except DoesNotExist as e:
                    self._report_error(line, str(e))
                    continue

                self.config.task_params[self.config.extras["id_field"]] = str(doc[0].id)
                app.signature(
                    self.config.chosen_task,
                    queue=self.config.celery_queue,
                    kwargs=self.config.task_params,
                ).apply_async(queue=self.config.celery_queue)

                self._report_document(line)


if __name__ == "__main__":
    moat = MotherOfAllTasks()
    moat.run_task()
