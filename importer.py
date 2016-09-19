from pymongo import MongoClient
from User import User


class Importer:

    @staticmethod
    def user_factory(user_cursor):
        """Creates user object from mongo cursor"""
        u = User()
        u.id = user_cursor.get("_id")
        u.download_list = user_cursor.get("downloadList")
        u.realms = user_cursor.get("realms")
        u.school_classes = user_cursor.get("schoolclasses")
        u.subjects = user_cursor.get("subjects")
        u.city = user_cursor.get("city")
        u.country = user_cursor.get("country")
        u.area_code = user_cursor.get("areaCode")
        u.gender = user_cursor.get("gender")
        u.schools = user_cursor.get("schools")

        return u

    def get_premium_users(self):
        """Fetchs a list of premium users from mongodb """
        client = MongoClient('localhost', 27017)
        db = client.mU.vws_Users
        result = db.find({'type': 2}).limit(1)
        user_list = []

        for r in result:
            user = self.user_factory(r)
            user_list.append(user)

    def filter(self, user_record):
        print(user_record)
        clean_data = []
        props = ['_id', 'downloadList', 'realms', 'schoolclasses', 'subjects', 'city', 'country', 'areaCode', 'gender',
                 'schools']
        u = User()
        u.id = user_record["_id"]
        u.download_list = user_record["downloadList"]
        u.realms = user_record["realms"]
        u.school_classes = user_record["schoolclasses"]

        print('--------------------------------------------')
        print(u)

    def ImportData(self):
        self.get_premium_users()

imp = Importer()

imp.ImportData()
