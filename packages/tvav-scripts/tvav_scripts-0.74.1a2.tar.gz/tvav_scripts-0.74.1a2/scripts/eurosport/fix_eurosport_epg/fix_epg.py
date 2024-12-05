import argparse
import logging
import os
import time
from typing import Dict

from dotenv import load_dotenv
from mongoengine import QuerySet, connect, disconnect
from reportal_model.schedule import Schedule

logger = logging.getLogger(__name__)

load_dotenv()

PREFIX = "EXTRAS_"
PREFIX_LEN = len(PREFIX)


def get_schedules(tag) -> QuerySet:
    return Schedule.objects.filter(schedule_ids__eurosport_tag__startswith=tag)


def prepare_replacement_dict() -> Dict[str, str]:
    res = {}
    for key, value in os.environ.items():
        if key.startswith(PREFIX):
            res[key[PREFIX_LEN:].lower()] = value
    return res


def run(tag: str, dry_run: bool = False, timeout: float = 0, backup: bool = False) -> None:
    logger.info("Starting")
    replacement_dict = prepare_replacement_dict()
    total = get_schedules(tag).count()
    counter = 0
    for schedule in get_schedules(tag):
        if backup:
            with open(f"backup_{schedule.id}.json", "w") as f:
                f.write(schedule.to_json())

        for key, value in replacement_dict.items():
            schedule.extras[key] = value

        counter += 1
        logger.info("Total %s, processed %s", total, counter)

        if dry_run:
            logger.info("Dry run, schedule %s, extras %s", schedule.id, schedule.extras)
            continue

        schedule.save()
        logger.info("Schedule %s is updated", schedule.id)

        if timeout:
            time.sleep(timeout)

    logger.info("Finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--backup", action="store_true", help="Save backups")
    parser.add_argument("-d", "--dry_run", action="store_true", help="Dry run")
    parser.add_argument(
        "--loglevel",
        action="store",
        dest="loglevel",
        choices=["DEBUG", "INFO", "ERROR"],
        default="INFO",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.loglevel),
        format="%(asctime)s %(levelname)-8s %(funcName)-30s %(lineno)-5s %(message)s",
    )

    mongo_uri = os.getenv("MONGO_URI")
    connect(host=mongo_uri)

    tag = os.getenv("TAG")
    timeout = float(os.getenv("TIMEOUT", 0))
    run(tag, dry_run=args.dry_run, timeout=timeout, backup=args.backup)
    disconnect()
