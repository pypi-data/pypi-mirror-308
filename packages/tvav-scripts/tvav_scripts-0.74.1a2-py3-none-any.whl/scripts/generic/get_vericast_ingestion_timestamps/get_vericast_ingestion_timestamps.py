import csv
import os

from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Tuple


def get_name_and_o_ids_from_csv_text(csv_text: str):
    def parse_id_from_csv_line(line: str):
        line_split = line.split(";")
        return line_split[0], line_split[2]
    return [
        parse_id_from_csv_line(line)
        for line in csv_text.split("\n")[1:]
        if line not in ["", " "]
    ]


def get_db(mongo_creds: str):
    return MongoClient(host=mongo_creds).get_default_database().get_collection("file")


def get_db_fields(o_id: str, file_col) -> Tuple[datetime, datetime]:
    file = file_col.find_one({"_id": ObjectId(o_id)})
    return (
        file["data"]["recording"]["recording_start_time"],
        file["data"]["recording"]["recording_start_time"]
    )


def get_vericast_ingestion_timestamps(filename: str, tv_av_prod_creds: str):
    with open(filename, "rt") as f:
        name_and_o_ids = get_name_and_o_ids_from_csv_text(f.read())
    report_items = []

    tv_av_prod_file = get_db(tv_av_prod_creds)

    for item in name_and_o_ids:
        name, o_id = item
        try:
            start_time, end_time = get_db_fields(o_id, tv_av_prod_file)
        except TypeError:
            print(f"File:{o_id} ERROR")
            report_items.append({
                "Start_Time_UTC": "ERROR",
                "End_Time_UTC": f"{name} File:{o_id} has no data",
                "Input_Name": "ERROR",
            })
        else:
            report_items.append({
                "Start_Time_UTC": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "End_Time_UTC": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Input_Name": name,
            })

    with open("REPORT_" + filename, "wt") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Start_Time_UTC",
                "End_Time_UTC",
                "Input_Name",
            ]
        )
        writer.writeheader()
        writer.writerows(report_items)


if __name__ == "__main__":
    load_dotenv()
    get_vericast_ingestion_timestamps(
        filename=os.getenv("INPUT_CSV"),
        tv_av_prod_creds=os.getenv("MONGO_URI").format(os.getenv("MONGO_USER"))
    )
