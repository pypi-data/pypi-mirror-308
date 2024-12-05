from pathlib import Path
from pydantic import BaseModel, Field
from typing import Union

from scripts.generic.moat.utils.tasks import ReportalTasks


class MoatConfig(BaseModel):
    max_queue_load: int = 500
    trigger_queue_count: int = 100
    backoff_timer: float = 2.0
    mongo_uri: str = "mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority"
    mongo_credentials: str = None
    mongo_db: str = None
    celery_uri: str = "amqp://{}@fast-rabbit.rmq.cloudamqp.com/file-processor"
    celery_credentials: str = None
    celery_queue: str = None
    reportal_url: str = "https://CHANGEME.bmat.com"
    input_file: Union[str, Path] = "input.csv"
    chosen_task: Union[str, ReportalTasks] = None
    task_params: Union[str, dict] = Field(default_factory=dict)
    extras: dict = Field(default_factory=dict)


ENV_MAPPING = {
    "max_queue_load": ("MAX_QUEUE_LOAD", int),
    "trigger_queue_count": ("TRIGGER_QUEUE_COUNT", int),
    "backoff_timer": ("BACKOFF_TIMER", float),
    "mongo_uri": ("MONGO_URI", str),
    "mongo_credentials": ("MONGO_CREDENTIALS", str),
    "mongo_db": ("MONGO_DB", str),
    "celery_uri": ("CELERY_URI", str),
    "celery_credentials": ("CELERY_CREDENTIALS", str),
    "celery_queue": ("CELERY_QUEUE", str),
    "reportal_url": ("REPORTAL_URL", str),
    "input_file": ("INPUT_FILE_WITH_OBJECT_IDS", str),
    "chosen_task": ("CHOSEN_TASK", str),
    "task_params": ("TASK_PARAMS_AS_JSON_DICT", str),
}
