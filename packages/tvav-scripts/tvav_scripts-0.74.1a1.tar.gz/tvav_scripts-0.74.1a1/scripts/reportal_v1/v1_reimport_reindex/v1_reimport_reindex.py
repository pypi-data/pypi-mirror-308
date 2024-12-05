import itertools
import logging.config

from typing import (
    Dict,
    List,
)

from celery import (
    Celery,
)
from celery.canvas import (
    Signature,
    chain,
)
from dotenv import load_dotenv
from mongoengine import connect

from scripts.reportal_v1.v1_reimport_reindex import (
    models,
    utils,
)


from gema.database_model import (
    Broadcast,
    Channel,
)

load_dotenv()
utils.setup_logging()


class V1ReimportReindexScript:
    def __init__(self, config: models.Config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.celery_app = None
        self.tasks_to_run = []

    def run(self, populate_broadcasts: bool, reset_index: bool):
        self.make_connections()

        broadcasts = self.get_broadcasts()

        if populate_broadcasts and reset_index:
            # Creating a list of tasks where the tasks are alternated:
            #   - Do a reimport matches for one broadcast
            #   - Do a reset index for that same broadcast
            # So none of the workers are going to be busy and SIGKILL a process
            self.tasks_to_run = list(
                itertools.chain(
                    *zip(
                        self.make_reimport_matches_tasks(broadcasts),
                        self.make_reset_index_tasks(broadcasts)
                    )
                )
            )

        elif populate_broadcasts:
            self.tasks_to_run = self.make_reimport_matches_tasks(broadcasts)

        elif reset_index:
            self.tasks_to_run = self.make_reset_index_tasks(broadcasts)

        else:
            self.logger.warning("Finishing script... no tasks to run.")
            return

        self.execute_chained_celery_tasks()
        self.logger.info("Script finished succesfully.")
        self.logger.info("To check if all tasks ran succesfully, see the celery queues and the pods logs.")

    def make_connections(self):
        self.logger.info("Making connection to mongodb and celery...")

        self._connect_to_mongo_db()
        self.celery_app = self._make_celery_app()

        self.logger.info("Done!")

    def get_broadcasts(self) -> List['Broadcast']:
        channels_parameters = models.ChannelsParameters()

        self.logger.info("Fetching channels...")
        channels = Channel.objects(**channels_parameters.dict()).no_cache()
        self.logger.info("Done.")

        models.BroadcastsParameters.update_forward_refs()
        broadcasts_parameters = models.BroadcastsParameters(channels=channels)
        self.logger.info(
            f"Fetching broadcasts from {broadcasts_parameters.start_time.isoformat()} to "
            f"{broadcasts_parameters.end_time.isoformat()}."
        )
        broadcasts = Broadcast.objects(**broadcasts_parameters.dict()).timeout(False)
        self.logger.info("Done.")

        return broadcasts

    def make_reimport_matches_tasks(self, broadcasts: List['Broadcast']) -> List[Signature]:
        assert self.config.celery_populate_queue, "CELERY_POPULATE_QUEUE env var must be set to reset index."

        return self._create_immutable_tasks_signature(
            task_name="populate_broadcast",
            tasks_kwargs=[
                {
                    "customer_name": self.config.vericast_customer_name,
                    "broadcast_id": str(broadcast.id),
                    "overwrite_music_works": self.config.overwrite_music_works,
                    "force_import": self.config.force_import,
                    "propagation_signals_enabled": self.config.propagation_signals_enabled,
                    "ignore_recording_status": self.config.ignore_recording_status,
                    "ignore_unidentified_music": self.config.ignore_unidentified_music,
                    "ignore_production_match": True
                } for broadcast in broadcasts
            ],
            queue=self.config.celery_populate_queue
        )

    def make_reset_index_tasks(self, broadcasts: List['Broadcast']) -> List[Signature]:
        assert self.config.celery_index_queue is not None, "CELERY_INDEX_QUEUE env var must be set to reset index."

        return self._create_immutable_tasks_signature(
            task_name="index_program",
            tasks_kwargs=[
                {"broadcast_id": str(broadcast.id), "reload_index_data": True}
                for broadcast in broadcasts
            ],
            queue=self.config.celery_index_queue
        )

    def execute_chained_celery_tasks(self):
        self.logger.info("Sending tasks to celery...")
        chain(*self.tasks_to_run).apply_async()
        self.logger.info("Done.")

    def _connect_to_mongo_db(self):
        connect(host=self.config.get_mongodb_connection_string())

    def _make_celery_app(self) -> Celery:
        return Celery(broker=self.config.get_celery_broker_connection_string())

    def _create_immutable_tasks_signature(
        self, *, task_name: str, tasks_kwargs: List[Dict], queue: str
    ) -> List[Signature]:
        return [
            self.celery_app.signature(
                task_name,
                **{
                    "kwargs": task_kwargs,
                    "immutable": True,
                    "queue": queue
                }
            ) for task_kwargs in tasks_kwargs
        ]


if __name__ == "__main__":
    config = models.Config()
    script = V1ReimportReindexScript(config)
    script.run(populate_broadcasts=True, reset_index=True)
