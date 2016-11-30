from mongo_repo import mongoRepo
from csv_exporter import CSVExporter


class Worker:
    repo = mongoRepo()
    users = []
    documents = []

    def process_user_data(self):
        self.users = self.repo.get_premium_users()

    def get_document_properties(self, id):
        doc = self.repo.get_document_features(id)
        # create a dict of a doc features

        # del doc.kind
        document = {}
        try:
            # document["id"] = doc.id
            document["title"] = doc.title
            document["subtitle"] = doc.subtitle
            # document["authors"] = doc.authors
            document["tags"] = doc.tags
        except (AttributeError):
            pass

        return document

    def process_document_data(self):
        self.documents = self.repo.get_documents()
        print("got {0} documents".format(len(self.documents)))

    def build_product_matrix(self):
        return self.__build_product_matrix(self.users, self.documents)

    def get_school_types(self):

        school_types = {}
        counter = 1

        for doc in self.documents:

            try:
                school_type = "".join(doc.school_type) 
                if not school_types.get(school_type):
                    school_types[school_type] = counter
                    counter += 1
            except (AttributeError, NameError) as err:
                pass

        return school_types

    def get_document_tags(self):

        tag_list = {}

        for doc in self.documents:
            tags = " ".join(doc.tags)
            tag_list[doc.id] = tags
            try:
                tags = " ".join(doc.tags)
                tag_list[doc.id] = tags
            except TypeError:
                pass

        return tag_list

    def build_document_matrix(self):
        tags = self.get_document_tags()
        school_types = self.get_school_types()

        doc_matrix = []

        for doc in self.documents:
            doc_school_type = " ".join(doc.school_type)

            try:
                if not school_types.get(doc_school_type):
                    school_type = 99
                    tag_list = tags.get(doc.id)
                    class_year = max(doc.class_years)
                else:
                    school_type = school_types.get(doc_school_type)
                    tag_list = tags.get(doc.id)
                    class_year = max(doc.class_years)

            except (AttributeError, ValueError):
                school_type = 99
                tag_list = ''
                class_year = 99
            doc_row = {'id': doc.id, 'school': school_type, 'tags': tag_list, 'class_year': class_year}

            doc_matrix.append(doc_row)

        return doc_matrix
        # for doc in self.documents:
        # {id, title, subtitle, schoolType, class years, tags}

    def __build_product_matrix(self, users, documents):
        doc_set = tuple(documents)

        # amazon v1 algo
        # http://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
        product_product_matrix = {}

        print("checking downloads for {0} users".format(len(users)))
        print("checking downloads for {0} docs".format(len(doc_set)))

        # Go through all products
        for doc in doc_set:
            for user in users:
                download_set = tuple(user.downloads)
                # find out if the user downloaded this document
                has_downloaded = doc.id in download_set
                if (has_downloaded):

                    # go through other items this customer downloaded
                    # record that doc has been downloaded along with those items
                    # we will then use this info to calculate similarity between doc and other downloaded items
                    if not doc in product_product_matrix:
                        product_product_matrix[doc] = user.downloads
                    else:
                        product_product_matrix[doc].append(user.downloads)
        print("constructed produc matrix with {0} documents".format(len(product_product_matrix)))
        return product_product_matrix
