import logging
from pprint import pprint
from typing import Optional

from dotenv import load_dotenv
from pymongo import InsertOne, MongoClient
from pymongo.errors import BulkWriteError
from tqdm import tqdm

from scripts.generic.copy_backup.config import CopyBackupSettings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("copy_backup")


def get_collections_to_copy(source_db, mongo_col: Optional[str] = None) -> list[str]:
    """

    """
    db_collections = source_db.list_collection_names()

    if mongo_col:
        if mongo_col not in db_collections:
            raise ValueError(f"'{mongo_col}' is not a valid collection for '{source_db.name}' DB")
        return [mongo_col]
    return db_collections



def copy_backup(
    source: str,
    destination: str,
    max_batch_size: int = 10_000,
    mongo_col: Optional[str] = None,
    query: Optional[dict] = None,
):
    """
    Will copy all documents matching query from an origin collection into a target collection.
    The copy will be stored in a collection named "[my_name]_[collection]_backup_[date in ISO-8601]"
    """

    if query is None:
        query = {}

    source_db = MongoClient(host=source).get_database()
    dest_db = MongoClient(host=destination).get_database()

    logger.info("Successfully connected to both source and destination DBs")

    collections_to_copy = get_collections_to_copy(source_db, mongo_col)
    print(f"Will copy the following collections from '{source_db.name}' --> '{dest_db.name}'")
    pprint(collections_to_copy)
    ans = input("Continue? y/N\n")

    if ans != "y":
        return

    logger.info("Copying %d collections from '%s' to '%s'" % (
        len(collections_to_copy),
        source_db.name,
        dest_db.name
    ))

    with tqdm(
        collections_to_copy,
        desc="Collections",
        postfix=f"- Collection name: {collections_to_copy[0]}"
    ) as pbar:
        for col in pbar:
            pbar.postfix = f"- Collection name: {col}"

            docs = source_db[col].find(query)
            docs_count = source_db[col].count_documents(query)

            n_batches, mod_docs_count = divmod(docs_count, max_batch_size)
            logger.info("Sending %d batches of size %d + a last one of %d" % (
                n_batches,
                max_batch_size,
                mod_docs_count
            ))

            # n_batches + 1 to send the mod_docs_count except if mod_docs_count == 0
            for batch_number in tqdm(
                range(n_batches + 1 if mod_docs_count != 0 else n_batches),
                desc="Doc batches",
            ):
                if batch_number == n_batches:
                    # last batch
                    docs_count_to_use = mod_docs_count
                else:
                    docs_count_to_use = max_batch_size

                batch = [next(docs) for _ in range(docs_count_to_use)]

                operations = [
                    InsertOne(doc)
                    for doc in batch
                ]

                try:
                    _ = dest_db[col].bulk_write(operations, ordered=False)
                except BulkWriteError as bwe:
                    raise RuntimeError(bwe.details)

    logger.info("Copy backup OK")


if __name__ == "__main__":
    load_dotenv()
    settings = CopyBackupSettings()
    copy_backup(**settings.model_dump())
