from Worker import Worker

# program workflow
# worker Gets documents via the repo
# worker Gets users via the repo
# export documents along with main attributes  to csv
# export users to csv
# create a dataset of which users downloaded which documents
def main():
    print('starting worker....')
    worker = Worker()

    print("starting to process user data")
    #worker.process_user_data()

    print("starting to process document data")
    worker.process_document_data()

    # worker.get_school_types()

    # print("consturcting product matrix")
    product_matrix = worker.build_product_matrix()
    # worker.join_document_user_data()
    tag_list = worker.get_document_tags()

    schools = worker.get_school_types()
    path = '/app/output/'
    # worker.export_user_data(path + 'users.csv')
    # worker.export_document_data(path + 'documents.csv')


    # vectorizer = DictVectorizer()
    # text_vectorizer = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
    #
    # doc_features = []
    # for i in product_matrix:
    #     main_doc_features = worker.get_document_properties(i)
    #     for doc in product_matrix[i]:
    #
    #         feature = worker.get_document_properties(doc)
    #         if (any(feature)):
    #             doc_features.append(feature)
    #
    #     matrix = vectorizer.fit_transform(doc_features).toarray()
    #     text_vectorizer.fit_transform(doc_features)
    #     print(vectorizer.get_feature_names())
    #     print(matrix)
    #     #fetch features for each of the associated documents
    #     # for doc in product_matrix[i]:





    #calculate similarity matrix between the key and all the items in the list


if __name__ == "__main__":
    main()
