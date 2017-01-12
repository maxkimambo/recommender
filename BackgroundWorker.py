from AssociativeRulesRecommender import AssociativeRulesRecommender
from ContentBasedFilter import ContentBasedFilter
from MysqlRepository import MysqlRepository
import time
from log import Logger
import threading


class BackgroundWorker:
    def __init__(self):
        self.ar = AssociativeRulesRecommender()
        self.logging = Logger()

    def generate_associative_rules(self):

        self.logging.debug('Generating association rules')
        ar_start = time.time()
        transactions = self.ar.get_transactions()

        rules = self.ar.find_association_rules(transactions)

        self.logging.debug('Starting to record the rules')
        for r in rules:
            r_key = self.ar.generate_key(r)
            self.ar.record_results(r_key, r)
        self.logging.debug('finished')
        self.logging.debug('{0} rules generated'.format(len(rules)))
        ar_end = time.time()

        self.logging.debug("Rule generation took {0} seconds".format(ar_end - ar_start))

    def calculate_content_based_similarity(self):

        cf_start = time.time()
        recommender = ContentBasedFilter()
        repo = MysqlRepository()

        self.logging.debug('Generating content based recommendations')
        product_recommendations = recommender.generate_recommendations()

        for rec in product_recommendations:
            self.logging.debug('Writing {0} recommendations to Mysql...'.format(len(rec)))
            repo.populate_data(rec)
        cf_end = time.time()
        self.logging.debug('finished generating CB recommendations in {0} seconds'.format(cf_end - cf_start))
