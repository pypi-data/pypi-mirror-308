import base64
import csv
import flatdict
import logging
import os

from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, MusicWork
from tqdm import tqdm


logging.basicConfig(level=logging.INFO)


def update_music_work(music_work: MusicWork, field_to_refactor: str, old_value, new_value):
    """
    Will go through each level of depth searching for the old_value in field and update it.
    """
    def update_music_work_dict(in_dict):
        # Checking root level first
        if "." not in field_to_refactor and in_dict[field_to_refactor] == old_value:
            in_dict[field_to_refactor] = new_value
            return in_dict

        # If it was not at root level, we dig deeper
        flat_mw_dict = flatdict.FlatterDict(in_dict, delimiter=".")

        if field_to_refactor in flat_mw_dict and flat_mw_dict[field_to_refactor] == old_value:
            # it was nested but not in iterable
            flat_mw_dict[field_to_refactor] = new_value
            in_dict = flat_mw_dict.as_dict()
            return in_dict

        # It must be inside an iterable, we look for it
        fields = field_to_refactor.split(".")
        for field in fields[:-1]:
            composed_field = '.'.join(fields[:fields.index(field) + 1])
            if f"{composed_field}.0" in flat_mw_dict:
                for i, _ in enumerate(flat_mw_dict[composed_field]):
                    full_idx = f"{composed_field}.{i}.{'.'.join(fields[fields.index(field) + 1:])}"
                    if full_idx not in flat_mw_dict:
                        continue
                    if flat_mw_dict[full_idx] == old_value:
                        flat_mw_dict[full_idx] = new_value
                        # no quick return bc more than 1 update may be needed
        in_dict = flat_mw_dict.as_dict()
        return in_dict

    mw_dict = music_work.to_mongo().to_dict()
    mw_dict = update_music_work_dict(mw_dict)
    # Update MusicWork from dict
    mw_dict["id"] = mw_dict.pop("_id")
    MusicWork(**mw_dict).save()


def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count


class MusicWorkRefactor:
    affected_mws_fields = [
        "music_work_id",
        "modified_field",
        "old_value",
        "new_value"
    ]
    affected_aws_fields = [
        "reportal_url",
        "program_id",
        "n_cue",
        "music_work_title",
        "modified_field",
        "old_value",
        "new_value",
    ]

    skipped_mws_fields = [
        "music_work_id",
        "skip_reason",
    ]

    def __init__(self, *args, **kwargs):
        load_dotenv()
        self.input_csv = kwargs.get("input_csv", os.getenv("INPUT_CSV", None))
        self.mongo_uri = kwargs.get("mongo_uri", os.getenv("MONGO_URI", None))
        self.mongo_user = kwargs.get("mongo_user", os.getenv("MONGO_USER", None))
        self.mongo_db = kwargs.get("mongo_db", os.getenv("MONGO_DB", None))
        self.reportal_url = kwargs.get("reportal_url", os.getenv("REPORTAL_URL", None))
        self.field_to_refactor = kwargs.get("field_to_refactor", os.getenv("FIELD_TO_REFACTOR", None))
        self.custom_customer_id = kwargs.get("field_to_refactor", os.getenv("CUSTOM_CUSTOMER_ID", "program_id"))
        # Report utils
        self.now = None
        self.music_work_report = None
        self.mw_writer = None
        self.av_work_report = None
        self.aw_writer = None
        self.skipped_report = None
        self.skipped_writer = None
        # Logger
        self.logger = logging.getLogger("mw-refactor")

    def do_refactor(self):
        """
        Performs the DB refactor using values in INPUT_CSV and FIELD_TO_REFACTOR.
        Generates 3 CSV reports:
        1. The affected MusicWorks (music_work_id, modified_field, old_value, new_value)
        2. The affected AvWorks (reportal_url, program_id, n_cue, music_work_title, modified_field, old_value, new_value)
        3. The skipped MusicWorks (music_work_id, skipped_reason)
        """
        self.check_env_vars()
        try:
            self.init_reports()

            n_rows = count_lines(self.input_csv)

            with connect(host=self.mongo_uri.format(self.mongo_user, self.mongo_db)):
                self.logger.info("Processing %s rows" % n_rows)
                for old_value, new_value in tqdm(self.read_values_from_csv_file(), total=int(n_rows)):
                    affected_music_works = self.get_music_works(query={
                        self.field_to_refactor: old_value
                    })

                    for music_work in tqdm(affected_music_works, total=affected_music_works.count()):
                        self.replace_value_in_music_work(music_work, old_value, new_value)
                        self.register_change(str(music_work.id), music_work.title, old_value, new_value)

            self.logger.info("Finished MusicWork refactor")
        finally:
            self.finish_reports()

    def check_env_vars(self):
        """Raises ValueError if None value in input params."""
        if any([
            not self.input_csv,
            not self.mongo_uri,
            not self.mongo_user,
            not self.mongo_db,
            not self.reportal_url,
            not self.field_to_refactor,
            not self.custom_customer_id,
        ]):
            raise ValueError("Check your env vars. None values are not allowed.")

    def init_reports(self):
        """Prepare report files"""
        self.now = datetime.now()
        self.music_work_report = open(f"affected_music_works_{self.now}.csv", "wt")
        self.mw_writer = csv.DictWriter(self.music_work_report, fieldnames=self.affected_mws_fields)
        self.mw_writer.writeheader()

        self.av_work_report = open(f"affected_av_works_{self.now}.csv", "wt")
        self.aw_writer = csv.DictWriter(self.av_work_report, fieldnames=self.affected_aws_fields)
        self.aw_writer.writeheader()

        self.skipped_report = open(f"skipped_music_works_{self.now}.csv", "wt")
        self.skipped_writer = csv.DictWriter(self.skipped_report, fieldnames=self.skipped_mws_fields)
        self.skipped_writer.writeheader()

        self.logger.info("Init reports OK")

    def finish_reports(self):
        """Close report files"""
        self.music_work_report.close()
        self.av_work_report.close()
        self.skipped_report.close()
        self.logger.info("Finish reports OK")

    def read_values_from_csv_file(self):
        """
        Reads a CSV file containing 2 columns (old_value, new_value) and yields each row.
        """
        if not os.path.exists(self.input_csv) or not os.path.isfile(self.input_csv):
            raise ValueError("Bad INPUT_CSV")

        with open(self.input_csv, "rt") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row["old_value"], row["new_value"]

    @staticmethod
    def get_music_works(query: dict):
        """Queries the DB to find all MusicWorks matching input query."""
        return MusicWork.objects(__raw__=query)

    def replace_value_in_music_work(self, music_work: MusicWork, old_value, new_value):
        """Replaces old_value with new_value in MusicWork's field."""
        update_music_work(music_work, self.field_to_refactor, old_value, new_value)

    def register_skip(self, music_work_id: str, skip_reason: str):
        """Adds row to skip report"""
        self.skipped_writer.writerow({
            "music_work_id": music_work_id,
            "skip_reason": skip_reason
        })

    def register_change(self, music_work_id: str, music_work_title: str, old_value, new_value):
        """Adds row to affected_mw_report + affected_aw_report"""
        # Add MusicWork to affected_mw_report
        self.mw_writer.writerow({
            "music_work_id": music_work_id,
            "modified_field": self.field_to_refactor,
            "old_value": old_value,
            "new_value": new_value,
        })
        # Add AvWork to affected_aw_report
        av_work = self.get_av_work_linked_to_music_work(music_work_id)
        self.aw_writer.writerow({
            "reportal_url": self.convert_to_reportal_url("AvWork:" + str(av_work.id)),
            "program_id": av_work.work_ids.get(self.custom_customer_id, None),
            "n_cue": self.get_cue_positions(music_work_id, av_work),
            "music_work_title": music_work_title,
            "modified_field": self.field_to_refactor,
            "old_value": old_value,
            "new_value": new_value,
        })

    @staticmethod
    def get_av_work_linked_to_music_work(music_work_id: str) -> AvWork:
        """Returns 1 AvWork linked to the music_work_id"""
        return next(AvWork.objects(__raw__={
            "cuesheet.cues.music_work": ObjectId(music_work_id)
        }))

    def convert_to_reportal_url(self, s: str) -> str:
        """Converts s string to reportal URL."""
        return self.reportal_url + "/cuesheets/view/" + base64.b64encode(s.encode("ascii")).decode("ascii").replace("=", "%3D")

    @staticmethod
    def get_cue_positions(music_work_id: str, av_work: AvWork) -> list[int]:
        """Returns cue positions for all music_work_id present in av_work."""
        positions = []  # We could have the same cue multiple times in 1 AvWork
        for cue in av_work.cuesheet.cues:
            if (mw := getattr(cue, "music_work", None)) and str(mw.id) == music_work_id:
                positions.append(cue.cue_index)
        return positions


if __name__ == "__main__":
    mwr = MusicWorkRefactor()
    mwr.do_refactor()
