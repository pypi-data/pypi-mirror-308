import os
from dotenv import load_dotenv
from mongoengine import connect
from mongoengine.queryset import QuerySet

from reportal_model import AvWork

from scripts.utils.slack_notifier import ClassWithSlackLogger


class MonitorAutoApprovedAvWorks(ClassWithSlackLogger):
    def __init__(self):
        load_dotenv()
        super().__init__()
        mongo_creds = os.getenv("MONGO_CREDENTIALS")
        mongo_db = os.getenv("MONGO_DB")
        self.mongo_uri = f"mongodb+srv://{mongo_creds}@bmat-tvav-prod.yq6o5.mongodb.net/{mongo_db}?retryWrites=true&w=majority"

        try:
            connect(host=self.mongo_uri)
        except Exception as exc:
            self.logger.error(str(exc))

    @staticmethod
    def _check_av_works() -> QuerySet:
        return AvWork.objects(
            approved=True,
            history_info__creator__who_name__ne="yle_musa_user",
            history_info__approved_change__who__exists=False,
        )

    def run(self):
        self.logger.info("Querying DB for auto approved AvWorks... :loading:")
        av_works = self._check_av_works()
        if av_works.count() != 0:
            av_work_str = ", ".join([
                f"AvWork:{str(av_work.id)}"
                for av_work in av_works
            ])
            self.logger.error(":x: Detected %d automatically approved AvWorks:\n%s" % (av_works.count(), av_work_str))
        else:
            self.logger.info("None found! :danceblob:")


if __name__ == "__main__":
    monitor = MonitorAutoApprovedAvWorks()
    monitor.run()
