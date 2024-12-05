import logging
import os
from datetime import datetime
from typing import Optional

from bazaar import FileSystem
from mongoengine import connect
from tqdm import tqdm

from scripts.yle.qa_post_reporting.model import File

logger = logging.getLogger("YLE-QA-POST-REPORT-UTILS ")


def download_file_from_bazaar(file: File, system_path: str, bazaar_storage_uri: str, bazaar_db_uri: str) -> None:
    fs = FileSystem(storage_uri=bazaar_storage_uri, db_uri=bazaar_db_uri)

    # Removing some additional details that could be due to files being moved.
    # For ex: / or /ok/
    file_name = file.path.replace("/ok/", "").replace("/./", "").replace("/", "")
    out_path = system_path + "/" + file_name

    # Don't download if file already exists
    if not os.path.exists(out_path):
        try:
            d = fs.get(path=file.path, namespace=file.namespace)
            with open(out_path, "wb") as f:
                f.write(d)
        except Exception as e:
            logger.error("Error Downloading File", file_name, e)


def download_yle_report_files(
    min_report_date: datetime,
    system_path: str,
    bazaar_storage_uri: str,
    bazaar_db_uri: str,
    tvav_mongo_uri: str,
    namespace: str = "yle-reports-fortnightly",
    max_report_date: Optional[datetime] = None,
):
    params = {
        "created__gte": min_report_date,
        "namespace": namespace
    }
    if max_report_date:
        params["created__lte"] = max_report_date

    with connect(host=tvav_mongo_uri):
        files = File.objects(**params)  # type: ignore
        for f in tqdm(files, total=files.count()):
            download_file_from_bazaar(
                file=f,
                system_path=system_path,
                bazaar_storage_uri=bazaar_storage_uri,
                bazaar_db_uri=bazaar_db_uri
            )
