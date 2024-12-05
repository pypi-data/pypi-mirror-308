"""Common config models to be re-used in any script. Requires pydantic to be installed."""
from typing import Optional
from pydantic import BaseModel


class MongoDBSettings(BaseModel):
    creds: Optional[str] = None
    db_name: Optional[str] = None
    uri: str = (
        "mongodb://{creds}@bmat-tvav-prod-shard-00-00-yq6o5.mongodb.net:27017,"
        "bmat-tvav-prod-shard-00-01-yq6o5.mongodb.net:27017,"
        "bmat-tvav-prod-shard-00-02-yq6o5.mongodb.net:27017/{db_name}"
        "?replicaSet=bmat-tvav-prod-shard-0&authSource=admin&ssl=true"
    )

    def get_mongo_db_uri(self) -> str:
        if not self.creds or not self.db_name:
            raise RuntimeError("Missing MONGODB_CREDS")
        return self.uri.format(creds=self.creds, db_name=self.db_name)


class KafkaSettings(BaseModel):
    sasl_plain_username: Optional[str] = None
    sasl_plain_password: Optional[str] = None
    security_protocol: str = "SASL_SSL"
    sasl_mechanism: str = "SCRAM-SHA-256"
    bootstrap_servers: str = "deluxe-mobile-home-01.srvs.cloudkafka.com:9094"
    api_version: tuple[int, int, int] = (0, 10, 1)

    def is_ready(self) -> bool:
        return bool(
            self.sasl_plain_username and
            self.sasl_plain_password
        )


class CelerySettings(BaseModel):
    creds: Optional[str] = None
    uri: str = "amqp://{creds}@fast-rabbit.rmq.cloudamqp.com/file-processor?ssl=true"

    def get_celery_uri(self) -> str:
        if not self.creds:
            raise RuntimeError("Missing CELERY_CREDS")
        return self.uri.format(creds=self.creds)

    def is_ready(self) -> bool:
        return bool(self.creds)
