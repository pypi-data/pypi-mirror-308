import os
from pathlib import Path


class Config:
    stats_reports_dir: Path
    xml_reports_dir: Path
    third_script_reports_dir: Path
    third_script_dry_run: bool
    third_script_generate_post_reports: bool

    download_bazaar_files: bool
    bazaar_mongo_uri: str
    bazaar_storage_uri: str
    namespace: str

    single_view_uri: str

    prod_mongo_uri: str
    backup_mongo_uri: str

    batch_size: int

    do_report_1: bool
    do_report_2: bool
    do_report_3: bool

    def __init__(self) -> None:
        cwd = os.getcwd()
        self.stats_reports_dir = Path(cwd) / os.getenv("STATS_REPORTS_DIR", "stats_reports")
        self.third_script_reports_dir = Path(cwd) / os.getenv("STATS_REPORTS_DIR", "3_reports")
        self.xml_reports_dir = Path(cwd) / os.getenv("REPORTS_DIR", "reports")

        self.bazaar_mongo_uri = os.getenv("BAZAAR_MONGO_URI")  # type: ignore
        self.bazaar_storage_uri = os.getenv("BAZAAR_STORAGE_URI")  # type: ignore
        self.namespace = os.getenv("NAMESPACE", "yle-reports-fortnightly")

        self.single_view_uri = os.getenv("SINGLE_VIEW_URI", "http://sv-api.data.bmat.com").rstrip("/")

        self.prod_mongo_uri = os.getenv("PROD_MONGO_URI")  # type: ignore
        self.backup_mongo_uri = os.getenv("BACKUP_MONGO_URI")  # type: ignore

        self.batch_size = int(os.getenv("BATCH_SIZE", 10_000))

        def env_as_bool(v: str) -> bool:
            return v.lower() in ["true", "1"]

        self.download_bazaar_files = env_as_bool(os.getenv("DOWNLOAD_BAZAAR_FILES", "0"))
        self.do_report_1 = env_as_bool(os.getenv("DO_REPORT_1", "0"))
        self.do_report_2 = env_as_bool(os.getenv("DO_REPORT_2", "0"))
        self.do_report_3 = env_as_bool(os.getenv("DO_REPORT_3", "0"))

        # default set to True
        self.third_script_dry_run = env_as_bool(os.getenv("THIRD_SCRIPT_DRY_RUN", "1"))
        self.third_script_generate_post_reports = env_as_bool(os.getenv("THIRD_SCRIPT_GENERATE_POST_REPORTS", "1"))

        if (
            not self.bazaar_storage_uri or
            not self.bazaar_mongo_uri
        ):
            raise ValueError("Missing BAZAAR credentials.")

        if (
            not self.prod_mongo_uri or
            not self.backup_mongo_uri
        ):
            raise ValueError("Missing MongoDB credentials.")

        if (
            not self.stats_reports_dir.exists() or
            not self.stats_reports_dir.is_dir()
        ):
            raise ValueError("Missing stats reports dir.")

        if (
            not self.xml_reports_dir.exists() or
            not self.xml_reports_dir.is_dir()
        ):
            raise ValueError("Missing YLE XML reports dir.")

        self.third_script_reports_dir.mkdir(parents=True, exist_ok=True)
