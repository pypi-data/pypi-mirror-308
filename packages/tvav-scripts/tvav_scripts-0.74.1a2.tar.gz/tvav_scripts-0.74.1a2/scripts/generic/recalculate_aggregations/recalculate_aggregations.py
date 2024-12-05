import base64
import os
import pandas as pd
import urllib.parse
from datetime import datetime
import pymongo
from bson import ObjectId
from product.util import get_logger
from dotenv import load_dotenv

load_dotenv()


class AggregationCalculator:
    """
    AggregationCalculator is a class that defines methods for recalculating and updating aggregation data for a given set
    of AvWorks.
    """

    def __init__(self):
        self.logger = get_logger(name="recalculate_aggregations")
        self.host = os.getenv("MONGO_DB_HOST")
        self.client = pymongo.MongoClient(host=self.host)
        self.db = self.client.get_database()
        self.approval_ratio = int(os.getenv("APPROVAL_RATIO", "95"))
        self.client_reportal = os.getenv("CLIENT_REPORTAL")
        self.datetime_format = os.getenv("DATETIME_FORMAT")
        self.start_time = datetime.strptime(os.getenv("START_TIME"), self.datetime_format)
        self.end_time = datetime.strptime(os.getenv("END_TIME"), self.datetime_format)
        self.collection = os.getenv("COLLECTION")

    def cuesheet_av_work_url(self, id_to_use: ObjectId) -> str:
        """
        Given an ID and reportal client, creates a link to view the cuesheet.
        ----------
        :param self:
        :param The subdomain of the url client reportal
        :param id: av_work ID of the program.

        :return string with cuesheet link:
        ----------
        """
        url_cuesheets = f"https://{self.client_reportal}.bmat.com/cuesheets/view/"
        return urllib.parse.quote(url_cuesheets + base64.b64encode(bytes("AvWork:" + str(id_to_use), "utf-8")).decode("ascii"), safe="/:")

    def recalculate(self):
        """
        Recalculates and updates aggregation data for a given set of AvWorks.
        Step 1 (Candidates). --> create a list of candidates.
        Step 2 (Eligibles). --> Query candidates in the 'av_work' collection along with more restrictions and put in a dataframe.
        Step 3 (UPDATE). --> If number of eligibles > 0 update the documents
        Step 5 (APPROVE documents where idententified_music_ratio >= APPROVAL_RATIO)
        Step 6 (XLSX) --> resume the info in a xlsx.


        :param client_url: The subdomain of the url client reportal.
        :param collection: collection where are the broadcasts (i.e. 'schedule' or 'digital_usage')
        :param start_time:
        :param end_time:

        :return:
        """

        # Candidates
        # get av_work ids candidates
        query_broadcasts = {"start_time": {"$gte": self.start_time, "$lt": self.end_time}}
        distinct_av_works = self.db[self.collection].distinct("av_work", query_broadcasts)

        # Eligible
        # query av_work eligible and put into dataframe
        query_av_work = {
            "_id": {"$in": distinct_av_works},
            "aggregations.total_identified_cues": 0,
            "cuesheet.cues.0": {"$exists": True},
            "cuesheet.cues.music_work": {"$exists": True},
        }
        cursor = self.db["av_work"].find(query_av_work, {"_id": 1, "title": "$titles.original_title"})
        eligibles = [item for item in list(cursor)]

        # check len of eligible
        update_count = len(eligibles)
        # logger info
        self.logger.info("Aggregations will be calculated for '%s' AvWorks.", update_count)

        if update_count > 0:

            # UPDATE
            df = pd.DataFrame(eligibles)

            #  create URL column
            df["URL"] = df.apply(lambda x: self.cuesheet_av_work_url(id_to_use=x["_id"]), axis=1)

            # update
            try:
                query_update = {"_id": {"$in": df["_id"].tolist()}}
                update = {"$set": {"document_info.updated_at": datetime.utcnow()}}
                self.db['av_work'].update_many(query_update, update)

            except Exception as ex:
                self.logger.info(ex)

        else:
            df = pd.DataFrame()

        # APPROVE documents where identified_music_ratio >= APPROVAL_RATIO
        query_ratio = {"aggregations.identified_music_ratio": {"$gte": self.approval_ratio}, "approved": False}
        update_ratio = {"$set": {"approved": True}}
        cursor = self.db["av_work"].find(query_ratio, {"_id": 1, "program_id": "work_ids.program_id"})
        filtered_list = [item for item in list(cursor)]
        if len(filtered_list) > 0:
            df_2 = pd.DataFrame(filtered_list)
            self.db['av_work'].update_many(query_ratio, update_ratio)
            df_2["URL"] = df_2.apply(lambda x: self.cuesheet_av_work_url(id_to_use=x["_id"]), axis=1)
        else:
            df_2 = pd.DataFrame()

        # XLSX
        wb2 = pd.ExcelWriter("Recalculate.xlsx", engine="xlsxwriter")
        df.to_excel(excel_writer=wb2, index=False, sheet_name="degenerated_cases")
        df_2.to_excel(excel_writer=wb2, index=False, sheet_name="approved_cases")
        wb2.save()

        if df.empty:
            update_count = 0

        self.logger.info("Total Approved: %s\nTotal updated: %s\n", len(filtered_list), update_count)


if __name__ == "__main__":
    AggregationCalculator().recalculate()
