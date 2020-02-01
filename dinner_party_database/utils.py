import pymongo
import os


class Utils:
    @staticmethod
    def update_question(phone, n):
        client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
        db = client["diner-party"]
        col = db["people"]
        col.update_one(
            {"number": phone},
            {"$set": {"last_question": n}}
        )

    @staticmethod
    def get_last_question(phone):
        client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
        db = client["diner-party"]
        col = db["people"]
        result = col.find_one(
            {"number": phone},
            {"last_question": 1}
        )
        return result["last_question"]