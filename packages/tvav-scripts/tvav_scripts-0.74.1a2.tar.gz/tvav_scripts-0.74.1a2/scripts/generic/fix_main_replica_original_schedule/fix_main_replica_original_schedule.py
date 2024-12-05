from dotenv import load_dotenv
from pymongo import MongoClient
from typing import List

from scripts.generic.fix_main_replica_original_schedule.config import MediasetFixMainReplicaAndOriginalScheduleConfig
from scripts.utils.slack_notifier import ClassWithSlackLogger


class MediasetFixMainReplicaAndOriginalSchedule(ClassWithSlackLogger):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.config = MediasetFixMainReplicaAndOriginalScheduleConfig()

        c = MongoClient(host=self.config.get_mongo_db_uri())
        self.db = c.get_default_database()

        self.PIPELINE = [
            {"$match": {"start_time": {"$gt": self.config.start_time, "$lt": self.config.end_time}}},
            {"$group": {"_id": "$av_work", "total": {"$sum": 1}}},
            {"$lookup": {"from": "av_work", "localField": "_id", "foreignField": "_id", "as": "av_work"}},
            {"$unwind": "$av_work"},
            {"$lookup": {"from": "schedule", "localField": "_id", "foreignField": "av_work", "as": "schedules"}},
            {"$project": {"av_work._id": 1, "av_work.original_schedule": 1, "schedules._id": 1, "schedules.start_time": 1, "schedules.main_replica": 1}},
        ]

    def set_oldest_schedule_to_exclusive_main_replica(self, oldest_schedule: dict, schedules_with_main_replica: List[dict]):
        """Makes sure only 1 schedule is marked as main_replica"""
        many_schedules_set_as_main_replica = len(schedules_with_main_replica) > 1
        wrong_schedule_marked_as_main_replica = (
            len(schedules_with_main_replica) == 1
            and oldest_schedule != schedules_with_main_replica[0]
        )

        if many_schedules_set_as_main_replica:
            schedule_ids_not_main_replica = [
                schedule["_id"]
                for schedule in schedules_with_main_replica
                if schedule["_id"] != oldest_schedule["_id"]
            ]
            self.db.schedule.update_many({"_id": {"$in": schedule_ids_not_main_replica}}, {"$set": {"main_replica": False}})
        elif wrong_schedule_marked_as_main_replica:
            self.db.schedule.update_one({"_id": schedules_with_main_replica[0]["_id"]}, {"$set": {"main_replica": False}})

        if not oldest_schedule.get("main_replica", False):
            self.db.schedule.update_one({"_id": oldest_schedule["_id"]}, {"$set": {"main_replica": True}})

    def set_av_work_original_schedule_to_the_oldest_schedule(self, av_work: dict, oldest_schedule: dict):
        """Sets the AvWork original_schedule to the oldest if it is incorrect."""
        if av_work.get("original_schedule") == oldest_schedule["_id"]:
            return
        self.db.av_work.update_one({"_id": av_work["_id"]}, {"$set": {"original_schedule": oldest_schedule["_id"]}})

    def run(self):
        """Fixes the main_replica and original_schedule issue for any linear client.
        Checks the following and commits the changes to the DB.

        - Oldest Schedule must be set to main_replica.
        - AvWork.original_schedule must point to the oldest Schedule
        """
        self.logger.info("Starting now")
        aggregate_result = self.db.schedule.aggregate(self.PIPELINE)
        for av_work_schedules in self.tqdm(aggregate_result):
            av_work = av_work_schedules["av_work"]
            schedules = av_work_schedules["schedules"]

            oldest_schedule = sorted(schedules, key=lambda x: x["start_time"])[0]
            schedules_with_main_replica = [
                schedule
                for schedule in schedules
                if schedule["main_replica"]
            ]

            self.set_oldest_schedule_to_exclusive_main_replica(oldest_schedule, schedules_with_main_replica)
            self.set_av_work_original_schedule_to_the_oldest_schedule(av_work, oldest_schedule)


if __name__ == "__main__":
    script = MediasetFixMainReplicaAndOriginalSchedule()
    script.run()
