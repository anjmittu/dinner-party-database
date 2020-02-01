import pymongo
import os


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
