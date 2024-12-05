import csv
import logging
from dotenv import load_dotenv
from mongoengine import connect
from tqdm import tqdm

from reportal_model import Schedule

from scripts.generic.get_av_work_info_for_date_range.config import GetAvWorkInfoSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("get_av_work_info")


if __name__ == "__main__":
    load_dotenv()
    config = GetAvWorkInfoSettings()  # type: ignore

    with connect(host=config.mongodb.get_mongo_db_uri()):
        logger.info("Starting")
        programs = Schedule.objects.aggregate([
            {"$match": {
                "start_time": {
                    "$gte": config.start_time_min,
                    "$lt": config.start_time_max,
                },
            }},
            {"$lookup": {
                "from": "av_work",
                "as": "av_work",
                "localField": "av_work",
                "foreignField": "_id",
            }},
            {"$unwind": "$av_work"},
            {"$project": {
                "_id": 0,
                "start_time": 1,
                "title": "$av_work.titles.original_title",
                "program_id": "$av_work.work_ids.program_id",
            }},
        ])

        with open("report.csv", mode="wt") as f:
            logger.info("Writing report")
            writer = csv.writer(f)
            writer.writerow(["start_time", "title", "program_id"])
            for program in tqdm(programs):
                program["start_time"] = program["start_time"].strftime("%d/%m/%y %H:%M:%S")
                writer.writerow(program.values())
            
    logger.info("Done")
