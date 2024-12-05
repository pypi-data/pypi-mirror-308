import csv
import logging
import os
from typing import Optional

from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import connect, DoesNotExist
from file_processor.model import File
from pathlib import Path
from tqdm import tqdm

from scripts.utils import log_decorator, count_lines


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("report-files-log")


class ReportFilesReceivedFromLog:

    def __init__(
        self,
        input_filename: Optional[str] = None,
        mongo_credentials: Optional[str] = None,
        *args,
        **kwargs
    ):
        """
        Reads INPUT_FILENAME text file and searches for File documents in tv-av-prod / file.

        Takes INPUT_FILENAME and MONGO_CREDENTIALS from environment, but you can pass these values
        as "input_filename" and "mongo_credentials" accordingly.

        Generates 3 reports:
        - output.csv: report with all found File documents.
        - not_found.csv: report with all File documents not found in DB.
        - meta.csv: report with info requested in the ticket:
            - Number of files in INPUT_FILENAME.
            - Number of files in DB.
            - Duplicated count (unique File ID + number of appearances in INPUT_FILENAME).
        """
        load_dotenv()

        self.mongo_uri = "mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority"
        self.mongo_credentials = mongo_credentials or os.getenv("MONGO_CREDENTIALS")
        self.mongo_db = "tv-av-prod"

        # Files
        self.input_file = Path(input_filename or os.getenv("INPUT_FILENAME"))
        self.output_file = Path("output.csv")
        self.error_file = Path("not_found.csv")
        self.meta_file = Path("meta.csv")

        self.output_headers = ["File ID", "File Name", "Namespace", "Created at", "Updated at", "Status", "Error description"]
        self.error_headers = ["File ID", "Error description"]
        self.meta_headers = [
            "Number of files received for the period (LOGS)",
            "Number of files ingested for the period (DB)",
            "Duplicated File ID",
            "Times dup"
        ]

    @log_decorator(log_msg="Initializing reports", logger=logger)
    def _init_reports(self):
        """
        Checks if INPUT_FILENAME exists and is a file.
        Creates the report files with their headers:
        - Output report
        - Error report
        - Meta report
        """
        if not (self.input_file.exists() and self.input_file.is_file()):
            error = "INPUT_FILENAME not found or is not a file."
            logger.error(error)
            raise ValueError(error)

        for file, headers in tqdm((
            (self.output_file, self.output_headers),
            (self.error_file, self.error_headers),
            (self.meta_file, self.meta_headers),
        )):
            file.touch()
            with file.open("wt") as f:
                report = csv.writer(f)
                report.writerow(headers)

    @log_decorator(log_msg="Adding row to error report", log_level=logging.DEBUG, logger=logger)
    def _add_to_error_report(self, o_id: str, error_msg: str):
        """Adds 1 row to error report"""
        logger.info("Registering error '%s' - '%s'", o_id, error_msg)
        with self.error_file.open("at") as error_report_file:
            error_report = csv.writer(error_report_file)
            error_report.writerow([o_id, error_msg])

    @log_decorator(log_msg="Generating meta report", logger=logger)
    def _generate_meta_report(self, unique_counter: dict):
        """Generates meta report with FAQ for the ticket"""
        with self.meta_file.open("at") as meta_report_file:
            input_log_lines = count_lines(self.input_file)
            output_report_lines = count_lines(self.output_file) - 1  # The first row

            meta_report = csv.writer(meta_report_file)
            meta_report.writerow([
                input_log_lines,
                output_report_lines,
                None,
                None
            ])
            for o_id, dup_count in unique_counter.items():
                if dup_count == 1:
                    continue
                meta_report.writerow([
                    None,
                    None,
                    o_id,
                    dup_count
                ])

    @log_decorator(log_msg="Generating reports", logger=logger)
    def generate_reports(self):
        unique_object_id_count = {}

        self._init_reports()

        with self.input_file.open(
            mode="rt"
        ) as input_log, self.output_file.open(
            mode="at"
        ) as output_report_file, connect(
            host=self.mongo_uri.format(self.mongo_credentials, self.mongo_db)
        ):
            output_report = csv.writer(output_report_file)

            for line in tqdm(input_log, total=count_lines(self.input_file)):
                o_id = line.strip('\n')

                if o_id in unique_object_id_count:
                    unique_object_id_count[o_id] += 1
                    continue

                unique_object_id_count[o_id] = 1

                try:
                    file_doc = File.objects.get(id=ObjectId(o_id))
                except DoesNotExist:
                    self._add_to_error_report(o_id, f"File not found in {self.mongo_db}.")
                    continue

                output_report.writerow([
                    o_id,
                    file_doc.path,
                    file_doc.namespace,
                    str(file_doc.created),
                    str(file_doc.updated),
                    file_doc.status,
                    file_doc.history[-1].error_description or "-",
                ])

        self._generate_meta_report(unique_object_id_count)


if __name__ == "__main__":
    report_generator = ReportFilesReceivedFromLog()
    report_generator.generate_reports()
