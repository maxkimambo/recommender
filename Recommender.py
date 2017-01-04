from Worker import Worker
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sklearn.datasets as datasets


class Recommender:

    __coded_docs = None
    __docs = None
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

