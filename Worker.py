from mongo_repo import mongoRepo
from csv_exporter import CSVExporter


class Worker:
    repo = mongoRepo()
    users = []
    documents = []
    exporter = CSVExporter()

    def process_user_data(self):
        self.users = self.repo.get_premium_users()

    def export_user_data(self, path):
        self.exporter.export_users('users.csv', self.users)

    def process_document_data(self):
        self.documents = self.repo.get_document_ids()

    def export_document_data(self, path):
        self.exporter.export_documents('docs.csv', self.documents)

    def __join_document_user_data(self, users, documents):
        print('user count {0}'.format(len(users)))
        print('documents count {0}'.format(len(documents)))

    def join_document_user_data(self):
        self.__join_document_user_data(self.users, self.documents)

    def build_product_matrix(self):
        return self.__build_product_matrix(self.users, self.documents)

    def __build_product_matrix(self, users, documents):

        doc_set = tuple(documents)

        # amazon v1 algo
        # http://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
        product_matrix = {}
        # Go throgh all products
        for doc in doc_set:
            for user in users:
                download_set = tuple(user.downloads)
                # find out if the user downloaded this document
                has_downloaded = doc.id in download_set
                print("checking document {0} for user {2} it was {1}".format(doc.id, has_downloaded, user.id))
                if (has_downloaded):
                    print(doc.id)
                    # go through other items this customer downloaded
                    # record that doc has been downloaded along with those items
                    # we will then use this info to calculate similarity between doc and other downloaded items
                    for download in user.downloads:
                        product_matrix[download.id] = doc.id

        return product_matrix