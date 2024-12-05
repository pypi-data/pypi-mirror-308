from datetime import datetime
from typing import Optional

from mongoengine import Document
from mongoengine.fields import BooleanField, DateTimeField, DictField, StringField
from pydantic import Field
from pydantic_settings import BaseSettings


class File(Document):
    path = StringField()
    namespace = StringField()
    data = DictField()
    created = DateTimeField()
    updated = DateTimeField()
    error = BooleanField()
    status = StringField()
    meta = {"strict": False}


class QAPostReportingConfig(BaseSettings):
    """Loading the dotenv to a config model"""

    bazaar_storage_uri: str = Field(..., env="bazaar_storage_uri")
    bazaar_db_uri: str = Field(..., env="bazaar_db_uri")
    tvav_mongo_uri: str = Field(..., env="tvav_mongo_uri")
    min_report_date: datetime
    max_report_date: Optional[datetime] = None
    reports_folder: str = Field(..., env="reports_folder")
    main_csv_path: str = Field(..., env="main_csv_path")
    generate_stats: bool = False
