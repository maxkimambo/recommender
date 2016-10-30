from mongo_repo import mongoRepo

class DocsImporter:

    repo = mongoRepo()

    def import_documents(self):
        self.repo.get_documents()


docs = DocsImporter()
docs.import_documents()
