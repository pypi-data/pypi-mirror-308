import base64
import json
import os
from typing import Iterable, Tuple

from mongoengine import connect
from openpyxl import Workbook
from reportal_model import AvWork, DigitalUsage


MONGO_URI = os.getenv("MONGO_URI")
BACKUP_MONGO_URI = os.getenv("BACKUP_MONGO_URI")
HEADERS = (
    "Reportal DU URL",
    "Reportal Cuesheet URL",
    "Cuesheet reported",
    "DU reported",
    "Publication start time",
    "Start time",
    "End time"
)
BASE_REPORTAL_URL = "https://nrk-reportal.bmat.com"
CUESHEET_URL = f"{BASE_REPORTAL_URL}/cuesheets/view/{{}}"
DU_URL = f"{BASE_REPORTAL_URL}/digital-usages/view/{{}}/{{}}"


def get_models_from_file(filename: str) -> Tuple[Iterable[DigitalUsage], Iterable[AvWork]]:
    with open(filename, "r") as in_file:
        data = json.load(in_file)
    du_ids, av_ids = set(), set()
    for transmission in data["transmissions"]:
        du_ids.add(transmission["transmission_id"])
        av_ids.add(transmission["production"]["production_id"])
    avs = {a.id: a for a in AvWork.objects(id__in=av_ids)}
    print('Arrived here')
    return {d.id: {"du": d, "av": avs[d.av_work.id]} for d in DigitalUsage.objects(id__in=du_ids)}


def generate_report(input_filename: str, output_filename: str):
    dus = get_models_from_file(input_filename)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(HEADERS)
    for i, digital_usage_info in enumerate(dus.values(), 1):
        du = digital_usage_info["du"]
        av_work_b64 = base64.urlsafe_b64encode(f"AvWork:{digital_usage_info['av'].id}".encode()).decode().replace('=', '%3D')
        du_b64 = base64.urlsafe_b64encode(f"DigitalUsage:{du.id}".encode()).decode().replace('=', '%3D')
        worksheet.append((
            CUESHEET_URL.format(av_work_b64),
            DU_URL.format(du_b64, av_work_b64),
            du.av_work.reported,
            du.reported,
            du.publication_start_time,
            du.start_time,
            du.end_time
        ))
        print(f'{i}')
    workbook.save(output_filename)


if __name__ == '__main__':
    connect(host=BACKUP_MONGO_URI)
    generate_report("2022-11-01-daily_report-PODCASTS.json", "PODCASTS.xlsx")
