import os

from dotenv import load_dotenv
from mongoengine import connect
from pymongo import UpdateOne
from reportal_model import MusicWork


def main():
    # TODO: Support multiple texts and regex patterns
    # TODO: Parameterise these fields for easier testing
    field_name = os.getenv("FIELD")
    regex_pattern = os.getenv("REGEX_TO_REMOVE")
    cleaned_regex = clean_regex(regex_pattern)
    text_to_remove = os.getenv("TEXT_TO_REMOVE")
    mws = MusicWork.objects.aggregate([
        {"$project": {"ids": {"$objectToArray": f"${field_name}"}, f"{field_name}": 1}},
        {"$match": {"$or": [{"ids.v": {"$regex": regex_pattern, "$options": "i"}}, {"ids.v": text_to_remove}]}},
    ])
    operations = []
    for mw in mws:
        work_ids = {}
        for key, value in mw["work_ids"].items():
            work_ids[key] = value if not isinstance(value, str) or value.lower() not in (text_to_remove, cleaned_regex) else None
        operations.append(UpdateOne({"_id": mw["_id"]}, {"$set": {"work_ids": work_ids}}))
    if operations:
        result = MusicWork._get_collection().bulk_write(operations)
        print(result.bulk_api_result)
    else:
        print("No operations needed")


def clean_regex(regex_pattern: str):
    # TODO: Actually change to text or pattern-match the regex while comparing
    return regex_pattern.replace("^", "").replace("$", "")


if __name__ == "__main__":
    load_dotenv()
    connect(host=os.getenv("MONGO_URI"))
    main()
