import csv
import mongoengine
from bson.objectid import ObjectId
from datetime import datetime
import os
import tempfile
import re
from pydantic_settings import BaseSettings
from unittest.mock import patch

from scripts.yle.unapproved_after_reported.unapproved_after_reported import ReportedButUnapproved, load_env_variables, generate_output_filename


class FakeSettings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017/"
    build_number: str = "1"
    input_start_time: datetime = datetime(2019, 12, 31)
    input_end_time: datetime = datetime(2020, 1, 2)


class FakeScheduleDocument(mongoengine.Document):
    _id = mongoengine.ObjectIdField()
    channel_display_name = mongoengine.StringField()
    program_title = mongoengine.StringField()
    alt_title = mongoengine.StringField(required=False)
    program_id = mongoengine.ObjectIdField()
    unique_id = mongoengine.StringField()
    client_id = mongoengine.StringField()
    broadcast_start_time = mongoengine.DateTimeField()
    last_edited_time = mongoengine.DateTimeField()
    last_approved_time = mongoengine.DateTimeField()
    last_reported_time = mongoengine.DateTimeField()


def document_data(
    _id=ObjectId(),
    channel_display_name="Test Channel",
    program_title="Test Program",
    alt_title="Test Alt Title",
    program_id=ObjectId(),
    unique_id="0123456789",
    client_id="ABCDEFGHIJ",
    broadcast_start_time=datetime(2020, 1, 1),
    last_edited_time=datetime(2020, 1, 1),
    last_approved_time=datetime(2020, 1, 1),
    last_reported_time=datetime(2020, 1, 1),
):
    return FakeScheduleDocument(
        _id=_id,
        channel_display_name=channel_display_name,
        program_title=program_title,
        alt_title=alt_title,
        program_id=program_id,
        unique_id=unique_id,
        client_id=client_id,
        broadcast_start_time=broadcast_start_time,
        last_edited_time=last_edited_time,
        last_approved_time=last_approved_time,
        last_reported_time=last_reported_time,
    )


def test_load_dotenv():
    with patch("scripts.yle.unapproved_after_reported.unapproved_after_reported.load_dotenv") as mock_load_dotenv:
        load_env_variables()
        mock_load_dotenv.assert_called_once_with(".env")


def test_aggregation_pipeline():
    class_definition = ReportedButUnapproved(
        config=FakeSettings(),
    )
    assert isinstance(class_definition.pipeline, list)
    pipeline_requirement = {"$match": {"$and": [{"reported": True}, {"aggregations.approved": False}]}}
    assert pipeline_requirement in class_definition.pipeline


def test_generate_output_filename():
    test_start_time = datetime(2022, 2, 21, 0, 0, 0)
    test_end_time = datetime(2022, 2, 22, 0, 0, 0)
    test_build_nr = "1"
    test_filename = generate_output_filename(test_start_time, test_end_time, test_build_nr)
    assert test_filename == "YLE_reported-but-unapproved_2022-02-21_2022-02-22_build-1.csv"


def test_write_output_csv():
    test_schedules = [
        document_data(
            # Testing Reportal URL construction
            _id=ObjectId("6222265127b5b29d980b3fe0"),
            # Testing fallback rules for empty string fields -> expected behaviour: "-"
            channel_display_name="",
            program_title="",
            alt_title="",
            program_id="",
            unique_id="",
            client_id="",
            broadcast_start_time="",
            last_edited_time="",
            last_approved_time="",
            last_reported_time="",
        ),
        document_data(
            # Testing Reportal URL construction
            _id=ObjectId("62441b20a8784d6cd7fed645"),
            # Testing fallback rules for None type fields -> expected behaviour: "-"
            channel_display_name=None,
            program_title=None,
            alt_title=None,
            program_id=None,
            unique_id=None,
            client_id=None,
            broadcast_start_time=None,
            last_edited_time=None,
            last_approved_time=None,
            last_reported_time=None,
        ),
        # Testing expected behaviour (true positive) for all fields except URL
        # Testing fallback rule for empty program_title string -> expected output: alt_title
        document_data(program_title=""),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_file = os.path.join(tmpdir, "test.csv")

        with open(tmp_file, "w"):
            reported_but_unapproved = ReportedButUnapproved(config=FakeSettings())
            reported_but_unapproved.write_output_csv(test_schedules)

            hex_pattern = re.compile(r"^[a-fA-F0-9]{24}$")

            with open(tmp_file, "r") as file_read:
                csv_reader = csv.DictReader(file_read)
                for index, row in enumerate(csv_reader):
                    if index < 2:
                        assert row.get("channel") == "-"
                        assert row.get("program_title") == "-"
                        assert row.get("program_id") == "-"
                        assert row.get("unique_id") == "-"
                        assert row.get("client_id") == "-"
                        assert row.get("broadcast_start_time") == "-"
                        assert row.get("last_edited_time") == "-"
                        assert row.get("last_approved_time") == "-"
                        assert row.get("last_reported_time") == "-"

                        if index == 0:
                            assert row.get("program_url") == "https://yle-reportal.bmat.com/programs/view/U2NoZWR1bGU6NjIyMjI2NTEyN2I1YjI5ZDk4MGIzZmUw"
                        if index == 1:
                            assert row.get("program_url") == "https://yle-reportal.bmat.com/programs/view/U2NoZWR1bGU6NjI0NDFiMjBhODc4NGQ2Y2Q3ZmVkNjQ1"

                    elif index == 2:
                        assert row.get("channel") == "Test Channel"
                        assert row.get("program_title") == "Test Alt Title"
                        assert hex_pattern.match(row.get("program_id"))
                        assert row.get("unique_id") == "0123456789"
                        assert row.get("client_id") == "ABCDEFGHIJ"
                        assert row.get("broadcast_start_time") == "01/01/2020 00:00:00"
                        assert row.get("last_edited_time") == "01/01/2020 00:00:00"
                        assert row.get("last_approved_time") == "01/01/2020 00:00:00"
                        assert row.get("last_reported_time") == "01/01/2020 00:00:00"
