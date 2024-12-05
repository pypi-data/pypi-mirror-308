from bson import ObjectId as _ObjectId
from pydantic.functional_validators import AfterValidator
from pydantic_settings import BaseSettings
from typing_extensions import Annotated


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


class BulkImportSameCuesheetConfig(BaseSettings):
    mongo_credentials: str
    mongo_db: str = "tv-av-prod"
    celery_credentials: str
    flag: str = "BULK_IMPORT_SAME_CUESHEET"
    file_id_to_use: ObjectId
    input_file_with_schedule_ids_as_str: str = "input.csv"

    def get_mongodb_connection_string(self) -> str:
        return (
            "mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority".format(
                self.mongo_credentials,
                self.mongo_db
            )
        )

    def get_celery_uri(self) -> str:
        return (
            "amqp://{}@fast-rabbit.rmq.cloudamqp.com/file-processor?ssl=true".format(self.celery_credentials)
        )
