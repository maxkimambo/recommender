from mongo_repo import mongoRepo


class DocumentInfo:
    repo = mongoRepo()

    def fetch_docs(self):
        document_list = self.repo.get_documents()
        return document_list


# Get 100 docs

# convert
# convert those docs into features