from mongo_repo import mongoRepo
import traceback
from csv_exporter import CSVExporter


class Worker:
    repo = mongoRepo()
    users = []
    documents = []

    def process_user_data(self):
        print('Retrieving user data ... ')
        self.users = self.repo.get_users()
        print('Done...')

    def process_document_data(self):
        print("processing document data .... ")
        self.documents = self.repo.get_documents()
        print("got {0} documents".format(len(self.documents)))

    def build_product_matrix(self):
        return self.__build_product_matrix(self.users, self.documents)

    def get_school_types(self):

        school_types = {}
        counter = 1

        for doc in self.documents:

            try:
                school_type = ",".join(doc.school_type) 
                if not school_types.get(school_type):
                    school_types[school_type] = counter
                    counter += 1
            except (AttributeError, NameError) as err:
                pass

        return school_types

    def get_all_tags(self): 
        tags = []
        for doc in self.documents: 
            try: 
                tags += doc.tags
            except(AttributeError): 
                pass 
        return tags 

    def get_document_tags(self):

        tag_list = {}

        for doc in self.documents:
            try:
                tags = " ".join(doc.tags)
                tag_list[doc.id] = tags
            except (TypeError, AttributeError):
                pass

        return tag_list
    
    def get_subjects(self): 

        subject_list = {}
        counter = 1

        for doc in self.documents: 
            try: 
                doc_subject = ",".join(doc.subject)
                if not subject_list.get(doc_subject): 
                    subject_list[doc_subject] = counter
                    counter += 1
            except AttributeError: 
                pass
        return subject_list

    def build_document_matrix(self):
        
        tags = self.get_document_tags()
        school_types = self.get_school_types()
        subjects = self.get_subjects()
        doc_matrix = []


        for doc in self.documents:
            
            try:
                doc_school_type = ",".join(doc.school_type)
                doc_subject = ",".join(doc.subject)
                
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
            doc_row = {'id': doc.id,'school': doc_school_type , 'school_code': school_type, 'tags': tag_list, 
            'class_year': class_year, 'subject': doc_subject, 'subject_code': subjects.get(doc_subject)}

            doc_matrix.append(doc_row)

        return doc_matrix

    def __build_product_matrix(self, users, documents):
        doc_set = tuple(documents)

        if not self.users:
            self.process_user_data()

        if not self.documents:
            self.process_document_data()

        # amazon v1 algo
        # http://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
        product_product_matrix = []

        print("checking downloads for {0} users".format(len(users)))
        print("checking downloads for {0} docs".format(len(doc_set)))

        # Go through all products
        for doc in doc_set:
            doc_row = {}
            for user in users:
                download_set = tuple(user.downloads)
                # find out if the user downloaded this document
                has_downloaded = doc.id in download_set
                try:
                    if (has_downloaded):

                        # go through other items this customer downloaded
                        # record that doc has been downloaded along with those items
                        # we will then use this info to calculate similarity between doc and other downloaded items
                        # print(doc.id)
                        if doc_row.get(doc.id):
                           doc_row.get(doc.id).append(user.downloads)
                        else:
                            doc_row = {doc.id: user.downloads}

                        product_product_matrix.append(doc_row)

                except TypeError as err:
                    traceback.print_tb(err)
                    pass

        print("constructed product matrix with {0} documents".format(len(product_product_matrix)))


        return product_product_matrix
