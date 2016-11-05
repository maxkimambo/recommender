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
        print('user count {0}'.format(len(users)))
        print('documents count {0}'.format(len(documents)))

    def join_document_user_data(self):
        self.__join_document_user_data(self.users, self.documents)

    def build_product_matrix(self, users, documents):
        # amazon v1 algo
        #http://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
        product_matrix = {}
        # Go throgh all products
        for doc in documents:
            for user in users:
                #find out if the user downloaded this document
                has_downloaded = doc.id in user.downloads
                if (has_downloaded):
                    #go through other items this customer downloaded
                    #record that doc has been downloaded along with those items
                    # we will then use this info to calculate similarity between doc and other downloaded items
                    for download in user.downloads:
                       product_matrix[download.id] = doc.id
