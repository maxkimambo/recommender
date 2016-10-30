from Worker import Worker


# program workflow
# worker Gets documents via the repo
# worker Gets users via the repo
# export documents along with main attributes  to csv
# export users to csv
# create a dataset of which users downloaded which documents
def main():
    worker = Worker()
    worker.process_document_data()
    worker.process_user_data()
    worker.join_document_user_data()

    path = '/app/output/'
    worker.export_user_data(path + 'users.csv')
    worker.export_document_data(path + 'documents.csv')


if __name__ == "__main__":
    main()
