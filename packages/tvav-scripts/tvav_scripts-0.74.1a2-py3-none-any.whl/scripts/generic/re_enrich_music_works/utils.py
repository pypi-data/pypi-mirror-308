import base64
import csv
import importlib

from reportal_model import (
    Cue as ReportalModelCue,
    AvWork as ReportalModelAvWork,
    Schedule
)
from music_report.model import (
    Cue as MusicReportCue,
    MusicWork as MusicReportMusicWork,
    CueIdentifiers as MusicReportCueIdentifiers,
    Contributor as MusicReportContributor,
)
from music_report.vericast.model import MusicReport as MusicReportVericast
from music_report.cuenator.model import MusicReport as MusicReportCuenator
from typing import Optional, Union


MusicReportCuesheet = Union[MusicReportVericast, MusicReportCuenator]


REPORT_FILENAME_COLS = {
    "single_view_ids_repeated.csv": [
        "single_view_id",
        "n_music_works",
    ],
    "music_works_updated.csv": [
        "music_work_id",
        "music_work_title",
        "music_work_source",
        "isrc",
        "single_view_id",
    ],
    "av_works_affected.csv": [
        "av_work_id",
        "reportal_url",
        "music_work_title",
        "music_work_source",
        "isrc",
        "single_view_id",
    ],
    "cue_level_enrichment.csv": [
        "music_work_id",
        "music_work_title",
        "av_work_id",
        "av_work_title",
        "cue_index",
    ],
}


class CueEnrichmentOptions:
    def __init__(self, extras: dict):
        self.extras = extras


def get_client_custom_values(custom_values_str: str) -> dict:
    """Returns the client reportal_custom_values dict from the custom_values_str path."""
    custom_values_package_str, custom_values_dict_str = custom_values_str.split(":")
    custom_values_package = importlib.import_module(custom_values_package_str)
    return getattr(custom_values_package, custom_values_dict_str)


def get_interceptors_dict(custom_values: dict, customer_name: str) -> dict:
    """Returns the client interceptors dict, using custom_values dict."""
    interceptors_package_str, interceptors_dict_str = custom_values.get("interceptors", ":").split(":")

    if not interceptors_package_str or not interceptors_dict_str:
        raise ValueError(f"Customer {customer_name} has not interceptors defined in custom values")

    interceptors_package = importlib.import_module(interceptors_package_str)
    return getattr(interceptors_package, interceptors_dict_str)


def init_reports(customer_name: str):
    """Prepares CSV reports for current customer."""
    for filename, columns in REPORT_FILENAME_COLS.items():
        with open(f"{customer_name}_" + filename, "wt") as f:
            writer = csv.writer(f)
            writer.writerow(columns)


def get_cuesheet_url(reportal_domain: str, av_work_id: str) -> str:
    """Returns customer Reportal URL for the requested AvWork."""
    return (
        reportal_domain +
        "/cuesheets/view/" +
        base64.b64encode(f"AvWork:{av_work_id}".encode("utf-8")).decode("utf-8").replace("=", "%3D")
    )


def get_music_report_cue_from_repmod_cue(repmod_cue: ReportalModelCue) -> MusicReportCue:
    """Convert reportal_model Cue into music_report Cue."""
    PRODUCTION_TYPES = {
        "production",
        "Production",
    }
    return MusicReportCue(
        start_time=int(repmod_cue.relative_start_time),
        duration=repmod_cue.duration,
        reference_start_time=int(repmod_cue.relative_start_time),
        use=repmod_cue.use,
        extras=repmod_cue.extras,
        identifiers=(
            MusicReportCueIdentifiers(
                single_view_id=repmod_cue.cue_identifiers.single_view_id,
                source=repmod_cue.cue_identifiers.source,
                service_id=repmod_cue.cue_identifiers.service_id,
                phonogram_id=repmod_cue.cue_identifiers.phonogram_id,
                match_id=repmod_cue.cue_identifiers.match_id,
                reference_id=repmod_cue.cue_identifiers.reference_id,
                fingerprint_id=repmod_cue.cue_identifiers.fingerprint_id,
            )
            if repmod_cue.cue_identifiers
            else None
        ),
        confidence=(
            repmod_cue.cue_identifiers.match_confidence
            if repmod_cue.cue_identifiers
            else 0
        ),
        music_work=(
            MusicReportMusicWork(
                title=repmod_cue.music_work.title,
                music_type=repmod_cue.music_work.type,
                contributors=[
                    MusicReportContributor(
                        first_name=cont.first_name,
                        last_name=cont.last_name,
                        role=cont.role,
                        extras=cont.extras,
                        contributor_ids=cont.contributor_ids,
                        affiliation=cont.affiliation,
                        share=cont.share,
                    )
                    for cont in repmod_cue.music_work.contributors
                ],
                work_ids=repmod_cue.music_work.work_ids,
                duration=repmod_cue.music_work.duration,
                source=repmod_cue.music_work.source,
                label=repmod_cue.music_work.work_ids.get("label"),
                is_production_music=(repmod_cue.music_work.type in PRODUCTION_TYPES),
                extras=repmod_cue.music_work.extras,
            )
            if repmod_cue.music_work
            else None
        ),
    )


def get_music_report_cuesheet_from_repmod_av_work(repmod_aw: ReportalModelAvWork, repmod_sch: Optional[Schedule]) -> MusicReportCuesheet:
    cues = []
    if repmod_aw.cuesheet and repmod_aw.cuesheet.cues:
        cues = [
            get_music_report_cue_from_repmod_cue(cue)
            for cue in repmod_aw.cuesheet.cues
        ]

    # extra parameters added to client's custom match importers options
    extras = repmod_aw.extras or {}

    extras["schedule_ids"] = repmod_sch.schedule_ids if repmod_sch else None

    extras["duration"] = repmod_aw.duration
    extras["av_work_duration"] = repmod_aw.duration

    extras["category"] = getattr(repmod_aw, "category", None)
    extras["av_work_category"] = getattr(repmod_aw, "category", None)

    extras["original_title"] = repmod_aw.titles.get("original_title")
    extras["av_work_title"] = repmod_aw.titles.get("original_title")

    extras["eurosport_tag"] = repmod_aw.work_ids.get("eurosport_tag")
    ###

    if repmod_sch:
        return MusicReportVericast(
            start_time=repmod_sch.start_time,
            end_time=repmod_sch.end_time,
            cues=cues,
            extras=extras,
        )

    return MusicReportCuenator(
        av_media=repmod_aw.av_media if repmod_aw.av_media else "",
        cues=cues,
        media_duration=repmod_aw.duration,
        extras=extras,
        error=False,
    )
