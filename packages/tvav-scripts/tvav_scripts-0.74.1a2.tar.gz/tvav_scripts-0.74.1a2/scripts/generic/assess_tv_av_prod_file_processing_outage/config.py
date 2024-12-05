import os
from datetime import datetime
from dateutil.parser import parse
from pathlib import Path


class Config:
    start_time: datetime
    end_time: datetime
    tv_av_prod_mongo_uri: str
    bazaar_prod_mongo_uri: str

    def __init__(self) -> None:
        self.start_time = parse(os.getenv("START_TIME"))  # type: ignore
        self.end_time = parse(os.getenv("END_TIME"))  # type: ignore
        self.tv_av_prod_mongo_uri = os.getenv("TV_AV_PROD_MONGO_URI")  # type: ignore
        self.bazaar_prod_mongo_uri = os.getenv("BAZAAR_PROD_MONGO_URI")  # type: ignore
        
        assert self.tv_av_prod_mongo_uri is not None
        assert self.bazaar_prod_mongo_uri is not None


report_dir = Path(__file__).parent / "reports"
report_dir.mkdir(parents=True, exist_ok=True)
cued_to_re_process = report_dir / "cued_to_re_process.csv"
cued_to_import = report_dir / "cued_to_import.csv"
reportal_to_process = report_dir / "reportal_to_process.csv"
error = report_dir / "error.csv"
unexpected = report_dir / "unexpected_please_review_manually.csv"
bazaar_prod_files_missing_in_tv_av_prod_report = report_dir / "bazaar_prod_files_missing_in_tv_av_prod.csv"


STATUS_FN_MAPPING: dict[str, Path] = {
    "cuenator_scheduled": cued_to_re_process,
    "matches": cued_to_import,
    "received": reportal_to_process,
    "error": error,
}

BLACKLIST_STATUSES = [
    # CUED
    "imported",
    # Reportal
    "epg_imported",
    "slack_sent",
    "archived",
    "bucket_moved",
    "music_imported",
    "works_imported",
    # Custom
    "vod_generated",
    "generating_report",

]
