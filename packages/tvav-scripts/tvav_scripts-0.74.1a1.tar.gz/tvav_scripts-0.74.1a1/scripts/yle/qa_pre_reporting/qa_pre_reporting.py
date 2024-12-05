from mongoengine import connect, DoesNotExist
from dotenv import load_dotenv

from reportal_model import Report, User, Channel
from yle_reportal.reports.cmo_biweekly.gramex_teosto_combined import GramexTeostoCombinedReportGenerator
from yle_reportal.reports.common.utils_shared import get_filename
from yle_reportal.reports.common.utils_checks import decide_whether_to_report

from scripts.utils.slack_notifier import ClassWithSlackLogger
from scripts.yle.qa_pre_reporting.model import QAPreReportingScriptConfig, QAReportGenerator


SLACK_MSG = "QA Report ready!\nGo check it https://marisol.bmat.me/launcher/job/Reportal%20-%20Cued/job/YLE/job/QA%20Report/"


class QAPreReportingScript(ClassWithSlackLogger):
    """
    This script generates a statistics report for QA purposes on regular report generation.

    It works by generating the usual report without updating the programs' report history
    in the DB and then using self.session (reportal_reports.ReportSession) to generate
    a report with the following info for each channel:

    - Total reported cuesheets
    - Total reported broadcasts
    - Reported music_works
        - Total
        - Total duration
    - Cuesheets missing interpreter contributor
        - Total
        - Reportal URLs
    - Cuesheets missing performer contributor
        - Total
        - Reportal URLs
    - Errors
        - av_work_id
        - music_work_id
        - error_description
    """
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.qa_report_generator = None
        self.report_generator = None
        self.config = QAPreReportingScriptConfig()

    def init_report_generators(self):
        """
        Initializes Regular report generator to make use of its methods on QA report generator.
        :return:
        """
        self.logger.info("Initializing Report Generators...")

        # Regular Report Generator
        try:
            user = User.objects.get(username=self.config.username)
        except DoesNotExist as e:
            self.logger.error(str(e))
            exit(-1)

        self.report_generator = GramexTeostoCombinedReportGenerator(
            report=Report(
                report_type="YLE-1868-QA",
                reported_by=user.id,
                report_status="submitted",
            ).save()
        )

        # QA Report Generator
        filename = "QA_" + get_filename("ALL_CHANNELS", self.config.start_time, self.config.report_date, "xlsx")
        self.qa_report_generator = QAReportGenerator()
        self.qa_report_generator.create_report(filename=filename)

        self.logger.info("Initializing Report Generators...OK")

    def generate_qa_report(self):
        """
        Populates the QA Report with schedules for each channel.
        :return:
        """
        self.logger.info("Generating QA Report...")

        channels = Channel.objects()
        for channel in self.tqdm(channels, total=channels.count()):
            self.logger.info("Processing schedules for Channel %s" % channel.display_name)

            channel_report = self.qa_report_generator.new_channel_report(channel_name=channel.display_name)

            schedules = self.report_generator.get_schedules(
                channel=channel,
                start_time=self.config.start_time,
                end_time=self.config.report_date,
            )

            program_ids_list = []
            for schedule in self.tqdm(schedules):
                if not decide_whether_to_report(
                    schedule=schedule,
                    report_date=self.config.report_date,
                    program_ids_list=program_ids_list,
                    set_error=False,
                ):
                    continue

                program_ids_list.append(schedule.av_work.work_ids.get("plasma_id"))

                channel_report.add_broadcast(schedule)
            self.qa_report_generator.add_channel_report(channel_report)

        self.logger.info("Generating QA Report...OK")

    def run(self):
        with connect(host=self.config.get_mongodb_connection_string()):
            self.init_report_generators()
            self.generate_qa_report()
            self.logger.info("DONE! :white_check_mark:")


if __name__ == "__main__":
    # TODO update tests and docstrings!
    script = QAPreReportingScript()
    script.run()
