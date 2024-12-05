import base64
import csv
import os
from datetime import datetime

from dotenv import load_dotenv
from mongoengine import connect
from reportal_model import AvWork, Schedule
from tqdm import tqdm


HEADERS = (
    "Channel",
    "Program Title",
    "Program ID",
    "Client ID",
    "Program URL",
    "Title",
    "Broadcast time and date",
    "Last edited timestamp",
    "Last approved timestamp",
    "Last reported timestamp"
)
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class ApprovedWithoutTimestampReport:
    def __init__(self, reportal_base_url: str, output_filename: str = "out.csv", client_id_field: str = ""):
        self.cuesheet_url = f"{reportal_base_url}/cuesheets/view/{{}}"
        self.output_filename = output_filename
        self.start_time = start_time
        self.client_id_field = client_id_field

    def generate(self):
        av_works = AvWork.objects(
            approved=True,
            history_info__approved_change=None,
            history_info__creator__updated_at__gte=self.start_time,
        ).order_by("-history_info__last_editor__updated_at")
        count = av_works.count()
        with open(self.output_filename, "w", encoding="utf-8", newline="") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=HEADERS)
            writer.writeheader()
            for av_work in tqdm(av_works, total=count):
                schedule = Schedule.objects(av_work=av_work).first()
                av_ui_id = base64.b64encode(f"AvWork:{av_work.id}".encode()).decode().replace("=", "%3D")
                writer.writerow({
                    "Channel": schedule.channel.display_name if schedule else "-",
                    "Program Title": av_work.titles.get("original_title") or av_work.titles.get("full_name"),
                    "Program ID": str(av_work.id),
                    "Client ID": av_work.work_ids.get(self.client_id_field),
                    "Program URL": self.cuesheet_url.format(av_ui_id),
                    "Broadcast time and date": schedule.start_time.strftime("%d/%m/%Y %H:%M:%S") if schedule else "-",
                    "Last edited timestamp": av_work.history_info.last_editor.updated_at.strftime(
                        "%d/%m/%Y %H:%M:%S") if av_work.history_info.last_editor else "-",
                    "Last approved timestamp": av_work.history_info.approved_change.updated_at.strftime(
                        "%d/%m/%Y %H:%M:%S") if av_work.history_info.approved_change else "-",
                    "Last reported timestamp": av_work.history_info.reported_change.updated_at.strftime(
                        "%d/%m/%Y %H:%M:%S") if av_work.history_info.reported_change else "-",
                })


if __name__ == "__main__":
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    reportal_base_url = os.getenv("REPORTAL_BASE_URL")
    output_filename = os.getenv("OUTPUT_FILENAME", "out.csv")
    start_time = datetime.strptime(os.getenv("START_TIME"), DATETIME_FORMAT)
    client_id_field = os.getenv("CLIENT_ID_FIELD")
    connect(host=mongo_uri)
    ApprovedWithoutTimestampReport(reportal_base_url, output_filename, client_id_field).generate()
