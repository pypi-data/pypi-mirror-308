import logging
import os
import uuid
from typing import Iterable

from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork
from scripts.generic.object_ids_to_reportal_urls.object_ids_to_reportal_urls import object_ids_to_reportal_urls

logger = logging.getLogger("nrk-program_ids")


def get_av_works():
    av_works = AvWork.objects(__raw__={
        "work_ids.program_id": None
    })
    logger.info("Found %d AvWorks with missing program_id" % av_works.count())
    return av_works


def _generate_program_id() -> str:
    return str(int.from_bytes(uuid.uuid1().bytes, byteorder='big') >> 64)


def create_unique_program_ids_for_all(
        mongo_uri: str,
        mongo_user: str,
        mongo_db: str,
) -> Iterable[str]:

    programs_affected = []

    with connect(host=mongo_uri.format(mongo_user, mongo_db)):
        for aw in get_av_works():
            # Just to double-check
            if aw.work_ids.get("program_id") is not None:
                continue
            program_id = _generate_program_id()
            aw.work_ids["program_id"] = program_id
            aw.save()
            programs_affected.append(str(aw.id))

    return programs_affected


if __name__ == "__main__":
    load_dotenv()
    programs_affected = create_unique_program_ids_for_all(
        mongo_uri=os.getenv("MONGO_URI"),
        mongo_user=os.getenv("MONGO_USER"),
        mongo_db=os.getenv("MONGO_DB"),
    )
    object_ids_to_reportal_urls(
        doc_type="AvWork",
        reportal_url=os.getenv("REPORTAL_URL"),
        object_ids_string="\n".join(programs_affected)
    )
