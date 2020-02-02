import pymongo
import os
from typing import List
from datetime import datetime
from google.cloud import pubsub_v1

class Utils:
    client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
    db = client["diner-party"]

    @staticmethod
    def update_question(phone, n):
        col = Utils.db["people"]
        col.update_one(
            {"number": phone},
            {"$set": {"last_question": n}}
        )

    @staticmethod
    def get_last_question(phone):
        return Utils.get_person(phone, {"last_question": 1})["last_question"]

    @staticmethod
    def get_person(phone, fields = {}):
        col = Utils.db["people"]
        return col.find_one(
            {"number": phone},
            fields
        )

    @staticmethod
    def get_person_by_id(id, fields={}):
        col = Utils.db["people"]
        return col.find_one(
            {"_id": id},
            fields
        )

    @staticmethod
    def get_party(phone):
        col = Utils.db["parties"]
        return col.find_one(
            {"_id": Utils.get_person(phone, {"party": 1})["party"]}
        )

    @staticmethod
    def get_all_party():
        parties = Utils.db["parties"]
        return parties.find({})

    @staticmethod
    def get_event(phone):
        col = Utils.db["events"]
        party = Utils.get_party(phone)
        return col.find_one(
            {"_id": party["event"] if party["event"] != None else Utils.__make_event(party)}
        )

    @staticmethod
    def update_event(id, changes):
        col = Utils.db["events"]
        col.update_one(
            {"_id": id},
            changes
        )

    @staticmethod
    def __make_event(party):
        events = Utils.db["events"]
        parties = Utils.db["parties"]

        result = events.insert_one({})
        parties.update_one(
            {"_id": party["_id"]},
            {"$set": {"event": result.inserted_id}}    
        )

        return result.inserted_id

    @staticmethod
    def get_cooker(people_ids: List):
        people_table = Utils.db["people"]
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

    @staticmethod
    def is_there_a_cook(from_number):
        return "who_cooking" in Utils.get_event(from_number)

    @staticmethod
    def add_to_event(number):
        col = Utils.db["events"]
        event = Utils.get_event(number)
        if "who_coming" in event:
            event["who_coming"].append(Utils.get_person(number, {"_id":1})["_id"])
            col.update_one(
                {"_id": event["_id"]},
                {"$set": {"who_coming": event["who_coming"]}}
            )
        else:
            col.update_one(
                {"_id": event["_id"]},
                {"$set": {"who_coming": [Utils.get_person(number, {"_id":1})["_id"]]}}
            )

    @staticmethod
    def trigger_function(data):
        # Set up pub/sub system which will trigger other lambda
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(os.getenv("PROJECT_ID"), os.getenv("TOPIC_NAME"))

        return publisher.publish(topic_path, data=data.encode("utf-8"))

    @staticmethod
    def remove_event(party):
        if party["event"]:
            Utils.db["events"].remove_one({
                "_id": party["event"]
            })

            Utils.db["party"].update_one(
                {"_id": party["_id"]},
                {"$set": {"event": None}}
            )