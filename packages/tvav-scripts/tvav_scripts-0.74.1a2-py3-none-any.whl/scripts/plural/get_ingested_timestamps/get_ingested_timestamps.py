import csv
import logging
import os

from dotenv import load_dotenv
from pymongo import MongoClient

HEADERS = (
    "Start_Time_UTC",
    "End_Time_UTC",
    "Input_Name",
)

logging.getLogger()


class TimestampGetterScript:
    def __init__(self, input_filename: str, output_filename: str, id_column: str, name_column: str, mongo_uri: str):
        self.db = MongoClient(host=mongo_uri).get_default_database()
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.id_column = id_column
        self.name_column = name_column

    def run(self):
        with open(self.input_filename, "r") as in_file, open(self.output_filename, "w") as out_file:
            reader = csv.DictReader(in_file, delimiter=";")
            writer = csv.DictWriter(out_file, HEADERS, delimiter=";")
            writer.writeheader()
            for row in reader:
                output_row = {"Input_Name": row[self.name_column]}
                multimedia = self.db.multimedia.find_one({"file_info": row[self.id_column]})
                if multimedia is not None:
                    output_row["Start_Time_UTC"] = multimedia["start"].strftime("%Y-%m-%d %H:%M:%S")
                    output_row["End_Time_UTC"] = multimedia["end"].strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow(output_row)


if __name__ == "__main__":
    load_dotenv()
    TimestampGetterScript(
        os.getenv("INPUT_FILENAME"),
        os.getenv("OUTPUT_FILENAME"),
        os.getenv("FILE_ID_COLUMN"),
        os.getenv("NAME_COLUMN"),
        os.getenv("TVAV_MONGO_URI"),
    ).run()
