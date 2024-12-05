import os
from datetime import datetime
from dotenv import load_dotenv
from mongoengine import connect
from pymongo import UpdateOne

from eurosport.common.client_custom_values import CueUse
from eurosport.match_importer.live_music_constants import (
    IS_LIVE_EUROSPORT_TAG_EQUALS,
    IS_LIVE_EUROSPORT_TAG_TITLE_EXCLUDES,
    IS_LIVE_TITLE_INCLUDES,
    IS_NOT_LIVE_TITLE_INCLUDES
)
from eurosport.processor.epg.loader.eurosport.nomenclature import ProduitsProgrammes, ProduitsProgrammesLive
from reportal_model import Schedule, AvWork


PIPELINE = [
    {"$match": {
        "category": ProduitsProgrammes.produits,
        "cuesheet.cues.use": CueUse.LIVE_MUSIC.value,
        "$or": [
            {"work_ids.eurosport_tag": {"$nin": IS_LIVE_EUROSPORT_TAG_EQUALS}},
            {
                "titles.original_title": {
                    "$regex": "|".join(
                        ".*" + pattern + ".*" for pattern in IS_LIVE_EUROSPORT_TAG_TITLE_EXCLUDES
                    ),
                    "$options": "i",
                },
            },
            {
                "$and": [
                    {
                        "titles.original_title": {
                            "$regex": "|".join(
                                ".*" + pattern + ".*" for pattern in IS_LIVE_TITLE_INCLUDES
                            ),
                            "$options": "i",
                        },
                    },
                    {
                        "titles.original_title": {
                            "$not": {
                                "$regex": "|".join(
                                    ".*" + pattern + ".*" for pattern in IS_NOT_LIVE_TITLE_INCLUDES
                                ),
                                "$options": "i",
                            }
                        },
                    },
                ]

            },
        ],
    }},
    {"$project": {"_id": 1}},
]


if __name__ == "__main__":
    load_dotenv()

    with connect(host=os.getenv("MONGO_URI")):
        start = datetime.now()
        candidates = AvWork.objects.aggregate(PIPELINE)

        av_work_ids = [c["_id"] for c in candidates]

        print("Time taken:", datetime.now() - start)
        print("AvWork candidates to update:", len(av_work_ids))

        operations = [
            UpdateOne(
                {"_id": aw_id},
                {"$set": {"category": ProduitsProgrammesLive.produits}},
            )
            for aw_id in av_work_ids
        ]

        Schedule.objects(av_work__in=av_work_ids).update(
            set__aggregations__category=ProduitsProgrammesLive.produits,
            set__extras__live_music_checked=True,
            set__extras__RCSUP_305=True
        )

        if operations:
            AvWork._get_collection().bulk_write(operations, ordered=False)

        print("Done")
