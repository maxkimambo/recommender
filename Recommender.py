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

    # def prepare_item_item_data(self, product_matrix):
    #     print("preparing unique items")
    #     pdf = pd.DataFrame(product_matrix)
    #     #check for duplicates
    #     pdf["is_dup"] = pdf.duplicated(["id"])
    #     dupes = pdf["is_dup"].sum()
    #
    #
    #     print('removing {0} duplicates'.format(dupes))
    #
    #     unique_docs = pdf.loc[pdf['is_dup'] == False]
    #
    #     return unique_docs

    # def prepare_document_data(self, doc_row):
    #
    #     print(doc_row)
    #
    # def prepare_data(self):
    #
    #     print("Started building document matrix")
    #
    #     self.worker.process_document_data()
    #     doc_matrix = self.worker.build_document_matrix()
    #     docs = pd.DataFrame(doc_matrix)
    #
    #     print("Finished building document matrix")
    #
    #     return docs



    # def get_document_matrix(self, docs):
    #     #dataframe docs
    #     coded_docs = docs[["class_year", "school_code", "subject_code"]]
    #     return coded_docs



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