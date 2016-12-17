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
            doc_row = {'id': doc.id,'school': doc_school_type, 'school_code': school_type, 'tags': tag_list,
            'class_year': class_year, 'subject': doc_subject, 'subject_code': subjects.get(doc_subject)}

            doc_matrix.append(doc_row)

        return doc_matrix

    def get_product_matrix_data(self, documents):
        """Fetches data from mongo and creates a format from which we can build a matrix"""
        product_matrix = []
        document_list = []
        counter = 0
        for doc in documents:

            if counter > 4:
                break

            doc_id = doc.get("id")
            # print(doc_id)

            downloads = doc.get("downloads")
            # print("downloads {0}".format(len(downloads)))

            result = self.repo.get_doc_by_id(doc_id)
            document_list.append(result) # main document


            # fetch all the related ones
            for d in downloads:
                document_list.append(self.repo.get_doc_by_id(d))

            counter += 1
            yield document_list
            document_list.clear()
        #     product_matrix.append(document_list)
        #
        # return product_matrix

    def build_downloaded_document_matrix(self, documents):
        """Builds a matrix on which we shall calculate similarity between the documents"""
        tags = self.get_document_tags()
        school_types = self.get_school_types()
        subjects = self.get_subjects()
        doc_matrix = []

        for doc in documents:

            try:
                doc_school_type = ",".join(doc.school_type)
                doc_subject = ",".join(doc.subject)

                if not school_types.get(doc_school_type):
                    school_type = 99
                    class_year = max(doc.class_years)

                else:
                    school_type = school_types.get(doc_school_type)
                    class_year = max(doc.class_years)

                if subjects.get(doc_subject):
                    doc_row = {'id': doc.id, 'school_code': school_type,
                               'class_year': class_year, 'subject_code': subjects.get(doc_subject), 'tags': doc.tag_collection}
                    doc_matrix.append(doc_row)

            except (AttributeError, ValueError, KeyError):
                pass

        print("document matrix has {0} docs".format(len(doc_matrix)))

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
            doc_row = {"id": doc.id, "downloads": []}
            for user in users:
                download_set = tuple(user.downloads)
                # find out if the user downloaded this document
                has_downloaded = doc.id in download_set
                try:
                    if (has_downloaded):

                        # go through other items this customer downloaded
                        # record that doc has been downloaded along with those items
                        # we will then use this info to calculate similarity between doc and other downloaded items

                        doc_row["downloads"] += user.downloads

                except TypeError as err:
                    traceback.print_tb(err)
                    pass

            # print("processing doc id : {0}".format(doc_row.get("id")))
            product_product_matrix.append(doc_row)

        print("constructed product matrix with {0} documents".format(len(product_product_matrix)))


        return product_product_matrix
