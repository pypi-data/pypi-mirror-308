from pydantic_settings import BaseSettings
from scripts.utils.common_config_models import MongoDBSettings


class SetAsApprovedSettings(BaseSettings):
    class Config:
        env_nested_delimiter = '__'

    mongodb: MongoDBSettings = MongoDBSettings()

    # input csv file
    input_csv_file: str = "input.csv"
    # work_id to be used to find programs in the DB
    work_id: str = "program_id"
