import datetime
import json
import os
from typing import List

from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, MusicWork
from tqdm import tqdm

from scripts.generic.object_ids_to_reportal_urls.object_ids_to_reportal_urls import \
    object_ids_to_reportal_urls

load_dotenv()


def get_av_work(aw_id: str) -> AvWork:
    return AvWork.objects.get(id=ObjectId(aw_id))


def get_music_work(mw_id: str) -> MusicWork:
    return MusicWork.objects.get(id=ObjectId(mw_id))


def replace_music_work(aw: AvWork, target_mw: MusicWork, final_mw: MusicWork, custom_prefix: str):
    not_found = True
    for idx, cue in enumerate(aw.cuesheet.cues):
        if cue.music_work and cue.music_work.id == target_mw.id:
            not_found = False
            print(f"AvWork:{aw.id} - Cue no {idx} = {target_mw.id} -> {final_mw.id}")
            cue.music_work = final_mw
            cue.extras[f"{custom_prefix}_replaced_{target_mw.id}_with_{final_mw.id}"] = datetime.datetime.now()
    if not_found:
        print(f"NOT FOUND AvWork:{aw.id}")
        return
    aw.save()


if __name__ == "__main__":
    mongo_uri = os.getenv("MONGO_URI")
    mongo_user = os.getenv("MONGO_USER")
    mongo_db = os.getenv("MONGO_DB")
    target_music_work = os.getenv("TARGET_MUSIC_WORK")
    final_music_work = os.getenv("FINAL_MUSIC_WORK")
    custom_prefix = os.getenv("CUSTOM_PREFIX")

    with open("av_works_to_be_affected.json", "rt") as f:
        av_works_ids: List[str] = json.load(f)

    with connect(host=mongo_uri.format(mongo_user, mongo_db)):
        target_mw = get_music_work(target_music_work)
        final_mw = get_music_work(final_music_work)
        for aw_id in tqdm(av_works_ids):
            aw = get_av_work(aw_id)
            replace_music_work(aw, target_mw, final_mw, custom_prefix)

    # Report programs affected
    object_ids_to_reportal_urls(
        doc_type="AvWork",
        reportal_url=os.getenv("REPORTAL_URL"),
        object_ids_string="\n".join(av_works_ids)
    )
