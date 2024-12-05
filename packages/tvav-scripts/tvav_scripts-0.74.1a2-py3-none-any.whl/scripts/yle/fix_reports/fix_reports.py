from dotenv import load_dotenv
from mongoengine import connect

from scripts.utils.slack_notifier import ClassWithSlackLogger
from scripts.yle.fix_reports.utils import FixReportsConfig, PARAMS, OPERATIONS


class FixReports(ClassWithSlackLogger):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.config = FixReportsConfig()
        connect(host=self.config.mongo_uri)

    def run(self, query: dict = None):
        self.logger.info("START")

        if not query:
            query = {}
            ans = input("No query specified, are you sure? (y/N)")
            if ans.lower() != "y":
                return

        self.logger.info("Operation: %s" % self.config.operation)

        params = PARAMS[self.config.operation](self.config, query=query)

        try:
            OPERATIONS[self.config.operation](**params)
        except Exception as e:
            self.logger.error(str(e))
            raise e
        finally:
            self.logger.info("END")


if __name__ == "__main__":
    script = FixReports()

    REPORT_FILENAMES = [
        "report_Yle Klassinen_20220125000000_20231115003047.xml",
        "report_YLERADIO1_20220125000000_20231115003047.xml",
        "report_Yle X3M_20220125000000_20231115003047.xml",
        "report_YLEVEGA_20220125000000_20231115003047.xml",
    ]

    for report_filename in REPORT_FILENAMES:
        QUERY = {
            "namespace": "yle-reports-fortnightly",
            # "name": {"$regex": r"report_.*_20220125000000_20231115.*\.xml"},
            "name": "/" + report_filename,
        }
        script.run(query=QUERY)
