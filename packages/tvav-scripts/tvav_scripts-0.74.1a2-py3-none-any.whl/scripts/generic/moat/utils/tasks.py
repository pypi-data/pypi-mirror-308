from enum import Enum


class ReportalTasks(str, Enum):
    """Reportal valid celery task names."""

    IMPORT_AV_WORK = "import_av_work"
    IMPORT_SCHEDULE = "import_schedule"
    IMPORT_SCHEDULE_JP = "import_schedule_jp"
    POPULATE_AV_WORK = "populate_av_work"
    POPULATE_SCHEDULE = "populate_schedule"
    POPULATE_BROADCAST = "populate_broadcast"

    @classmethod
    def values(cls):
        return [s.value for s in cls]


REPORTAL_TASK_PARAMS_MAPPINGS = {
    ReportalTasks.IMPORT_SCHEDULE: {
        "force": False,
        "recordings_validations": True,
        "overwrite_music_works": False,
        "include_unidentified": True,
        "use_epg_sync": True,
        "reset": False,
        "epg_sync_scope_minutes": None,
        "ignore_protection": False,
    },
    ReportalTasks.IMPORT_SCHEDULE_JP: {
        "force": False,
        "recordings_validations": True,
        "overwrite_music_works": False,
        "include_unidentified": True,
        "use_epg_sync": True,
        "reset": False,
        "epg_sync_scope_minutes": None,
    },
    ReportalTasks.IMPORT_AV_WORK: {
        "force": False,
        "include_unidentified": True,
        "overwrite_music_works": False,
        "reset": False,
        "ignore_protection": False,
    },
    ReportalTasks.POPULATE_SCHEDULE: {
        "customer_name": None,
        "force_import": False,
        "reimport_protections": True,
        "ignore_recording_status": False,
        "overwrite_music_works": False,
        "ignore_unidentified_music": False,
        "use_epg_sync": True,
    },
    ReportalTasks.POPULATE_AV_WORK: {
        "force_import": False,
        "overwrite_music_works": False,
        "ignore_unidentified_music": False,
    },
    ReportalTasks.POPULATE_BROADCAST: {
        "customer_name": None,
        "force_import": False,
        "overwrite_music_works": False,
        "ignore_recording_status": False,
        "ignore_unidentified_music": False,
        "ignore_production_match": False,
        "propagation_signals_enabled": False,
    },
}
