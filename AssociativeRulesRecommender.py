from Worker import Worker
import fim

from mongo_repo import mongoRepo


# get all downloads for user

# get a list of transactions

class AssociativeRulesRecommender:
    def get_transactions(self):
        repo = mongoRepo()
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
        frequent_items = fim.apriori(transactions, target='r',  prune=2, mode='y')
        return frequent_items

    def find_association_rules(self, transactions):

        rules = fim.arules(transactions)
        return rules

# sample input format
test_transaction = []
test_transaction.append(['gin', 'tonic', 'ice', 'tea'])
test_transaction.append(['gin', 'tonic', 'ice'])
test_transaction.append(['gin', 'tonic', 'ice', 'lemon'])
test_transaction.append(['sugar', 'coffee', 'water'])
test_transaction.append(['sugar', 'coffee', 'water'])
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