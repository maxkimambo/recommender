from mongo_repo import mongoRepo


class Worker:
    repo = mongoRepo()
    users = []
    documents = []

    def process_user_data(self):
        self.users = self.repo.get_premium_users()

    def export_user_data(self, path):
        pass

    def process_document_data(self):
        self.documents = self.repo.get_documents()

    def export_document_data(self, path):
        pass

    def __join_document_user_data(self, users, documents):
        pass

    def join_document_user_data(self):
        self.__join_document_user_data(self.users, self.documents)
