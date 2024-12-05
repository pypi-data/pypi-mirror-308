import csv
import logging
import os

import tqdm
from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import Channel


logger = logging.getLogger(__name__)


def get_values_to_update(filename: str) -> dict[str, str]:
    values_to_update = {}
    with open(filename, "r") as in_file:
        reader = csv.reader(in_file)
        next(reader)
        for row in reader:
            values_to_update[row[0]] = row[1]
    return values_to_update


def add_channel_codes_to_display_names(input_filename: str, output_filename: str):
    values_to_update = get_values_to_update(input_filename)
    with open(output_filename, "w") as out_file:
        writer = csv.writer(out_file)
        writer.writerow((
            "Channel ID",
            "Channel Display Name",
            "New Channel Code",
            "Old Channel Code",
            "Was code changed?"
        ))
        for channel_display_name, channel_code in tqdm.tqdm(values_to_update.items()):
            channel = Channel.objects.get(display_name=channel_display_name)
            channel.update(set__work_ids__channel_codes=channel_code)
            writer.writerow((
                str(channel.id),
                channel_display_name,
                channel_code,
                channel.work_ids["channel_codes"],
                "YES" if channel_code != channel.work_ids["channel_codes"] else "NO"
            ))


if __name__ == '__main__':
    load_dotenv(override=True)
    connect(host=os.getenv("MONGO_URI"))
    add_channel_codes_to_display_names(os.getenv("CHANNEL_CSV_PATH"), os.getenv("OUTPUT_FILENAME"))
