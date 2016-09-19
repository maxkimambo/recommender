import pymongo

from pymongo import MongoClient


class mongoRepo:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.mU.vws_Users

    # fetch all premium users
    def get_premium_users(self, number_to_skip, page_size):
        result = self.db.find().skip(number_to_skip).limit(page_size)
        print(len(result))
        # return the cursor
        return result

    def get_premium_users(self):
        result = self.dbfind({"type": 2})
        # return the cursor
        return result

    def get_all_active_users(self):
        result = self.db.find({"active": True})
        return result
