from datetime import datetime
from typing import Any, Literal, Optional, Union
from pydantic.main import IncEx
from pydantic_settings import BaseSettings

from scripts.utils.common_config_models import MongoDBSettings


class UpdateAllIndexInfoConfig(BaseSettings):
    class Config:
        env_nested_delimiter = '__'
    mongo: MongoDBSettings = MongoDBSettings()
    timestamp: datetime

    def model_dump(
        self,
        *,
        mode: Union[Literal['json', 'python'], str]  = 'python',
        include: IncEx = None,
        exclude: IncEx = None,
        context: Optional[dict[str, Any]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: Union[bool, Literal['none', 'warn', 'error']] = True,
        serialize_as_any: bool = False
    ) -> dict[str, Any]:
        dump = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any
        )
        dump["mongo"] = self.mongo.get_mongo_db_uri()

        return dump
