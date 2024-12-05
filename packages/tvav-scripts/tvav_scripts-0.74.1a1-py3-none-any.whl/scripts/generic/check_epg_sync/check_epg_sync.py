import logging

from dotenv import load_dotenv
from epg_processor.epg_sync import EPGSyncClient
from epg_processor.match_importer.missing_work_packages import \
    create_work_package
from mongoengine import connect
from reportal_model import Channel, Schedule

from scripts.generic.check_epg_sync import models
from scripts.generic.check_epg_sync.models import (ChannelParameters,
                                                   ScheduleParameters)

load_dotenv()
logging.basicConfig(level=logging.INFO)


class CheckEpgSyncScript:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = models.Config()

    def run(self):
        epg_sync_client = EPGSyncClient(username=self.config.epg_sync_username, password=self.config.epg_sync_password)

        schedule_parameters = ScheduleParameters()
        schedule_parameters.convert_dates_to_utc_from_user_timezone(self.config.user_timezone)
        if not self.config.only_no_epg_sync:
            schedule_parameters.error_description = None

        channel_parameters = ChannelParameters()

        with connect(host=self.config.get_mongodb_connection_string()):
            if Schedule.objects(**schedule_parameters.dict()).count() == 0:
                self.logger.info("No schedules found with missing epg sync for the date range specified")
                return

            query = {}
            if channel_parameters.display_name:
                self.logger.info("Selecting channel %s", channel_parameters.display_name)
                query["display_name"] = channel_parameters.display_name
            else:
                self.logger.info("Selecting ALL CHANNELS")

            channels = list(Channel.objects(**query))
            if not channels:
                self.logger.warning("No channels found")
                return

            self.logger.info("Found %s channels", [ch.display_name for ch in channels])

            total = create_work_package(
                epg_sync_client=epg_sync_client,
                channels=channels,
                start_time=schedule_parameters.start_time,
                end_time=schedule_parameters.end_time,
                work_package_name=self.config.epg_work_package_name,
                interval_seconds=self.config.epg_sync_interval_seconds,
                sample_size=self.config.epg_sync_sample_size,
            )
            self.logger.info(f"{self.config.epg_work_package_name} package created containing {total} EPGs")


if __name__ == "__main__":
    script = CheckEpgSyncScript()
    script.run()
