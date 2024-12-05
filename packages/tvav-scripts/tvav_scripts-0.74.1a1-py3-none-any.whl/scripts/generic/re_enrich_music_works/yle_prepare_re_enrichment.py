"""
Use this script before re-enrichment script for YLE.

It re-uses the same configuration as the re-enrichment script so make sure it is ready for YLE.

This script takes as input the summary.csv from the pre QA report and updates
input.csv with a list of SV ids to be used by the re-enrichment script.

Updates MusicWorks in DB with the missing SV id if they are missing in DB.

It will generate 2 files:
- input.csv --> with every single_view_id it could find to be used in re-enrichment
- yle_pre_re_enrichment_error.txt --> with SV API URLs from those it could not find
"""
import base64
import csv
import requests
from dotenv import load_dotenv
from mongoengine import connect

from reportal_model import AvWork

from scripts.generic.re_enrich_music_works.config import EnricherSettings


if __name__ == "__main__":
    load_dotenv()
    config = EnricherSettings()  # type: ignore

    with open(
        "summary.csv", "rt"
    ) as f, open(
        "input.csv", "wt"
    ) as sv_ids_file, open(
        "yle_pre_re_enrichment_error.txt", "wt"
    ) as error_file, connect(
        host=config.mongodb.get_mongo_db_uri()
    ):
        reader = csv.DictReader(f)
        for row in reader:
            needs_re_enrichment = (
                row["Missing in SV too (False = fixed with re-enrichment)"] == "FALSE"
            )
            if not needs_re_enrichment:
                continue

            if sv_id := row["Single View ID"]:
                # we already have the sv id
                print(sv_id, file=sv_ids_file)
                continue

            # we don't know the sv id, need to ask SV API
            source = row["Source"]
            service_id = row["Service id"]
            sv_url = config.single_view_url + (
                f"/sound-recording?source=crawler_{source}&service_id={service_id}"
            )
            try:
                sv_id = requests.get(sv_url).json()["_id"]
                print(sv_id, file=sv_ids_file)
            except KeyError:
                print(sv_url, file=error_file)
                # could not find the SV id in SV API
                continue

            # now we need to update the DB, or the MusicWork won't be updated by the re-enrichment script
            cue_index = int(row["Cue #"]) - 1
            av_work_id = (
                base64.b64decode(
                    row["Reportal URLs"].replace(config.reportal_domain.rstrip("/") + "/cuesheets/view/", "").replace("%3D", "=")
                ).decode().replace("AvWork:", "")
            )
            if not (av_work := AvWork.objects.get(id=av_work_id)):
                raise RuntimeError("Could not find AvWork:%s" % av_work_id)

            music_work = av_work.cuesheet.cues[cue_index].music_work
            music_work.work_ids["single_view_id"] = sv_id
            music_work.save()
