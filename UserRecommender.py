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
        self.ar_counter = 0
        self.cb_counter = 0

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

    def get_topN_ar_recommendations(self, user_id, limit=10):
        """Fetches N top recommendations for a user from Association Rules store"""
        key = "recommendation:ar:{0}".format(user_id)
        result = self.redis.read_binary(key)
        top_n = []
        rec_list = result[0:limit]

        for rec in rec_list:
            # first item is the recommendation
            top_n.append(rec[0])

        logging.debug("recs for user {0} : {1}".format(user_id, top_n))

        return top_n

    def get_topN_cb_recommendations(self, user_id, limit=10):
        """Fetches N top recommendations for a user from CB filter store"""
        key = "recommendation:cb:{0}".format(user_id)
        result = self.redis.read_binary(key)
        top_n = []
        rec_list = result[0:limit]

        for rec in rec_list:
            top_n.append(rec.get('doc_id'))

        logging.debug("recs for user {0} : {1}".format(user_id, top_n))
        return top_n

    def get_top_n_combined_recommendations(self, user_id, limit=10):
        """Convenience method to combine both recommenders in one call"""
        ar = self.get_topN_ar_recommendations(user_id, limit)
        cb = self.get_topN_cb_recommendations(user_id, limit)

        return ar + cb

    def generate_ar_recommendations_for_user(self, user_id, downloads):
        """Generates recommendatios for user by Associative rule mining"""
        recommendation_type = "ar"
        # go through the list of downloads ids and find related docs
        recommendations = self.__find_related_items_ar(downloads)
        if recommendations:
            self.ar_counter += len(recommendations)
            self.record_user_recommendations(user_id, recommendation_type, recommendations)

    def generate_cb_recommendations_for_user(self, user_id, downloads):
        """Generates recommendations for a user by CB Filtering"""
        recommendation_type = "cb"
        recommendations = self.__find_related_items_cb(downloads)

        #recs are a list of dictionaries
        # [{'product_id': '50464e9ab92d2a47a4c94595', 'related_product_id': '50464e87b92d2a47a4c938b2',
        # 'similarity_score': 54.197352130201196, 'tag_similarity': 0.04769175627333097}]

        # trying this format for now ignore above
        #[{'doc_id': '51260e38d8d2ce66c47fdd04'}]

        if recommendations:
            self.record_user_recommendations(user_id, recommendation_type, recommendations)

        self.cb_counter += len(recommendations)
        logging.debug("Generated {0} recommendations for user {1}".format(len(recommendations), user_id))

    def record_user_recommendations(self, user_id, rec_type, recommendations):
        """Stores generated recommendations in Redis"""
        key = "recommendation:{1}:{0}".format(user_id, rec_type)
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

        logging.debug("Generated {1} AR recommendations for {0} users".format(counter, self.ar_counter))

    def process_cb_recommendations(self):
        """Drives the content based recommendation generation algorithm"""
        users = self.__get_all_users()

        counter = 0
        for user in users:
            downloads = self.__get_recent_downloads(user.download_history)
            self.generate_cb_recommendations_for_user(user.id, downloads)
            counter += 1

        logging.debug("Generated {1} CB recommendations for {0} users".format(counter, self.cb_counter))

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
            recs = self.mysql.get_document_by_id(doc, downloads)
            if recs:
                recommendation_result += recs
        return recommendation_result
