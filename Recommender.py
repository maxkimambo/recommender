from Worker import Worker
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sklearn.datasets as datasets


class Recommender:

    __coded_docs = object
    __docs = object
    # prepare the datasets
    worker = Worker()

    def prepare_item_item_data(self, product_matrix):
        all_documents = self.worker.process_document_data();


    def prepare_data(self):

        print("Started building document matrix")

        self.worker.process_document_data()
        doc_matrix = self.worker.build_document_matrix()
        docs = pd.DataFrame(doc_matrix)

        print("Finished building document matrix")

        return docs

    def get_tag_matrix(self, docs):
        tags = docs["tags"]
        # vectorise
        tfid_vectorizer = TfidfVectorizer()
        matrix = tfid_vectorizer.fit_transform(tags)

        return matrix

    def get_document_matrix(self, docs):
        coded_docs = docs[["class_year", "school_code", "subject_code"]]
        return coded_docs

    def calculate_tag_similarity(self, tag, tagMatrix):
        tags_similarity = cosine_similarity(tag, tagMatrix)
        return tags_similarity

    def calculate_document_similarity(self, doc, documentsMatrix):
        document_similarity = cosine_similarity(doc, documentsMatrix)

        return document_similarity

    def calculate_recommendations(self):
        product_matrix = self.worker.build_product_matrix()



    def get_recommendations(self, doc_id, count=5):
        """ Fetches item / item recommendations  """

        #calc tag similarity
        #calc document similarity
        #weighted average




        pass

    # # dataframe of coded documents
    # self.__coded_docs =
    #
    # ten_doc = self.__coded_docs[:10]
    #
    # docs_no_tags_similarity = cosine_similarity(ten_doc[:3], ten_doc)
    #
    # tag_list = worker.get_all_tags()
    # pass