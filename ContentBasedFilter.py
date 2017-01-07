from Worker import Worker
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Recommender import Recommender
from config_loader import ConfigLoader
from log import Logger

class ContentBasedFilter:
    # Constants
    DOCS_TO_SHOW = 40
    SEPARATOR = '===================================================================================='

    def __init__(self):
        cfg = ConfigLoader()
        self.config = cfg.get_config()

        self.SIMILARITY_CUTOFF = self.config.get('similarity_cuttoff')
        self.logging = Logger()

    # pandas options
    pd.set_option('display.height', 1000)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    def generate_recommendations(self):
        self.logging.debug('starting worker....')
        worker = Worker()
        rec = Recommender()

        self.logging.debug("starting to process user data")
        worker.process_user_data()

        self.logging.debug("starting to process document data")
        worker.process_document_data()

        worker.get_all_tags()

        worker.get_school_types()

        self.logging.debug("constructing product matrix")
        product_matrix = worker.build_product_matrix()

        documents_data = worker.get_product_matrix_data(product_matrix)

        for doc_col in documents_data:
            # we dont want to process single item lists
            if len(doc_col) > 2:
                self.logging.debug("generating recommendations....")
                downloaded_documents_matrix = worker.build_downloaded_document_matrix(doc_col)
                df = rec.get_data_frame(downloaded_documents_matrix)
                yield self.process_document_collection(df)

    def process_document_collection(self, df):
        # make a dataframe based on tags only
        tags = df['tags']

        tfid_vectorizer = TfidfVectorizer()

        tag_matrix = tfid_vectorizer.fit_transform(tags)

        tag_similarity = cosine_similarity(tag_matrix[0:1], tag_matrix)
        doc_meta = df[["school_code", "subject_code", "class_year"]]

        tag_df = pd.DataFrame(tag_similarity)

        # tag_df.shape
        # (1, 719)

        # transppose the dataframe
        tag_df = tag_df.transpose()

        # combine both dataframes
        combined = pd.concat([doc_meta, tag_df], axis=1)

        # rename columns
        combined.columns = ['school_code', 'subject_code', 'class_year', 'similarity']

        # calculate document similarity
        document_similarity = cosine_similarity(combined[0:1], combined)

        # convert into dataframe
        doc_similarity_df = pd.DataFrame(document_similarity)

        # transpose the similarity dataframe
        doc_similarity_df = doc_similarity_df.transpose()

        combined_document_similarity = pd.concat([combined, doc_similarity_df], axis=1)

        combined_document_similarity.columns = ['school_code', 'subject_code', 'class_year', 'tag_similarity',
                                                'similarity']

        doc_similarity_matrix = pd.concat([df["id"], combined_document_similarity], axis=1)

        # Get rid of duplicate documents
        doc_similarity_matrix = doc_similarity_matrix.drop_duplicates("id")

        # sort documents based on similarity from highest to lowest
        doc_similarity_matrix.sort_values(["similarity"], ascending=False)

        # set cutoff point for similarity values
        # TODO: experiment with different cutoff values

        doc_similarity_matrix = doc_similarity_matrix[(doc_similarity_matrix["similarity"] > self.SIMILARITY_CUTOFF)]

        # drop off all rows where similarity is 0
        doc_similarity_matrix = doc_similarity_matrix[(doc_similarity_matrix["tag_similarity"] != 0)]

        document_similarity_table = doc_similarity_matrix.sort_values(["similarity", "tag_similarity"], ascending=False)

        document_similarity_table["similarity_score"] = (document_similarity_table["tag_similarity"] +
                                                         document_similarity_table["similarity"] / 2) * 100

        document_similarity_table = document_similarity_table.sort_values("similarity_score", ascending=False)

        if len(document_similarity_table.index):
            main_doc = document_similarity_table[0:1]

            main_product_id = main_doc.get_value(0, "id")

            self.logging.debug(self.SEPARATOR)
            self.logging.debug("processed product : {0} ".format(main_product_id))

            document_similarity_table["product_id"] = main_product_id
        else:
            document_similarity_table["product_id"] = "Dont know"
        # relabel the columns
        document_similarity_table.columns = ["related_product_id", "school_code", "subject_code",
                                             "class_year", "tag_similarity", "similarity", "similarity_score",
                                             "product_id"]

        # self.logging.debug(self.SEPARATOR)
        # self.logging.debug(document_similarity_table.head(self.DOCS_TO_SHOW))

        return document_similarity_table
