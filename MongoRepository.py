from pymongo import MongoClient
from bson.objectid import ObjectId
from Model import User
from Model import Document
from datetime import datetime
from time import strftime
from config_loader import ConfigLoader

class MongoRepository:
    download_counter = 0

    def __init__(self):

        cfg = ConfigLoader()
        self.config = cfg.load()
        print(self.config)
        self.MONGO_HOST = self.config.get('mongo_host')
        self.MONGO_PORT = self.config.get('mongo_port')
        self.USER_LIMIT = self.config.get('data_user_limit')
        self.DOC_LIMIT = self.config.get('data_doc_limit')
        self.MIN_DOWNLOADS = self.config.get('data_min_downloads')

        client = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        self.db = client.mU
        self.users = None

    def user_factory(self, user_cursor):
        """Creates user object from mongo cursor"""
        u = User()
        u.id = str(user_cursor.get("_id"))
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
                u.downloads.append(str(doc["doc_id"]))
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
            pass

        return u

    def document_factory(self, record):

        document = Document()

        try:
            document.id = str(record.get("_id"))
            document.title = record.get("qualifications")["title"]
            document.subtitle = record.get("qualifications")["subtitle"]
            document.issue = record.get("qualifications")["issue"]
            document.class_years = record.get("qualifications")["classYears"]
            document.school_type = record.get("qualifications")["schoolType"]
            document.subject = record.get("qualifications")["subject"]
            document.tags = []
            tags = record.get("qualifications")["tags"]

            for t in tags:
                document.tags.append(t.get("tag").lower())

            document.tag_collection = " ".join(map(str, document.tags))

            document.authors = record.get("qualifications")["author"]
            document.publisher = record.get("qualifications")["publishingHouse"]
            document.kind = record.get("type")

        except (KeyError, TypeError, AttributeError) as err:
            pass

        return document

    def get_doc_by_id(self, id):
        doc_cursor = self.db.mU_documents.find_one({'_id': ObjectId(id)})
        doc = self.document_factory(doc_cursor)
        return doc

    def get_documents(self):

        docs = self.db.mU_documents
        title_filter = ['Originaldokument',
                        'Titel',
                        'Titelseite',
                        'Inhaltsverzeichnis',
                        'Inhalt',
                        'Info',
                        'Einfuerhrung',
                        'EinfuFChung',
                        'EinfüFChung',
                        'Infoseite',
                        'Infoseiten',
                        'Quellenverzeichnis',
                        'Anhang',
                        'Glossar',
                        'Impressum',
                        'Verlaufsplanung',
                        'Verlausplanung',
                        'Literaturverzeichnis']

        result = docs.find(
            {"type": "mindItem", "status.active": True, "status.exists": True, "status.hexxlerRelease": True,
             "title": {"$nin": title_filter}}).limit(self.DOC_LIMIT)
        documentList = []

        for r in result:
            document = self.document_factory(r)
            documentList.append(document)

        return documentList

    def get_users(self):
        """Fetches a list of users from mongodb """

        self.users = self.db.vws_Users
        result = self.users.find({'active': True, 'marketing.mailings.customer.doubleOptIn': 'confirmed'}).limit(
            self.USER_LIMIT)
        user_list = []

        for r in result:
            user = self.user_factory(r)
            if len(user.downloads) > self.MIN_DOWNLOADS:
                user_list.append(user)

        return user_list

    def get_user_downloads(self):

        self.users = self.db.vws_Users
        result = self.users.find({'active': True, 'marketing.mailings.customer.doubleOptIn': 'confirmed'}).limit(
            self.USER_LIMIT)
        user_list = []

        for r in result:
            user_transactions = self.user_transaction_factory(r)
            if user_transactions:
                user_list.append(user_transactions)

        return user_list

    def user_transaction_factory(self, user_cursor):
        """Creates transaction object from mongo cursor"""
        u = User()
        u.id = str(user_cursor.get("_id"))
        u.download_list = user_cursor.get("downloadList")

        try:
            transaction = {}
            #e.g {'503a0123b2d700ed1400007b-2013-08-18': ['50a2bca4d789a700ddc7fec1', '50a2bca4d789a700ddc7fec0']}
            # create a list of downloaded ids
            for doc in u.download_list:
                doc_id = str(doc.get('doc_id'))

                if doc_id:
                    transaction_timestamp = datetime.utcfromtimestamp(int(doc['timestamp'] / 1000 / 86400) * 86400).strftime('%Y-%m-%d')
                    transaction_id = "{0}-{1}".format(u.id, transaction_timestamp)

                    doc_list = []

                    if transaction_id in transaction:
                        transaction[transaction_id].append(doc_id)
                    else:

                        doc_list.append(doc_id)
                        transaction = {transaction_id: doc_list }

            return transaction

        except TypeError as err:
            pass


