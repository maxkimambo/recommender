from pymongo import MongoClient
from User import User
import copy

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
        u.school_type = []
        u.downloads = []

        #create a clean list of school types
        for school in u.schools:
            u.school_type.append(school["type"])

        # create a list of downloaded ids
        for doc in u.download_list:
            u.downloads.append(doc["doc_id"])

        return u

    def get_premium_users(self):
        """Fetchs a list of premium users from mongodb """
        client = MongoClient('localhost', 27017)
        db = client.mU.vws_Users
        result = db.find({'type': 2}).limit(10)
        user_list = []

        for r in result:
            user = self.user_factory(r)
            user_list.append(user)

        return user_list

    def create_user_array(self, user):
        """Creates a list of users and the downloads one record per download """
        user_array = []
        user_copy = copy.copy(user)

        del user_copy.downloads
        del user_copy.download_list

        for d in user.downloads:
            user_copy.doc_id = d
            user_array.append(user_copy)

        return user_array




    def ImportData(self):
      users  =  self.get_premium_users()

      for u in users:
         result = self.create_user_array(u)

imp = Importer()

imp.ImportData()
