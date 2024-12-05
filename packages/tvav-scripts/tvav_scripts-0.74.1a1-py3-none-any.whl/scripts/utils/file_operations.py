import csv
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Callable, Optional


def count_lines(file: Path) -> int:
    """
    Returns the total of lines in a file.
    file must be a Path object.
    """
    with file.open() as f:
        total_lines = sum([1 for _ in f.readlines()])
    return total_lines


class CSVDictUpdater:
    """
    Object to aid on CSV update operations, so you can just focus on updating the rows.

    **Warning** All rows you do not pass to the update_row method won't be in the updated CSV.

    If used as context manager, will maintain both versions of the CSV file on error.

    Example:
    ```python3
    updater = CSVDictUpdater(file_name="example.csv").open()

    for row in updater:
        row["col_1"] = "new value for col_1"
        updater.update_row(row)

    updater.close()
    ```

    You can also use it as a context manager to not handle the open and close operations.
    ```python3
    with CSVDictUpdater(file_name="example.csv") as updater:
        for row in updater:
            row["col_1"] = "new value for col_1"
            updater.update_row(row)
    ```
    """
    def __init__(self, file_name: str, overwrite_file: bool = False):
        self._file_name = file_name
        self._temp_file_name = file_name.replace(".csv", "") + f"_{str(time.time()).split('.')[0]}.csv.tmp"
        self._overwrite_file = overwrite_file

        self._read_file = None
        self._write_file = None

        self.reader: csv.DictReader = None
        self.writer: csv.DictWriter = None

        self._reader_total_rows = None

    def __enter__(self) -> 'CSVDictUpdater':
        return self.open()

    def __iter__(self):
        return self.reader

    def __next__(self):
        yield from self.reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(error=exc_type is not None)

    def open(self) -> 'CSVDictUpdater':
        """
        Opens files, creates the csv.DictReader and csv.DictWriter instances + writes header.

        Returns self.
        """
        with open(self._file_name, "r") as file:
            self._reader_total_rows = sum(1 for _ in file) - 1  # substract the header line

        self._read_file = open(self._file_name, "rt")
        self._write_file = open(self._temp_file_name, "wt")

        self.reader = csv.DictReader(self._read_file)
        self.writer = csv.DictWriter(self._write_file, fieldnames=self.reader.fieldnames)
        self.writer.writeheader()
        return self

    @property
    def total_rows(self) -> int:
        if not self._reader_total_rows:
            raise ValueError("Row count won't be calculated until the file is opened.")
        return self._reader_total_rows

    def update_row(self, row: dict):
        """Will write the current row to the temporal file."""
        self.writer.writerow(row)

    def close(self, error: bool = False):
        """
        Closes files and replaces old file with new one if no error raised.

        :param error: If True, won't overwrite the original file.
        """
        self._read_file.close()
        self._write_file.close()

        # We do not want to accidentally overwrite the file on error
        if error is False:
            if self._overwrite_file:
                final_name = self._file_name
            else:
                final_name = self._temp_file_name.replace(".tmp", "")
            shutil.move(self._temp_file_name, final_name)


def download_bazaar_files(
    db_uri: str,
    storage_uri: str,
    query: Optional[dict] = None,
    local_dir: str = "."
):
    """Download files from bazaar that match the query.
    Default output_dir is ".", replace with the existing folder name.

    Requires bazaar to be installed.
    """

    from bazaar import FileSystem

    fs = FileSystem(db_uri=db_uri, storage_uri=storage_uri)

    if query is None:
        query = {}

    files = fs.db.find(query)
    for file in files:
        with fs.open(
            file["name"], "r", namespace=file["namespace"]
        ) as in_file, open(
            local_dir + "/" + file["name"].split("/")[-1], "w"
        ) as out_file:
            out_file.write(in_file.read())


def upload_to_bazaar(
    db_uri: str,
    storage_uri: str,
    query: dict = None,
    local_dir: str = "."
):
    from bazaar import FileSystem

    fs = FileSystem(db_uri=db_uri, storage_uri=storage_uri)

    if query is None:
        query = {}

    file = fs.db.find_one(query)

    with fs.open(
        file["name"], "w", namespace=file["namespace"]
    ) as out_file, open(
        local_dir + "/" + file["name"].split("/")[-1], "r"
    ) as in_file:
        out_file.write(in_file.read())
