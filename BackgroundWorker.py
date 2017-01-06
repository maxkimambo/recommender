from AssociativeRulesRecommender import AssociativeRulesRecommender
from ContentBasedFilter import ContentBasedFilter
from MysqlRepository import MysqlRepository
import time


class BackgroundWorker:
    def __init__(self):
        self.ar = AssociativeRulesRecommender()

    def generate_associative_rules(self):

        print('Generating association rules')
        ar_start = time.time()
        transactions = self.ar.get_transactions()

        rules = self.ar.find_association_rules(transactions)

        print('Starting to record the rules')
        for r in rules:
            r_key = self.ar.generate_key(r)
            self.ar.record_results(r_key, r)
        print('finished')
        print('{0} rules generated'.format(len(rules)))
        ar_end = time.time()

        print("Rule generation took {0} seconds".format(ar_end - ar_start))

    def generate_rule_based_recommendations(self):
        pass

        # get recent downloads for each user
        # compare against the rules
        # write out recommendations

    def calculate_content_based_similarity(self):

        cf_start = time.time()
        recommender = ContentBasedFilter()
        repo = MysqlRepository()

        print('Generating content based recommendations')
        product_recommendations = recommender.generate_recommendations()

        print('Done ...')

        print('Writing recommendations to Mysql...')
        for rec in product_recommendations:
            repo.populate_data(rec)

        cf_end = time.time()
        print('finished generating CB recommendations in {0} seconds'.format(cf_end - cf_start))

    def generate_content_based_recommendations(self):
        pass

        # get recent downloads for each user
        # compare against the rules
        # write out recommendations
