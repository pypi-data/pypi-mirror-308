import logging
from pathlib import Path

from dotenv import load_dotenv

from scripts.yle.qa_post_reporting.file_utils import download_yle_report_files
from scripts.yle.qa_post_reporting.model import QAPostReportingConfig
from scripts.yle.qa_post_reporting.statics import prioritized_tags
from scripts.yle.qa_post_reporting.utils import (
    convert_all_xml_to_csv,
    filter_for_media_type,
    find_duplicates_between_two_csvs,
    find_duplicates_combining_two_csvs,
    find_duplicates_within_one_csv,
    run_shell_command,
    generate_report_stats,
)

logging.basicConfig(level="INFO")


class QAPostReportingScript:
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.logger = logging.getLogger("YLE-QA-POST-REPORT")
        self.config = QAPostReportingConfig()  # type: ignore

        parent_dir = Path(__file__).parent

        (parent_dir / self.config.reports_folder).mkdir(parents=True, exist_ok=True)
        (parent_dir / self.config.main_csv_path).touch(exist_ok=True)

        self.csv_path = f"{self.config.reports_folder}/current_batch.csv"
        self.tv_csv_path = f"{self.config.reports_folder}/current_batch_tv.csv"
        self.radio_csv_path = f"{self.config.reports_folder}/current_batch_radio.csv"

    def run(self):
        # First we need to download the files from Bazaar
        self.logger.info(f"==== Downloading Report Generated >= {self.config.min_report_date} and <= {self.config.max_report_date} ====")

        download_yle_report_files(
            min_report_date=self.config.min_report_date,
            max_report_date=self.config.max_report_date,
            system_path=self.config.reports_folder,
            bazaar_storage_uri=self.config.bazaar_storage_uri,
            bazaar_db_uri=self.config.bazaar_db_uri,
            tvav_mongo_uri=self.config.tvav_mongo_uri,
        )
        self.logger.info(f"==== Reports downloaded to {self.config.reports_folder}/ ====\n")

        # Next extract the `current_batch.csv`
        self.logger.info("==== Generating CSV of Current Batch ====")

        status = convert_all_xml_to_csv(self.config.reports_folder, self.csv_path, prioritized_tags=prioritized_tags)
        if not status:
            self.logger.warning(f"CSV {self.csv_path} already exists!!!\n")
        else:
            self.logger.info("==== CSV of Current Batch Generated ====\n")

        # Create another CSV filtered only for Radio Channels
        filter_for_media_type(input_csv_path=self.csv_path, output_csv_path=self.tv_csv_path, media_type_startswith="t")
        filter_for_media_type(input_csv_path=self.csv_path, output_csv_path=self.radio_csv_path, media_type_startswith="r")

        # Now start the checks

        self.logger.info("==== CHECKING RULE 1")
        # RULE 1 - Check for duplicate programs in this batch
        # 	- Filter for programs that have the same broadcast date + time and duration and program ID and title
        # 	- There should be only 1 program for this
        check_1 = find_duplicates_within_one_csv(
            input_csv_path=self.csv_path,
            output_csv_path=f"{self.config.reports_folder}/check_1.csv",
            duplicate_columns=["julk_pvm_a", "aklo", "kanava", "plasma_ohjelma_id", "car_ohjelma_id", "nimi"],
        )
        if not check_1:
            self.logger.error("==== DUPLICATES FOUND RULE 1 VALIDATION FAILED !!!!\n")
        else:
            self.logger.info("==== RULE 1 VALIDATED OK ====\n")

        self.logger.info("==== CHECKING RULE 2")
        # RULE 2 - Check for duplicate programs in all history
        # 	- Filter for programs that have the same broadcast date + time and duration and program ID and title
        # 	- There should be only 1 program for this
        check_2 = find_duplicates_between_two_csvs(
            main_csv_path=self.config.main_csv_path,
            input_csv_path=self.csv_path,
            output_csv_path=f"{self.config.reports_folder}/check_2.csv",
            duplicate_columns=["rapnro", "julk_pvm_a", "aklo", "plasma_ohjelma_id", "car_id", "car_ohjelma_id"],
        )
        if not check_2:
            self.logger.error("==== DUPLICATES FOUND RULE 2 VALIDATION FAILED !!!!\n")
        else:
            self.logger.info("==== RULE 2 VALIDATED OK ====\n")

        self.logger.info("==== CHECKING RULE 3")
        # RULE 3 - Check for changes in rapnro (report number) in all history
        # 	- Filter for programs that have the same program ID and title
        # 	- There should be only 1 rapnro for this
        check_3 = find_duplicates_between_two_csvs(
            main_csv_path=self.config.main_csv_path,
            input_csv_path=self.csv_path,
            output_csv_path=f"{self.config.reports_folder}/check_3.csv",
            duplicate_columns=["julk_pvm_a", "aklo", "kanava", "plasma_ohjelma_id", "car_id", "car_ohjelma_id", "nimi"],
        )
        if not check_3:
            self.logger.error("==== DUPLICATES FOUND RULE 3 VALIDATION FAILED !!!!\n")
        else:
            self.logger.info("==== RULE 3 VALIDATED OK ====\n")

        self.logger.info("==== CHECKING RULE 4")
        # RULE 4 - Check for TV Reruns
        # 	- Filter for TV programs that have the same duration and program ID and title
        # 	- There should be only 1 program for this
        check_4 = find_duplicates_combining_two_csvs(
            main_csv_path=self.config.main_csv_path,
            input_csv_path=self.tv_csv_path,
            output_csv_path=f"{self.config.reports_folder}/check_4.csv",
            duplicate_columns=["rapnro", "nimi", "plasma_ohjelma_id"],
            report_date=self.config.min_report_date,
        )
        if not check_4:
            self.logger.error("==== DUPLICATES FOUND RULE 4 VALIDATION FAILED !!!!\n")
        else:
            self.logger.info("==== RULE 4 VALIDATED OK ====\n")

        self.logger.info("==== CHECKING RULE 5")
        # RULE 5 - Check for Radio Duplicates
        # 	- Filter for Radio programs that have the same duration and program ID and title
        # 	- There should be only 1 program for this
        check_5 = find_duplicates_within_one_csv(
            input_csv_path=self.radio_csv_path,
            output_csv_path=f"{self.config.reports_folder}/check_5.csv",
            duplicate_columns=["rapnro", "julk_pvm_a", "aklo", "nimi", "car_ohjelma_id"],
        )
        if not check_5:
            self.logger.error("==== DUPLICATES FOUND RULE 5 VALIDATION FAILED !!!!\n")
        else:
            self.logger.info("==== RULE 5 VALIDATED OK ====\n")

        self.logger.info("==== CHECKING RULE 6")
        # RULE 6 - Check for Radio Duplicates
        # 	- Filter for Radio programs that have the same duration and program ID and title
        # 	- There should be only 1 program for this
        check_6 = True
        check_6_out, stderr = run_shell_command(
            r"grep -r '\(r01,\|r02,\|r03,\|r04,\|r44,\|r48,\)'" + f" {self.config.reports_folder}/*.xml",
        )
        if check_6_out:
            run_shell_command(f"echo {check_6_out} > {self.config.reports_folder}/check_6.txt")
            check_6 = False
            self.logger.error("==== DUPLICATES FOUND RULE 6 VALIDATION FAILED !!!!\n")
        else:
            self.logger.info("==== RULE 6 VALIDATED OK ====\n")

        # Now generate the stats
        if self.config.generate_stats or (
            check_1 and
            check_2 and 
            check_3 and
            check_4 and
            check_5 and
            check_6
        ):
            self.logger.info("==== GENERATING REPORT STATS ====")
            """
                Creates a file in the stats_folder_path with the following information
                - Total number of reported cue-sheets
                - Unique number of reported cue-sheets
                - Total number of reported cue-sheets for SoMe ONLY if possible
                - Unique number of reported cue-sheets for SoMe ONLY
                - Total number of reported music tracks
                - Total number of reported unique music works
                - Unique number of tracks with a missing performer (esittajat)
                - Unique number of tracks with a missing composer/author (saveltajat)
                - Total of programs starting with YLEMUSA_XXX
            """
            generate_report_stats(self.config.reports_folder)
            self.logger.info("==== STATS GENERATED OK ====\n")


if __name__ == "__main__":
    script = QAPostReportingScript()
    script.run()
