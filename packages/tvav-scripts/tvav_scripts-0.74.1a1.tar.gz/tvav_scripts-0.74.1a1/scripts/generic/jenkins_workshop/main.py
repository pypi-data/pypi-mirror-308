import logging
from dotenv import load_dotenv
from mongoengine import connect

from reportal_model import AvWork

from scripts.generic.jenkins_workshop.config import JenkinsWorkshopSettings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jenkins-worksho")


if __name__ == "__main__":
    load_dotenv()
    config = JenkinsWorkshopSettings()  # type: ignore

    with connect(host=config.mongodb.get_mongo_db_uri()):
        logger.info("we were able to connect to mongo database!")
        av_work_count = AvWork.objects.count()
        logger.info(f"n_av_works={av_work_count}")

    with open("report.csv", "wt") as f:
        f.write("n_av_works\n")
        f.write(str(av_work_count))
        
    logger.info("Done")
