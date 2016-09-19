import mongo_repo as mongo


class DataManager:
    def __init__(self, mongoRepo):
        self.mongo_repo = mongoRepo

    # def filter_values(self, data):
    # def pluck_properties(self, user):

    def filter(self, user_data):
        clean_data = []
        props = ['_id', 'downloadList', 'realms', 'schoolclasses', 'subjects', 'city', 'country', 'areaCode', 'gender',
                 'schools']

        p = user_data.__dict__.keys()

        print('this is new')
        # print(p)

    def get_data(self):
        users = self.mongo_repo.get_premium_users(0, 10)
        for u in users:
            filter(u)

