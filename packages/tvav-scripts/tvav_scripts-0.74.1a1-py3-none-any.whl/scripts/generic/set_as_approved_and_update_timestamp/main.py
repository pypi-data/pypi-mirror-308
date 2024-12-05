import csv
import logging
from pathlib import Path

from dotenv import load_dotenv
from mongoengine import DoesNotExist, MultipleObjectsReturned, connect
from reportal_model import AvWork
from tqdm import tqdm

from scripts.generic.set_as_approved_and_update_timestamp.config import \
    SetAsApprovedSettings

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("set_as_approved_and_update_timestamps")
    config = SetAsApprovedSettings()

    input_csv = Path(config.input_csv_file)
    report_csv = Path("report.csv")

    with input_csv.open() as f:
        work_ids_list = [
            line.rstrip("\n")
            for line in f.readlines()
            if line.rstrip("\n")
        ]

    with connect(
        host=config.mongodb.get_mongo_db_uri()
    ):
        logger.info("Updating %d AvWorks." % len(work_ids_list))
        av_works_updated = []
        for work_id in tqdm(work_ids_list):
            try:
                av_work: AvWork = AvWork.objects.get(__raw__={
                    f"work_ids.{config.work_id}": work_id
                })
            except DoesNotExist:
                logger.warning("AvWork with '%s=%s' does not exist" % (
                    config.work_id,
                    work_id
                ))
                continue
            except MultipleObjectsReturned as e:
                raise RuntimeError(
                    "Multiple AvWorks found with '%s=%s'. User review is needed!" % (
                        config.work_id,
                        work_id
                    )
                ) from e

            av_work.approved = True
            av_work.status = "approved"
            av_work.history_info.approved_change = av_work.history_info.last_editor
            av_work.save()
            av_works_updated.append(av_work)

        with report_csv.open(mode="wt") as f:
            logger.info("Generating report...")
            writer = csv.writer(f)
            writer.writerow([
                "Program_id",
                "Approved",
                "Status",
                "Last edited by",
                "Last edited at",
                "Last approved by",
                "Last approved at",
                "Last reported by",
                "Last reported at",
                "Approved matches edited?"
            ])

            for av_work in av_works_updated:
                av_work.reload()

                writer.writerow([
                    av_work.work_ids.get(config.work_id),
                    av_work.approved,
                    av_work.status,
                    av_work.history_info.last_editor.who_name if av_work.history_info.last_editor else None,
                    av_work.history_info.last_editor.updated_at if av_work.history_info.last_editor else None,
                    av_work.history_info.approved_change.who_name if av_work.history_info.approved_change else None,
                    av_work.history_info.approved_change.updated_at if av_work.history_info.approved_change else None,
                    av_work.history_info.reported_change.who_name if av_work.history_info.reported_change else None,
                    av_work.history_info.reported_change.updated_at if av_work.history_info.reported_change else None,
                    (
                        av_work.history_info.last_editor.who_name == av_work.history_info.approved_change.who_name and
                        av_work.history_info.last_editor.updated_at == av_work.history_info.approved_change.updated_at
                    ),
                ])



    logger.info("Done!")
