import base64
import os
from datetime import datetime
from dotenv import load_dotenv
from mongoengine import connect
from tqdm import tqdm

from reportal_model import Schedule


load_dotenv()


def get_pipeline() -> list:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    return [
        {"$match": {"start_time": {
            "$gte": datetime.strptime(os.getenv("START_DATE"), DATETIME_FORMAT),
            "$lte": datetime.strptime(os.getenv("END_DATE"), DATETIME_FORMAT),
        }}},
        {"$group": {"_id": "$av_work"}},
        {"$lookup": {
            "from": "schedule",
            "localField": "_id",
            "foreignField": "av_work",
            "as": "schedule",
        }},
        {"$unwind": "$schedule"},
        {"$match": {"schedule.main_replica": True}},
        {"$group": {"_id": "$_id", "schedule": {"$first": "$schedule._id"}}},
        {"$project": {
            "_id": 0,
            "schedule": {"$toString": "$schedule"},
        }},
    ]


def get_reportal_url(reportal_domain_name: str, sch_id: str) -> str:
    b64 = base64.b64encode(f"Schedule:{sch_id}".encode("utf-8")).decode("utf-8")
    return f"https://{reportal_domain_name}/programs/view/{b64}"


if __name__ == "__main__":
    reportal_domain_name = os.getenv("REPORTAL_DOMAIN_NAME") or "reportal-domain-name.bmat.com"

    with connect(host=os.getenv("MONGO_URI")), open(
        "reportal_urls.csv",
        mode="wt",
        encoding="utf-8"
    ) as f:
        schedules = Schedule.objects.aggregate(get_pipeline())
        for schedule_id in tqdm(schedules):
            reportal_url = get_reportal_url(reportal_domain_name, schedule_id["schedule"])
            f.write(reportal_url + "\n")
