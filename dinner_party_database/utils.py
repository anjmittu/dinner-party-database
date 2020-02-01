import pymongo
import os
from typing import List
from datetime import datetime


class Utils:
    client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
    db = client["diner-party"]

    @staticmethod
    def update_question(phone, n):
        col = db["people"]
        col.update_one(
            {"number": phone},
            {"$set": {"last_question": n}}
        )

    @staticmethod
    def get_last_question(phone):
        return __get_person(phone, {"last_question": 1})["last_question"]

    @staticmethod
    def get_person(phone, fields = {}):
        col = db["people"]
        return col.find_one(
            {"number": phone},
            fields
        )

    @staticmethod
    def get_party(phone):
        col = db["parties"]
        return col.find_one(
            {"_id": __get_person(phone, {"party": 1})}
        )

    @staticmethod
    def get_all_party():
        parties = db["parties"]
        return parties.find({})

    @staticmethod
    def get_event(phone):
        col = db["events"]
        party = get_party(phone)
        res = col.find_one(
            {"_id": party["event"] if party["event"] != None else make_event(party)}
        )

    @staticmethod
    def update_event(id, changes):
        col = db["events"]
        col.update_one(
            {"_id": id},
            changes
        )

    @staticmethod
    def __make_event(party):
        events = db["events"]
        parties = db["parties"]

        result = events.insert_one({})
        parties.update_one(
            {"_id": party["_id"]},
            {"$set": {"event": result.inserted_id}}    
        )

        return result.inserted_id

    @staticmethod
    def get_cooker(people_ids: List):
        people_table = dp["people"]
        latest_cooked = None
        latest_person = None
        for person in people_ids:
            person_info = people_table.find_one({"_id": person})
            if latest_cooked is None or latest_cooked > person_info["last_cooked"]:
                # The person is current the last person to have cooked
                # We still need to check if they are able to cook today
                if Utils.__get_current_day() in person_info["cook_days"]:
                    latest_person = person_info
                    latest_cooked = person_info["last_cooked"]
        return latest_person

    @staticmethod
    def __get_current_day():
        return datetime.today().weekday()
