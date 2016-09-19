from pymongo import MongoClient
from User import User
import copy
import mysql.connector
from sets import Set

import csv

class Importer:

    @staticmethod
    def user_factory(user_cursor):
        """Creates user object from mongo cursor"""
        u = User()
        u.id = user_cursor.get("_id")
        u.download_list = user_cursor.get("downloadList")
        u.realms = user_cursor.get("realms")
        u.school_classes = user_cursor.get("schoolclasses")
        u.subjects_list = user_cursor.get("subjects")
        u.city = user_cursor.get("city")
        u.country = user_cursor.get("country")
        u.area_code = user_cursor.get("areaCode")
        u.gender = user_cursor.get("gender")
        u.schools = user_cursor.get("schools")
        u.school_type_list = []
        u.downloads = []

        #create a clean list of school types
        for school in u.schools:
            try:
                u.school_type_list.append(school["type"].encode('utf-8'))
            except (TypeError,AttributeError) as err:
                print(err)

        try:
            u.school_type = "|".join(u.school_type_list)
        except (TypeError, AttributeError) as err:
            print(err)
            u.school_type = ""

        try:
        # create a list of downloaded ids
            for doc in u.download_list:

                u.downloads.append(doc["doc_id"])
        except TypeError as err:
            print(err)


        try:

            temp_sub = []
            for subject in u.subjects_list:
                temp_sub.append(subject.encode('utf-8'))

            u.subjects = "|".join(temp_sub)


            tmp_realm = []
            for r in u.realms:
                tmp_realm.append(r)

            u.realm = " | ".join(tmp_realm)

            try:
                tmp_classes = []
                for c in u.school_classes:
                    tmp_classes.append(c)

                u.classes = " | ".join(tmp_classes)
            except (TypeError) as err:
                u.classes = ''

        except (TypeError,AttributeError) as err:
            print(err)

        return u

    def get_premium_users(self):
        """Fetchs a list of premium users from mongodb """
        client = MongoClient('mongo', 27017)
        db = client.mU.vws_Users
        result = db.find({'type': 2}).limit(10000)
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
        """Kicks off the data import """
        users  =  self.get_premium_users()


        for u in users:
          result = self.create_user_array(u)
          self.insert_data(result)

    def get_cursor(self):

        try:
            conn = mysql.connector.connect(user='root', password='alexandra', host='mysql', database='recommender')
            cursor = conn.cursor()


        except mysql.connector.Error as err:
            print(err)

        return cursor

    def insert_data(self, user_data):

        query = ""
        try:
            conn = mysql.connector.connect(user='root', password='alexandra', host='mysql', database='recommender')
            cursor = conn.cursor()

            for u in user_data:

                # print (args)
                #create query
                query = "INSERT INTO all_user_downloads (user_id, gender, country, schoolclasses, schools, subjects, realm, user_type, doc_id) "\
                        "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}')".format(u.id, u.gender, u.country, u.classes, u.school_type, u.subjects, u.realm, 2, u.doc_id)

                # execute it against the db
                cursor.execute(query)
            #commit the result
            conn.commit()
        except UnicodeEncodeError as err:
            print(err)
imp = Importer()
imp.ImportData()
# imp.get_sql_connection()