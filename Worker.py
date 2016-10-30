from mongo_repo import mongoRepo

class Worker:

    repo = mongoRepo()

    def process_user_data(self):
        # repo = mongoRepo()
        users = self.repo.get_premium_users()


    def export_user_data(self, path):
        pass

    def process_document_data(self):
        documents = self.repo.get_documents()
        print(len(documents))

    def export_document_data(self, path):
        pass