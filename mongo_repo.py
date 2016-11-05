from pymongo import MongoClient
from Model import User
from Model import Document


class mongoRepo:
    download_counter = 0

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.users = client.mU.vws_Users
        self.docs = client.mU.mU_documents

    def user_factory(self, user_cursor):
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

        # create a clean list of school types
        for school in u.schools:
            try:
                u.school_type_list.append(school["type"].encode('utf-8'))
            except (KeyError, TypeError, AttributeError) as err:
                pass

        try:
            u.school_type = "|".join(u.school_type_list)
        except (TypeError, AttributeError) as err:
            u.school_type = ""

        try:
            # create a list of downloaded ids
            for doc in u.download_list:
                u.downloads.append(doc["doc_id"])
        except TypeError as err:
            pass

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

        except (TypeError, AttributeError) as err:
            print("")

        return u

    def document_factory(self, record):

        document = Document()

        try:
            document.id = record.get("_id")
            document.title = record.get("qualifications")["title"]
            document.subtitle = record.get("qualifications")["subtitle"]
            document.issue = record.get("qualifications")["issue"]
            # extract class years and scholl type

            educationLevels = record.get("qualifications")["educationlevels"]
            document.class_years = []
            document.school_type = []
            for level in educationLevels:
                document.school_type += level.get("schoolType")["name"]
                document.class_years += level.get("class_years")

            document.tags = []
            tags = record.get("qualifications")["tags"]
            for t in tags:
                document.tags.append(t["tag"])

            document.authors = record.get("qualifications")["author"]
            document.publisher = record.get("qualifications")["publishingHouse"]
            document.kind = record.get("type")

        except (KeyError, TypeError, AttributeError) as err:
            pass

        return document

    def get_documents(self):

        client = MongoClient('mongo', 27017)
        docs = client.mU.mU_documents
        result = docs.find({})

        documentList = []
        for r in result:
            document = self.document_factory(r)
            documentList.append(document)
        return documentList

    def get_premium_users(self):
        """Fetches a list of premium users from mongodb """
        client = MongoClient('mongo', 27017)
        self.users = client.mU.vws_Users
        result = self.users.find({'type': 2})
        user_list = []

        for r in result:
            user = self.user_factory(r)

            # print("User id: {0} processing ".format(user.id))
            # print("Download count is : {0}".format(len(user.downloads)))
            # print("\t")
            # print("===============================")
            # for d in user.downloads:
            #
            #     try:
            #         # print(d)
            #     except AttributeError:
            #         print("")

            self.download_counter += len(user.downloads)
            # print("===============================")
            user_list.append(user)

        return user_list
