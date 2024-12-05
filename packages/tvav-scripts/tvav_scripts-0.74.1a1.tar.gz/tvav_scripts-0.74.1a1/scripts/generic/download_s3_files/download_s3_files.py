import json
import os

from bazaar import FileSystem
from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import Document, connect
from mongoengine.fields import StringField, DateTimeField, IntField, BooleanField
from tqdm import tqdm


class File(Document):
    path = StringField()
    namespace = StringField()
    created = DateTimeField()
    updated = DateTimeField()
    size = IntField()
    error = BooleanField()
    meta = {"strict": False}


def download_epg_file(file: File, mongo_uri, s3_bazaar_uri):
    """Given the ID of a file entity, return the data as a file"""
    fs = FileSystem(
        storage_uri=s3_bazaar_uri,
        db_uri=mongo_uri,
    )

    # Removing some additional details that were added due to files being moved to /ok/ folder.
    file_name = file.path.replace("/ok/", "").replace("/./", "").replace("/", "")
    system_path = os.getcwd()

    if os.path.exists(os.path.join(system_path, file_name)):
        print(f"File {file_name} already exists in {system_path}")
        return

    try:
        d = fs.get(path=file.path, namespace=file.namespace)
        with open(os.path.join(system_path, file_name), "wb") as file:
            print("New file", file_name)
            file.write(d)
    except Exception as e:
        print("ERROR", file_name, e)


def download_s3_files(
    mongo_uri: str,
    mongo_tv_av_prod_user: str,
    mongo_bazaar_user: str,
    s3_bazaar_uri: str,
    ids: str,
):
    try:
        id_list = json.loads(ids)
    except TypeError:
        print("Bad ids input. Use JSON format")
        return

    params = {"id__in": [ObjectId(_id) for _id in id_list]}

    with connect(host=mongo_uri.format(mongo_tv_av_prod_user, "tv-av-prod")):
        files = File.objects(**params)

        for file in tqdm(files, total=files.count()):
            download_epg_file(
                file=file,
                mongo_uri=mongo_uri.format(mongo_bazaar_user, "bazaar-prod"),
                s3_bazaar_uri=s3_bazaar_uri
            )


if __name__ == "__main__":
    load_dotenv()
    download_s3_files(
        mongo_uri=os.getenv("MONGO_URI"),
        mongo_tv_av_prod_user=os.getenv("MONGO_TV_AV_PROD_USER"),
        mongo_bazaar_user=os.getenv("MONGO_BAZAAR_USER"),
        s3_bazaar_uri=os.getenv("S3_BAZAAR_URI"),
        ids=os.getenv("IDS"),
    )
