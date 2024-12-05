import xmltodict
from datetime import datetime
from pydantic import BaseSettings
from reportal_model import AvWork, Cue, Report, User
from typing import Literal

from yle_reportal.reports.formats.gramex_teosto_combined import GramexTeostoCombinedReportGenerator
from scripts.utils.file_operations import upload_to_bazaar, download_bazaar_files


class FixReportsConfig(BaseSettings):
    bazaar_mongo_uri: str
    bazaar_storage_uri: str
    mongo_uri: str
    namespace: str = "yle-reports-fortnightly"
    operation: Literal["DOWNLOAD", "GENERATE_MUSIC_WORK_XML", "UPLOAD"]
    local_report_dir: str = "."
    av_work_id: str
    cue_index: int


def get_music_work_xml(cue: Cue) -> None:
    """Generates the XML version for the MusicWork linked to the cue specified
    :param cue
    :return: The MusicWork XML str
    """
    report = Report(
        report_type="YLE-QA-SUBSTITUTION",
        reported_by=User.objects.get(username="bmat_processor"),
        report_status="submitted"
    ).save()
    report_generator = GramexTeostoCombinedReportGenerator(report=report)
    program_cue = report_generator.prepare_cue(cue=cue, schedule_start_time=datetime.now())
    program_music_work = program_cue.works

    as_xml = xmltodict.unparse(program_music_work.to_primitive(), pretty=True)
    print(as_xml)
    print("MusicWork:%s" % str(cue.music_work.id))


def bazaar_params_from_config(config: FixReportsConfig, query: dict, **kwargs) -> dict:
    return {
        "db_uri": config.bazaar_mongo_uri,
        "storage_uri": config.bazaar_storage_uri,
        "query": query,
        "local_dir": config.local_report_dir,
    }


def music_work_xml_params_from_config(config: FixReportsConfig, **kwargs) -> dict:
    return {
        "cue": AvWork.objects.get(id=config.av_work_id).cuesheet.cues[config.cue_index-1]
    }


PARAMS = {
    "DOWNLOAD": bazaar_params_from_config,
    "UPLOAD": bazaar_params_from_config,
    "GENERATE_MUSIC_WORK_XML": music_work_xml_params_from_config
}

OPERATIONS = {
    "DOWNLOAD": download_bazaar_files,
    "UPLOAD": upload_to_bazaar,
    "GENERATE_MUSIC_WORK_XML": get_music_work_xml
}