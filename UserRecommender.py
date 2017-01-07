import logging
import threading
from MongoRepository import MongoRepository
from MysqlRepository import MysqlRepository
from config_loader import ConfigLoader
from datetime import datetime, timedelta
from RedisRepository import RedisRepository


class UserRecommender:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                            )
        self.repo = MongoRepository()
        self.mysql = MysqlRepository()
        cfg = ConfigLoader()
        self.config = cfg.get_config()
        self.CUTTOFF_DAYS = timedelta(days=self.config.get('data_days_to_analyze'))
        self.redis = RedisRepository()
        self.recommendation_counter = 0

    def __get_all_users(self):
        users = self.repo.get_users()

        return users

    def __get_recent_downloads(self, downloads):
        # get downloads after a cutoff point
        self.cuttoff_date = datetime.now() - self.CUTTOFF_DAYS
        recent_downloads = []

        for d in downloads:
            if d["download_time"] > self.cuttoff_date:
                recent_downloads.append(d["doc_id"])
        if len(recent_downloads):
            logging.debug("Recent downloads identified : {0}".format(len(recent_downloads)))
        return recent_downloads

    def __get_topN_ar_recommendations(self, limit):
        """Fetches N top recommendations for a user from Association Rules store"""
        pass

    def __get_topN_cb_recommendations(self, limit):
        """Fetches N top recommendations for a user from CB filter store"""
        pass

    def generate_ar_recommendations_for_user(self, user_id, downloads):
        """Generates recommendatios for user by Associative rule mining"""

        # go through the list of downloads ids and find related docs
        recommendations = self.__find_related_items_ar(downloads)
        if recommendations:
            self.recommendation_counter += len(recommendations)
            self.record_user_recommendations(user_id, recommendations)

    def generate_cb_recommendations_for_user(self, user_id, downloads):
        """Generates recommendations for a user by CB Filtering"""
        recommendations = self.__find_related_items_cb(downloads)

        self.record_user_recommendations(user_id, recommendations)

    def record_user_recommendations(self, user_id, recommendations):
        """Stores generated recommendations in Redis"""
        key = "recommendation:{0}".format(user_id)
        self.redis.store_binary(key, recommendations)

    def process_ar_recommendations(self):
        """Drives the recommendation generation algorithm"""
        logging.debug("starting at {0}".format(datetime.now()))
        users = self.__get_all_users()

        logging.debug("Got {0} users to process ".format(len(users)))

        counter = 0
        for user in users:
            downloads = self.__get_recent_downloads(user.download_history)
            self.generate_ar_recommendations_for_user(user.id, downloads)
            counter += 1

        logging.debug("Generated {1} recommendations for {0} users".format(counter, self.recommendation_counter))

    def process_cb_recommendations(self):
        """Drives the content based recommendation generation algorithm"""
        users = self.__get_all_users()

        counter = 0
        for user in users:
            downloads = self.__get_recent_downloads(user.download_history)
            self.generate_cb_recommendations_for_user(user.id, downloads)
            counter += 1

        logging.debug("Generated recommendations for {0} users".format(self.recommendation_counter))

    def __find_related_items_ar(self, downloads):
        """Finds related items and holds filtering logic"""
        key_count = len(downloads)
        if key_count < 2:
            return
        # we need to build a combo to represent the redis key look a like and search via that
        sorted_downloads = sorted(downloads)
        recommendation_results = []

        # first pass highest specificity
        for i in range(1, key_count + 1):
            key_list = sorted_downloads[0:i]
            key = ":".join(key_list)
            result = self.redis.read_binary(key)
            if result:
                logging.debug(result)
                item_recommendation = {"id": result[0], "score": result[3]}
                recommendation_results.append(item_recommendation)

        # second pass just look for pairs
        for i in range(1, key_count + 1):
            limit = i + 2
            key_list = sorted_downloads[i:limit]
            key = ":".join(key_list)
            result = self.redis.read_binary(key)
            if result:
                logging.debug(result)
                item_recommendation = {"id": result[0], "score": result[3]}
                recommendation_results.append(item_recommendation)

        logging.debug("Recommendations: {0}".format(recommendation_results))
        return recommendation_results

    def __find_related_items_cb(self, downloads):
        """Finds related items and holds filtering logic"""
        recommendation_result = []
        for doc in downloads:
            self.mysql.get_document_by_id(doc)
