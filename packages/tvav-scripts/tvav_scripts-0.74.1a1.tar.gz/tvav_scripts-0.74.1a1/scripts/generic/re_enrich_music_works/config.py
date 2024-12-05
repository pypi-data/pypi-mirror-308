from pydantic import Field, BaseSettings
from typing import Optional

from scripts.utils.common_config_models import MongoDBSettings


class EnricherSettings(BaseSettings):
    class Config:
        env_nested_delimiter = '__'

    reportal_domain: str
    custom_values_str: str = Field(env="CUSTOM_VALUES")
    mongodb: MongoDBSettings = MongoDBSettings()
    music_works_file: str = Field("input.csv", env="FILE_TO_USE")
    is_music_works_ids: bool
    csv_with_header: bool
    single_view_ids_still_valid: bool

    single_view_url: str = Field("http://api.single-view.bmat.srv", env="SV_URL")
    dry_run: bool = False
    update_source: bool = False
    replace_work_ids: bool = False
    do_cue_level_enrichment: bool = False

    commissioned_music_crawler: Optional[str] = None
    custom_id_field: Optional[str] = None
