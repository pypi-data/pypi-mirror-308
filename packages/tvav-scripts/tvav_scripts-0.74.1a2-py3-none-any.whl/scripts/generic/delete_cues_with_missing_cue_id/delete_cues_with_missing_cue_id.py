import os

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from tqdm import tqdm


from scripts.generic.object_ids_to_reportal_urls.object_ids_to_reportal_urls import object_ids_to_reportal_urls


def get_db(mongo_uri: str, mongo_user: str, mongo_db: str):
    return MongoClient(host=mongo_uri.format(mongo_user, mongo_db)).get_database(mongo_db)


def delete_cues_with_missing_cue_id(mongo_uri: str, mongo_user: str, mongo_db: str, custom_extras_flag: str):

    query = {
        "cuesheet.cues.0": {"$exists": True},
        "cuesheet.cues._id": None,
    }
    db = get_db(mongo_uri, mongo_user, mongo_db)
    av_works = db.av_work.find(query)

    if db.av_work.count_documents(query) == 0:
        return []

    # Fix AvWorks in memory
    docs_affected = []
    bulk_operations = []
    for av_work in tqdm(av_works):
        # Get cues to be deleted
        cues_to_be_deleted = []
        for cue_idx, cue in enumerate(av_work["cuesheet"]["cues"]):
            if cue.get("_id") is None:
                cues_to_be_deleted.append(cue)

        # Remove cues from av_work
        for cue in cues_to_be_deleted:
            av_work["cuesheet"]["cues"].remove(cue)

        # Add flag to extras to trace the change
        av_work["extras"][custom_extras_flag] = len(cues_to_be_deleted)
        docs_affected.append(str(av_work["_id"]))
        bulk_operations.append(
            UpdateOne(
                filter={'_id': av_work["_id"]},
                update={'$set': {"cuesheet": av_work["cuesheet"], "extras": av_work["extras"]}}
            )
        )

    # Update AvWorks in DB
    db.av_work.bulk_write(bulk_operations)

    # Return list of affected
    return docs_affected


if __name__ == "__main__":
    load_dotenv()

    # Getting env vars
    mongo_uri = os.getenv("MONGO_URI")
    mongo_user = os.getenv("MONGO_USER")
    mongo_db = os.getenv("MONGO_DB")
    custom_extras_flag = os.getenv("CUSTOM_EXTRAS_FLAG")
    doc_type = os.getenv("DOC_TYPE")
    reportal_url = os.getenv("REPORTAL_URL")

    # The actual work
    docs_ids_affected = delete_cues_with_missing_cue_id(mongo_uri, mongo_user, mongo_db, custom_extras_flag)

    # Report affected docs
    object_ids_to_reportal_urls(doc_type="AvWork", reportal_url=reportal_url, object_ids_string="\n".join(docs_ids_affected))
