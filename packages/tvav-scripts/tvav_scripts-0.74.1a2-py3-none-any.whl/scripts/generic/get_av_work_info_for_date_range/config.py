from datetime import datetime
from pydantic_settings import BaseSettings
from scripts.utils.common_config_models import  MongoDBSettings


class GetAvWorkInfoSettings(BaseSettings):
    class Config:
        env_nested_delimiter = '__'

    mongodb: MongoDBSettings = MongoDBSettings(db_name="tv-av-prod")
    start_time_min: datetime
    start_time_max: datetime
