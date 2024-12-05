import argparse
import logging
import os
import time
from collections import namedtuple
from typing import Optional

import boto3
from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from pymongo import UpdateOne

logger = logging.getLogger(__name__)

load_dotenv()

TV_AV_MONGO_URI = os.getenv("TV_AV_MONGO_URI")
BAZAAR_MONGO_URI = os.getenv("BAZAAR_MONGO_URI")
S3 = os.getenv("S3")
NAMESPACE = "nrk-daily-reports"
MAX_SIZE = int(os.getenv("MAX_SIZE", 400))

S3File = namedtuple("S3File", ["version_id", "is_latest", "size"])


def _get_db(host):
    disconnect()
    client = connect(host=host)
    return client.get_database()


def _get_duplicate_paths():
    db = _get_db(host=TV_AV_MONGO_URI)
    return db["file"].aggregate(
        [
            {"$match": {"namespace": NAMESPACE}},
            {"$group": {"_id": "$path", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
            {"$project": {"_id": 0, "path": "$_id"}},
        ]
    )


def get_s3_client():
    credentials, bucket = S3.split("@")
    s3_key, s3_secret = credentials.split(":")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret,
    )
    return s3_client, bucket


def _get_file_versions(s3_client, bucket, file_id):
    versions = s3_client.list_object_versions(Bucket=bucket, Prefix=file_id).get("Versions", [])
    latest_version = next(filter(lambda v: v["IsLatest"], versions))
    latest_version = S3File(version_id=latest_version["VersionId"], is_latest=latest_version["IsLatest"], size=latest_version["Size"])
    return latest_version, [v for v in versions if v["VersionId"] != latest_version.version_id]


def _process_file(file: dict, s3_client, bucket: str, dry_run=False, backup=False) -> Optional[S3File]:
    logger.info("Processing %s %s", file["name"], file["_id"])
    file_id = str(file["_id"])
    latest_version, versions = _get_file_versions(s3_client, bucket, file_id)
    if latest_version.size > MAX_SIZE:
        logger.info("Latest version %s is too big, skip deleting %s", latest_version, file_id)
        return

    versions_to_keep = [v for v in versions if v["Size"] > MAX_SIZE]
    if not versions_to_keep:
        logger.info("All versions are small enough, skip deleting %s", file_id)
        return

    versions_to_delete = [latest_version]
    versions_to_delete.extend([S3File(version_id=v["VersionId"], is_latest=v["IsLatest"], size=v["Size"]) for v in versions if v["Size"] <= MAX_SIZE])

    if dry_run:
        logger.info("Dry run, skip deleting %s", versions_to_delete)
        return

    for file in versions_to_delete:
        if backup and file.is_latest:
            logger.info("Backing up %s", file_id)
            s3_client.download_file(Bucket=bucket, Key=file_id, Filename=f"{file_id}_{file.version_id}")

        logger.info("Deleting version %s, bucket %s, key %s", file.version_id, bucket, file_id)
        s3_client.delete_object(Bucket=bucket, Key=file_id, VersionId=file.version_id)

    latest_version, _ = _get_file_versions(s3_client, bucket, file_id)
    return latest_version


def run(ids: Optional[str], dry_run: Optional[bool] = False, backup: Optional[bool] = False):
    t1 = time.time()
    logger.info("Starting")
    if ids:
        query = {"_id": {"$in": [ObjectId(id) for id in ids]}}
    else:
        paths = [path["path"] for path in _get_duplicate_paths()]
        logger.info("Found %s duplicate paths", len(paths))
        query = {"name": {"$in": paths}, "size": {"$lte": MAX_SIZE}, "namespace": NAMESPACE}

    db = _get_db(host=BAZAAR_MONGO_URI)
    s3_client, bucket_name = get_s3_client()

    files_to_update = []
    file_collection = db.get_collection("file")
    for f in file_collection.find(query):
        try:
            s3_file = _process_file(f, s3_client=s3_client, bucket=bucket_name, dry_run=dry_run, backup=backup)
            if s3_file:
                logger.info("Need to update file %s with size %s", f["_id"], s3_file.size)
                files_to_update.append(UpdateOne({"_id": f["_id"]}, {"$set": {"size": s3_file.size}}))
        except Exception as e:
            logger.exception("Failed to process %s, %s", f["_id"], e)

    if files_to_update and not dry_run:
        logger.info("Updating %s files in DB", len(files_to_update))
        file_collection.bulk_write(files_to_update, ordered=False)

    t2 = time.time()
    logger.info("Done, took %s seconds", t2 - t1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        action="store",
        dest="loglevel",
        choices=["DEBUG", "INFO", "ERROR"],
        default="INFO",
    )
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    parser.add_argument("--bazaar-file-ids", nargs="+", dest="ids", type=str)
    parser.add_argument("--backup", action="store_true", dest="backup")
    parser.add_argument("--write-log-to-file", action="store_true", dest="file_log")

    args = parser.parse_args()

    logging.basicConfig(
        filename=f"{os.path.basename(__file__)}_{time.time()}.log" if args.file_log else None,
        level=getattr(logging, args.loglevel),
        format="%(asctime)s %(levelname)-8s %(funcName)-30s %(lineno)-5s %(message)s",
    )
    run(args.ids, args.dry_run, args.backup)
