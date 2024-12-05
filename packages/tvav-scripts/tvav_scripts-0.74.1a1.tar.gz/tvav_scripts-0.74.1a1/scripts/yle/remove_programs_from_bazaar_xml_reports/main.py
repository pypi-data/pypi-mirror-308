import csv
import os
import re
import shutil
from collections import defaultdict
from dateutil.parser import parse
from dotenv import load_dotenv
from lxml import etree, objectify
from pathlib import Path
from tqdm import tqdm
from typing import Iterable, Iterator

from scripts.utils.file_operations import download_bazaar_files, upload_to_bazaar


class Config:
    bazaar_mongo_uri: str
    bazaar_storage_uri: str
    namespace: str
    reports_dir: Path
    input_file_csv: Path

    def __init__(self) -> None:
        self.bazaar_mongo_uri = os.getenv("BAZAAR_MONGO_URI")  # type: ignore
        self.bazaar_storage_uri = os.getenv("BAZAAR_STORAGE_URI")  # type: ignore

        self.namespace = "yle-reports-fortnightly"
        self.reports_dir = Path(__file__).parent / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        self.input_file_csv = Path(__file__).parent / "input.csv"

        if not self.input_file_csv.exists():
            raise ValueError(
                "Please, create an input.csv file with the yle_numerical_ids and report_dates.\n"
                "For more info please read the README.md file."
            )

        if not (
            self.bazaar_storage_uri and
            self.bazaar_mongo_uri
        ):
            raise ValueError("Missing BAZAAR credentials.")


class Program:
    def __init__(self, program: objectify.ObjectifiedElement) -> None:
        self._data = program

    @property
    def yle_numerical_id(self) -> str:
        """Matches Reportal yle_numerical_id."""
        return str(self._data.rapnro)

    @property
    def report_date(self) -> str:
        """Reported date --> YYYY-MM-DD"""
        return str(parse(str(self._data.ajopvm)).date())


class ReportFile:
    def __init__(self, report_file: Path) -> None:
        self._data = report_file
        self._bak_file = self._data.parent / (self._data.name + ".bak")
        self._file_content = objectify.fromstring(self._data.read_bytes())

    def _create_backup(self):
        if self._bak_file.exists():
            return
        
        # create backup just in case we want to revert the operation
        shutil.copy(self._data, self._bak_file)

    @property
    def name(self) -> str:
        return self._data.name

    @property
    def programs(self) -> Iterator[Program]:
        try:
            programs = self._file_content.ohjelma_esitys
        except AttributeError:
            return []

        for program in programs:
            yield Program(program)

    @programs.setter
    def programs(self, programs: list[Program]) -> None:
        """ Updates report file program list with specified programs.

        Previous state is stored as filename.bak.
        """

        self._file_content.ohjelma_esitys = [p._data for p in programs]

        # I have to prepend this because etree doesn't add it by itself
        updated_file_content = b"<?xml version='1.0' encoding='UTF-8'?>\n"
        updated_file_content += etree.tostring(self._file_content, pretty_print=True)

        self._create_backup()

        self._data.write_bytes(updated_file_content)


class ProgramFinder:
    def __init__(self, config: Config) -> None:
        self._config = config

    def download_reports_from_bazaar(self, report_dates: Iterable[str]):
        print("Downloading reports from bazaar, please wait...")

        download_bazaar_files(
            db_uri=self._config.bazaar_mongo_uri,
            storage_uri=self._config.bazaar_storage_uri,
            query={
                "namespace": "yle-reports-fortnightly",
                "name": re.compile("|".join(report_dates)),
            },
            local_dir=str(self._config.reports_dir.absolute()),
        )

        print("REPORT FILES DOWNLOADED FROM BAZAAR")
        print()

    def upload_reports_to_bazaar(self, files: Iterable[Path]):
        """Uploads file to bazaar, replacing an already existing file."""

        for file in tqdm(files, desc="Uploading files to bazaar", unit="files"):
            upload_to_bazaar(
                db_uri=self._config.bazaar_mongo_uri,
                storage_uri=self._config.bazaar_storage_uri,
                query={
                    "namespace": "yle-reports-fortnightly",
                    "name": "/" + file.name,
                },
                local_dir=str(file.parent.absolute())
            )

    @property
    def report_files(self) -> Iterator[ReportFile]:
        for report_file in self._config.reports_dir.iterdir():
            yield ReportFile(report_file)

    @property
    def total_report_files(self) -> int:
        return len([
            f
            for f in self._config.reports_dir.iterdir()
            if ".bak" not in f.name
        ])


def revert_files(files: Iterable[Path]):
    """Restores file contents from previous backup."""

    for file in tqdm(files, desc="Reverting files", unit="files"):
        bak_file = file.parent / (file.name + ".bak")
        shutil.move(bak_file, file)


def run() -> None:
    """The MAIN body for the script.

    1. Init setup
        - Read config from env
    2. Read yle_numerical_ids and ajopvm from input.csv file
    3. Download all reports that match the filter
    4. Find all report files that contain the programs to remove
    5. Update report files with the updated program lists (keep old version as backup)
    6. Ask user if to revert or upload changes to bazaar
    6.1. If user chosed revert --> restore files from bak copies
    6.2. If user chosed upload --> upload files to bazaar
    """

    print("### START ###")

    stats = defaultdict(list)

    load_dotenv()
    config = Config()

    input_lines = config.input_file_csv.read_text().splitlines()
    reader = csv.reader(input_lines)
    header = next(reader)

    assert header == ["yle_numerical_id", "ajopvm"], "Was expecting to find `yle_numerical_id,ajovpm` in the first row"
    rows = []
    unique_dates = set()
    for row in reader:
        assert parse(row[1]).strftime("%Y%m%d") == row[1], "Date format invalid, expected YYYYMMDD"
        row_d = dict(zip(header, row))
        rows.append(row_d)
        unique_dates.add(row[1])

    program_finder = ProgramFinder(config)
    if input("Download reports from BAZAAR? [y/N]: ") == "y":
        program_finder.download_reports_from_bazaar(unique_dates)

    print(f"Reports dir contains a total of {program_finder.total_report_files} reports")
    print()

    print("Searching programs in XML files:")

    updated_files = set()
    pbar = tqdm(rows, unit="programs")
    for row in pbar:
        yle_numerical_id = row["yle_numerical_id"]

        pbar.set_description_str(yle_numerical_id)
        
        pbar_files = tqdm(
            [
                file
                for file in config.reports_dir.glob("*" + row["ajopvm"] + "*")
                if not file.name.endswith(".bak")
            ],
            desc="Searching program in files:",
            unit="files",
            leave=False
        )
        for file in pbar_files:
            if yle_numerical_id not in file.read_text():
                continue

            # match! let's update the file without the program
            report_file = ReportFile(file)

            programs_to_keep = []
            for program in report_file.programs:
                if program.yle_numerical_id != yle_numerical_id:
                    programs_to_keep.append(program)
                    continue

            report_file.programs = programs_to_keep
            updated_files.add(file)

            stats[yle_numerical_id].append(file.name)

    print("These are the files that have been updated per yle_numerical_id:")
    for yle_numerical_id, files in stats.items():
        print(f"--- {yle_numerical_id} ---")
        for file in files:
            print(f"- {file}")
        print()

    res = False
    while res not in ["upload", "revert"]:
        res = input(
            "Should we UPLOAD them to bazaar or REVERT the changes done to local files? (upload/revert)"
        )

    if res == "revert":
        revert_files(updated_files)
    elif res == "upload":
        program_finder.upload_reports_to_bazaar(updated_files)
    else:
        raise RuntimeError("Impossible")

    print("### END ###")


if __name__ == "__main__":
    run()
