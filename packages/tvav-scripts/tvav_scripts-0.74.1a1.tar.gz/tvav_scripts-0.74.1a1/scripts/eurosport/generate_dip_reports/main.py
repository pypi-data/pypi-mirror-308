import os
import logging
from mongoengine import connect
from tqdm import tqdm
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from eurosport.reports.report_handler.dip4.reportal_2_dip4 import Dip4Handler, Dip4PubHandler
from reportal_model import Channel
from scripts.utils.decorators import ntfy


logger = logging.getLogger("eurosport-dip-reports")

class Config:
    def __init__(self) -> None:
        if __name__ == "__main__":
            self.parent_dir = Path(__file__).parent
        else:
            self.parent_dir = Path(os.getcwd())

        self.reports_dir = self.parent_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.mongo_uri = os.getenv("MONGO_URI")



@ntfy()
def generate_channel_reports(channel, report_generator_dip4, report_generator_dip4_pub, config):
    for month in tqdm([4, 5, 6], leave=False):
        start_time = datetime(2024, month, 1)
        end_time = datetime(2024, month + 1, 1)

        data, _, name = report_generator_dip4.generate_report(
            channel=channel,
            start_time=start_time,
            end_time=end_time
        )

        with (config.reports_dir / name).open("wb") as f:
            f.write(data)

        logger.info("{} Written".format(name))

        data, _, name = report_generator_dip4_pub.generate_report(
            channel=channel,
            start_time=start_time,
            end_time=end_time
        )
        name = "PUB_" + name

        with (config.reports_dir / name).open("wb") as f:
            f.write(data)

        logger.info("{} Written".format(name))


@ntfy()
def main():
    config = Config()
    with connect(host=config.mongo_uri):
        report_generator_dip4 = Dip4Handler()
        report_generator_dip4_pub = Dip4PubHandler()

        for channel in tqdm(Channel.objects(), total=4):
            generate_channel_reports(channel, report_generator_dip4, report_generator_dip4_pub, config)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    main()
