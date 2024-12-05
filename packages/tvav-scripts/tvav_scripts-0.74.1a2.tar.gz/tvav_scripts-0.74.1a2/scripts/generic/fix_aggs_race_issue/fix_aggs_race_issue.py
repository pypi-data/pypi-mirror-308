import base64
from typing import Generator

from dotenv import load_dotenv
from mongoengine import connect
from pydantic_settings import BaseSettings
from reportal_model import AvWork, Schedule


def get_av_works_from_url_list(url_list: list[str]) -> Generator[AvWork, None, None]:
    for url in url_list:
        encoded_str = url.split("/")[-1].replace("%3D", "=")
        decoded_str = base64.b64decode(encoded_str.encode()).decode()  # AvWork:xxxxxx / Schedule:xxxxxx
        object_id = decoded_str.split(":")[-1]

        if "AvWork" in decoded_str:
            yield AvWork.objects.get(id=object_id)
            continue
        if "Schedule" in decoded_str:
            yield Schedule.objects.get(id=object_id).av_work
            continue

        raise RuntimeError("Unexpected Document '%s'" % decoded_str)


def clean_cues(av_work: AvWork) -> None:
    cue_list = [
        cue
        for cue in av_work.cuesheet.cues
        if cue.cue_index is not None
    ]
    av_work.update(cuesheet__cues=cue_list)


class FixAggsRaceIssueSettings(BaseSettings):
    mongo_uri: str = "mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority"
    mongo_credentials: str
    mongo_db: str
    url_list: list[str]

    def get_mongo_uri(self) -> str:
        return self.mongo_uri.format(self.mongo_credentials, self.mongo_db)


class FixAggsRaceIssueScript:
    def __init__(self):
        load_dotenv()
        self.settings = FixAggsRaceIssueSettings()

    def run(self):
        with connect(host=self.settings.get_mongo_uri()):
            for av_work in get_av_works_from_url_list(self.settings.url_list):
                clean_cues(av_work)


if __name__ == "__main__":
    FixAggsRaceIssueScript().run()
