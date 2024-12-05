from datetime import datetime
from typing import (
    Iterable,
    Optional,
    Union,
)

from pydantic import (
    BaseSettings,
    Field,
)

from scripts.reportal_v1.v1_reimport_reindex import utils
from scripts.utils.models import CustomLoadFromEnvModel


from gema.database_model import Channel


class Config(BaseSettings):
    mongo_user: str
    mongo_pwd: str
    db_name: str
    celery_user: str
    celery_pwd: str
    celery_index_queue: Optional[str] = None
    celery_populate_queue: Optional[str] = None
    vericast_customer_name: str
    # disregard recording status
    ignore_recording_status: bool = Field(..., env="IgnoreRecordingsValidations")
    # do not import unidentified music
    ignore_unidentified_music: bool = Field(..., env="IgnoreUnidentified")
    # force import
    force_import: bool = Field(..., env="ForceImport")
    # get music metadata from SV
    overwrite_music_works: bool = Field(..., env="OverwriteMusicWorks")
    # recalculate statistics (index)
    propagation_signals_enabled: bool = Field(..., env="PropagationSignalsEnabled")

    def get_mongodb_connection_string(self) -> str:
        return (
            f"mongodb://{self.mongo_user}:{self.mongo_pwd}@bmat-tvav-prod-shard-00-00-yq6o5.mongodb.net:27017,"
            f"bmat-tvav-prod-shard-00-01-yq6o5.mongodb.net:27017,bmat-tvav-prod-shard-00-02-yq6o5.mongodb.net:27017/"
            f"{self.db_name}?replicaSet=bmat-tvav-prod-shard-0&authSource=admin&ssl=true"
        )

    def get_celery_broker_connection_string(self) -> str:
        return f"amqp://{self.celery_user}:{self.celery_pwd}@fast-rabbit.rmq.cloudamqp.com/file-processor?ssl=true"


class BroadcastsParameters(CustomLoadFromEnvModel):
    start_time: datetime = Field(..., env="broadcast_start_time", alias="start_time__gte")
    end_time: datetime = Field(..., env="broadcast_end_time", alias="start_time__lt")
    channels: Iterable['Channel'] = Field(None, alias="_channel__in")
    category: Optional[str] = Field(None, env="broadcast_category", alias="_category")
    production_in: Optional[Iterable[Union[int, str]]] = Field(
        None, env="broadcast_production_in", alias="production__in", parse_obj=utils.string_to_list
    )
    populated: Optional[bool] = Field(None, env="broadcast_populated", alias="_populated")
    error_description_in: Optional[Iterable[str]] = Field(
        None,
        env="broadcast_error_description_in",
        alias="_error_description__in",
        parse_obj=utils.string_to_list
    )
    id_in: Optional[Iterable[Union[str, int]]] = Field(
        None, env="broadcast_id_in", alias="id__in", parse_obj=utils.string_to_list
    )


class ChannelsParameters(CustomLoadFromEnvModel):
    keyname: Optional[str] = Field(None, env="channel_keyname")
