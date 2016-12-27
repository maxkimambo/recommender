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

    def get_data_frame(self, matrix):
        df = pd.DataFrame(matrix)
        return df

    def get_document_matrix(self, document_df):
        coded_docs = document_df[["class_year", "school_code", "subject_code"]]
        return coded_docs

    def get_tag_matrix(self, document_df):
        tags = document_df["tags"]
        # vectorise
        tfid_vectorizer = TfidfVectorizer()
        matrix = tfid_vectorizer.fit_transform(tags)

        return matrix

    def calculate_tag_similarity(self, tag, tagMatrix):
        tags_similarity = cosine_similarity(tag, tagMatrix)
        return tags_similarity

    def calculate_document_similarity(self, doc, document_matrix):
        document_similarity = cosine_similarity(doc, document_matrix)

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