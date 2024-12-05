import pytz
from datetime import datetime
from pydantic import Field, BaseSettings, validator
from typing import Optional

from scripts.utils.models import CustomLoadFromEnvModel


class Config(BaseSettings):
    mongo_credentials: str
    mongo_db: str
    epg_sync_username: str
    epg_sync_password: str
    epg_sync_interval_seconds: int = 14400
    epg_sync_sample_size: int = 3
    epg_work_package_name: str
    user_timezone: str = "UTC"
    only_no_epg_sync: bool = True

    @validator("user_timezone", pre=False, always=True)
    def update_user_timezone(cls, value, values):
        return pytz.timezone(value)

    def get_mongodb_connection_string(self) -> str:
        return (
            "mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority".format(
                self.mongo_credentials,
                self.mongo_db
            )
        )


class ScheduleParameters(CustomLoadFromEnvModel):
    # TODO: Add more schedule parameters as needed
    start_time: datetime = Field(..., env="start_time", alias="start_time__gte")
    end_time: datetime = Field(..., env="end_time", alias="start_time__lt")
    error_description: str = "No epg sync"

    def convert_dates_to_utc_from_user_timezone(self, user_timezone):
        user_timezone_start_time = user_timezone.localize(self.start_time)
        user_timezone_end_time = user_timezone.localize(self.end_time)
        self.start_time = user_timezone_start_time.astimezone(pytz.utc)
        self.end_time = user_timezone_end_time.astimezone(pytz.utc)


class ChannelParameters(CustomLoadFromEnvModel):
    # TODO: Add more channels parameters as needed
    display_name: Optional[str] = Field(None, env="channel_display_name")
