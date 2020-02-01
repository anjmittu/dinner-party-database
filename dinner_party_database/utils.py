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