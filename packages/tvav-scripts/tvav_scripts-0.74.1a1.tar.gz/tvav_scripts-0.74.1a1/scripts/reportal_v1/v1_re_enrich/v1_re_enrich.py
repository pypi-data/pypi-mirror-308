"""Script to re-enrich music works with provided single view ids"""

import csv
import logging
import os
from datetime import datetime

from api_clients.single_view import SingleViewClient
from dotenv import load_dotenv
from mongoengine import connect
from music_report.tracks import Tracks

from gema.database_model import MusicWork
from gema.matching.interceptor.ard import mutators
from gema.matching.music_report import GemaMusicReportManager
from tqdm import tqdm

load_dotenv()
logger = logging.getLogger(__name__)


class FakeMatch:
    album = None
    label = None


def update_music_work_with_new_metadata(music_work: MusicWork) -> None:
    """Replace all music works with new data from music_work."""
    for database_music_work in MusicWork.objects(single_view_id=music_work.single_view_id).no_cache():
        music_work.created_at = database_music_work.created_at
        music_work.updated_at = datetime.utcnow()

        MusicWork._get_collection().replace_one({"_id": database_music_work.id}, music_work.to_mongo().to_dict())


def get_track_from_single_view(sv_id: str, mr: GemaMusicReportManager) -> Tracks:
    """Return single view track from single vie id."""
    single_view_sr = mr.sv.get_entity('sound-recording', id=sv_id)
    sv_track = mutators.get_track(singleview_client=mr.sv, sound_recording=single_view_sr)
    track = Tracks(music_title=single_view_sr.display_title or sv_track.display_title,
                   duration=None,
                   artists=None,
                   work_creators=None,
                   match=FakeMatch,
                   start_time=None,
                   end_time=None,
                   music_type="music",
                   identified=True,
                   sound_recording=single_view_sr,
                   track_info=sv_track,
                   source=sv_track.source,
                   service_id=sv_track.service_id
                   )
    return track


def re_enrich(single_view_ids: list) -> None:
    """re-enrich all music works that have a single view ids from provided list."""
    single_view_uri = os.getenv("SINGLE_VIEW_URL")

    mr = GemaMusicReportManager(
        single_view_api_client=SingleViewClient(base_url=single_view_uri)
    )

    for sv_id in tqdm(iterable=single_view_ids, desc="single view ids checked"):
        try:
            track = get_track_from_single_view(sv_id, mr)
            mw = MusicWork()
            mr.enrich_music_work(mw, track)

            update_music_work_with_new_metadata(mw)
        except Exception as e:
            logger.error("Error during re-enrichment of single view ids: %s - %s", sv_id, e)


def get_single_view_ids_from_file(file_path: str) -> list:
    """Return a list of id from .csv file"""
    with open(file_path, 'r') as file:
        return [row.get('sv_sr_id') for row in csv.DictReader(file)]


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    mongo_uri = os.getenv("MONGO_URI")
    connect(host=mongo_uri)

    file_path = os.getenv("FILE_TO_USE")
    single_view_ids = get_single_view_ids_from_file(file_path)

    re_enrich(single_view_ids)
    logger.info("Enrichment finished")
