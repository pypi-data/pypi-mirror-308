from datetime import datetime, date
from pydantic import BaseSettings
from typing import Union


class MediasetFixMainReplicaAndOriginalScheduleConfig(BaseSettings):
    mongo_uri: str = "mongodb+srv://{mongo_credentials}@bmat-tvav-prod.yq6o5.mongodb.net/{mongo_db}?retryWrites=true&w=majority"
    mongo_db: str
    mongo_credentials: str
    start_time: Union[date, datetime]
    end_time: Union[date, datetime]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.start_time, date):
            self.start_time = datetime.combine(self.start_time, datetime.min.time())

        if isinstance(self.end_time, date):
            self.end_time = datetime.combine(self.end_time, datetime.min.time())

    def get_mongo_db_uri(self):
        return self.mongo_uri.format(
            mongo_db=self.mongo_db,
            mongo_credentials=self.mongo_credentials,
        )
