import argparse
import concurrent.futures
import csv
import datetime
import logging
import multiprocessing
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, Channel, Schedule

logger = logging.getLogger(__name__)

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")

COMMERCIAL_MUSIC = "Commercial music"
PRODUCTION_MUSIC = "Production music"


@dataclass
class Result:
    total: float = 0
    commercial: float = 0
    production: float = 0
    unidentified: float = 0

    def __add__(self, other):
        return Result(
            total=self.total + other.total,
            commercial=self.commercial + other.commercial,
            production=self.production + other.production,
            unidentified=self.unidentified + other.unidentified,
        )


def get_channels(channel_ids: Optional[List[str]] = None) -> Dict[ObjectId, str]:
    params = {}
    if channel_ids:
        params["id__in"] = [ObjectId(_id) for _id in channel_ids]
    res = {}
    for ch in Channel.objects(**params):
        res[ch.id] = ch.full_name
    return res


def calculate_duration(av_work: AvWork) -> Result:
    cues = av_work.cuesheet.cues
    res = Result()
    for c in cues:
        mw = getattr(c, "music_work", None)
        res.total += c.duration
        if mw:
            if mw.source == COMMERCIAL_MUSIC:
                res.commercial += c.duration
            elif mw.source == PRODUCTION_MUSIC:
                res.production += c.duration
        else:
            res.unidentified += c.duration

    return res


def get_av_works(channel_id: ObjectId, start: datetime.date, end: datetime.date):
    logger.info("Getting avworks for %s from %s to %s", channel_id, start, end)
    for s in Schedule.objects.filter(channel=channel_id, start_time__gte=start, start_time__lt=end, populated=True).no_cache():
        yield s.av_work


def calculate_total(channel_id: ObjectId, start: datetime.date, end: datetime.date, connection_required: bool = True):
    if connection_required:
        connect(host=MONGO_HOST)
    total = Result()
    for a in get_av_works(channel_id, start, end):
        total += calculate_duration(a)
    return total


def write_to_csv(res: Dict[str, Result], output: str) -> None:
    with open(output, "w", newline="") as csvfile:
        fieldnames = ["channel", "total", "commercial", "production", "indetified", "unidentified"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for channel, duration in res.items():
            writer.writerow(
                {
                    "channel": channel,
                    "total": round(duration.total),
                    "commercial": round(duration.commercial),
                    "production": round(duration.production),
                    "indetified": round(duration.production + duration.commercial),
                    "unidentified": round(duration.unidentified),
                }
            )


def report(start: datetime.date, end: datetime.date, channel_ids: Optional[List[str]] = None, output="duration_report.csv", max_workers=1) -> None:
    logger.info("Starting report from %s, to %s", start, end)
    t1 = time.time()

    connect(host=MONGO_HOST)
    channels = get_channels(channel_ids)
    channel_ids = list(channels.keys())
    num_channels = len(channel_ids)
    res = {}

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for id_, total in zip(channel_ids, executor.map(calculate_total, channel_ids, [start] * num_channels, [end] * num_channels)):
            channel_name = channels[id_]
            res[channel_name] = total
            logger.info("total %s %s", channel_name, total)

    write_to_csv(res, output)
    t2 = time.time()
    logger.info("Finished reporting %s", t2 - t1)


def parse_date(s) -> datetime.date:
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        action="store",
        dest="loglevel",
        choices=["DEBUG", "INFO", "ERROR"],
        default="INFO",
    )
    parser.add_argument("--start", action="store", dest="start", type=str, help="start date, format YYYY-MM-DD")
    parser.add_argument("--end", action="store", dest="end", type=str, help="end date, format YYYY-MM-DD")
    parser.add_argument("--channel-ids", nargs="+", dest="ids", type=str)
    parser.add_argument("--output", action="store", dest="output", type=str, default="duration_report.csv", help="output file name")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.loglevel),
        format="%(asctime)s %(levelname)-8s %(funcName)-30s %(lineno)-5s %(message)s",
    )
    start = parse_date(args.start)
    end = parse_date(args.end)
    max_workers = multiprocessing.cpu_count() * 2

    report(start, end, args.ids, args.output, max_workers)
