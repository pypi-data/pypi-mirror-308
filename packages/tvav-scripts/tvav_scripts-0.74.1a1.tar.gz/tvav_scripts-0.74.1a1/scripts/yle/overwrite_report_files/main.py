import os
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

from scripts.utils.file_operations import upload_to_bazaar


class Config:
    bazaar_mongo_uri: str
    bazaar_storage_uri: str
    reports_dir_to_use: str
    namespace: str
    reports_dir: Path

    def __init__(self) -> None:
        self.bazaar_mongo_uri = os.getenv("BAZAAR_MONGO_URI")  # type: ignore
        self.bazaar_storage_uri = os.getenv("BAZAAR_STORAGE_URI")  # type: ignore
        self.reports_dir_to_use = os.getenv("REPORTS_DIR_TO_USE")  # type: ignore

        self.namespace = "yle-reports-fortnightly"
        self.reports_dir = Path(__file__).parent / self.reports_dir_to_use

        if not (
            self.bazaar_storage_uri and
            self.bazaar_mongo_uri
        ):
            raise ValueError("Missing BAZAAR credentials.")

        if not (
            self.reports_dir.exists() and
            self.reports_dir.is_dir()
        ):
            raise ValueError("Check your REPORTS_DIR_TO_USE")


def upload_reports_to_bazaar(config: Config):
    """Uploads file to bazaar, replacing an already existing file."""

    files = [_ for _ in config.reports_dir.iterdir()]
    for file in tqdm(
        files,
        desc="Uploading files to bazaar",
        unit="files"
    ):
        upload_to_bazaar(
            db_uri=config.bazaar_mongo_uri,
            storage_uri=config.bazaar_storage_uri,
            query={
                "namespace": "yle-reports-fortnightly",
                "name": "/" + file.name,
            },
            local_dir=str(config.reports_dir.absolute())
        )


def run() -> None:
    """The MAIN body for the script.

    1. Init setup
        - Read config from env
    """

    print("### START ###")

    load_dotenv()
    config = Config()
    upload_reports_to_bazaar(config)

    print("### END ###")


if __name__ == "__main__":
    run()
