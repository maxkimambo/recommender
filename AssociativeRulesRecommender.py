from Worker import Worker
import fim
from RedisRepository import RedisRepository
from MongoRepository import MongoRepository


# get all downloads for user

# get a list of transactions

class AssociativeRulesRecommender:
    def __init__(self):
        self.redis = RedisRepository()

    def get_transactions(self):
        repo = MongoRepository()
        users_transactions = repo.get_user_downloads()
        transactions = []

        for t in users_transactions:

            # go over the keys and join the list of transactions
            for _, v in t.items():

                if len(v) > 1:
                    transactions.append(v)
        print("processing {0} transactions".format(len(transactions)))
        return transactions

    def get_frequent_items(self, transactions):
        # report='c',
        frequent_items = fim.apriori(transactions, target='r', prune=2, mode='y')
        return frequent_items

    def find_association_rules(self, transactions):

        rules = fim.arules(transactions)
        return rules

    def generate_key(self, rule_set):
        """Generates an identifier for a ruleset"""
        rule = rule_set[1]
        sorted_rule_list = sorted(rule)
        rule_key = ":".join(sorted_rule_list)
        return rule_key

    def record_results(self, key, rule):
        self.redis.store_binary(key, rule)
        pass


# sample input format
test_transaction = []
test_transaction.append(['gin', 'tonic', 'ice', 'tea'])
test_transaction.append(['gin', 'tonic', 'ice'])
test_transaction.append(['gin', 'tonic', 'ice', 'lemon'])
test_transaction.append(['sugar', 'coffee', 'water', 'melon'])
test_transaction.append(['sugar', 'coffee', 'water', 'milk', 'orange juice'])
test_transaction.append(['sugar', 'coffee', 'water', 'banana', 'orange juice'])
test_transaction.append(['sugar', 'coffee', 'water', 'eggs', 'orange juice'])
test_transaction.append(['sugar', 'coffee', 'water'])
test_transaction.append(['water', 'milk', 'juice', 'vodka'])
test_transaction.append(['sugar', 'milk', 'coffee'])
test_transaction.append(['sugar', 'milk', 'flour', 'yeast'])
test_transaction.append(['sugar', 'milk', 'yeast'])
test_transaction.append(['water', 'milk', 'coffee'])

mb = AssociativeRulesRecommender()
trx = mb.get_transactions()
# freq = mb.get_frequent_items(test_transaction)
# freq = mb.get_frequent_items(trx)
# print("frequent items {0}".format(len(freq)))
#
# for f in freq:
#     if (f[2] > 1):
#         print('------------------')
#         print("item set {0}".format(f))
#         print("frequency : {0}".format(f[2]))
#         print("")

rules = mb.find_association_rules(test_transaction)

for r in rules:
    print(r)
    r_key = mb.generate_key(r)
    mb.record_results(r_key, r)
    print("==========")
    # print(r[0])
    # print(type(r[2]))
    # for match in r[1]:
    #     print(match)
    # print(r[3])
    # print("--------")
