import base64
import datetime
import os
from dotenv import load_dotenv


def clean(object_id: str):
    return object_id.replace('ObjectId("', '').replace('")', '').replace(',', '').replace('\n', '')


def object_ids_to_reportal_urls(doc_type: str, reportal_url: str, object_ids_string: str):
    valid_doc_types = ["AvWork", "Schedule", ]

    if doc_type not in valid_doc_types:
        print(f"Unrecognized doc_type: {doc_type}")
        exit(1)

    if doc_type == "AvWork":
        reportal_url += "/cuesheets/view/{}"
    elif doc_type == "Schedule":
        reportal_url += "/programs/view/{}"

    object_ids = [clean(obj_id) for obj_id in object_ids_string.split('\n')]
    if '' in object_ids:
        object_ids.remove('')

    reportal_urls = [
        reportal_url.format(
            base64.b64encode(f"{doc_type}:{obj_id}".encode("utf-8")).decode("utf-8").replace("=", "%3D")
        ) for obj_id in object_ids
    ]

    with open(f'{datetime.datetime.now()}_programs_affected.txt', 'wt') as f:
        f.writelines([line + '\n' for line in reportal_urls])
    print(f"{len(reportal_urls)} reportal_urls written to reportal_urls.txt")


if __name__ == "__main__":
    load_dotenv()

    doc_type = os.getenv("DOC_TYPE")
    reportal_url = os.getenv("REPORTAL_URL")

    with open('object_ids.txt', 'rt') as f:
        object_ids_string = f.read()

    object_ids_to_reportal_urls(doc_type, reportal_url, object_ids_string)
