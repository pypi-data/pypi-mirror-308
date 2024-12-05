import json
import os
from typing import Iterable, Tuple

from mongoengine import connect, disconnect
from pymongo import UpdateOne
from reportal_model import AvWork, DigitalUsage


MONGO_URI = os.getenv("MONGO_URI")
BACKUP_MONGO_URI = os.getenv("BACKUP_MONGO_URI")


def get_models_from_file(filename: str) -> Tuple[Iterable[DigitalUsage], Iterable[AvWork]]:
    with open(filename, "r") as in_file:
        data = json.load(in_file)
    du_ids = set()
    for transmission in data["transmissions"]:
        du_ids.add(transmission["transmission_id"])
    return DigitalUsage.objects(id__in=du_ids)


def generate_report(input_filename: str):
    dus = get_models_from_file(input_filename)
    du_ops, av_ops = [], []
    count = dus.count()
    for i, du in enumerate(dus, 1):
        du_ops.append(UpdateOne(
            {'_id': du.id},
            {'$set': {
                'reported': du['reported'],
                'extras.reported_daily': du.extras.get('reported_daily', False),
                'extras.reported_by': du.extras.get('reported_by'),
            }}
        ))
        av_ops.append(UpdateOne({'_id': du.av_work.id}, {'$set': {
            'reported': du.av_work.reported,
            'extras.reported_daily': du.av_work.extras.get('reported_daily'),
            'extras.reported_by': du.av_work.extras.get('reporeted_by'),
            'history_info.reported_change': du.av_work.history_info.reported_change
        }}))
        print(f'{i}/{count}')
    disconnect()
    connect(host=MONGO_URI)
    print(DigitalUsage._get_collection().bulk_write(du_ops).raw_result)
    print(AvWork._get_collection().bulk_write(av_ops).raw_result)


if __name__ == '__main__':
    connect(host=BACKUP_MONGO_URI)
    generate_report("2022-11-01-daily_report-PODCASTS.json")
