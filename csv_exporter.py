import csv


# TODO: clean up unwanted fields from being exported.

class CSVExporter:
    def export_users(self, path, userList):
        with open(path, "wb") as f:
            fieldnames = ["id", "gender", "country", "classes", "school_type", "subjects", "realm", "doc_id", 'city',
                          'school_type_list', 'area_code', 'school_classes', 'realms', 'schools', 'subjects_list']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # writer.writeheader()
            for user in userList:
                del user.downloads
                del user.download_list
                writer.writerow(user.__dict__)

    def export_documents(self, path, documentList):
        with open(path, "wb") as f:
            fieldnames = ["id", "title", "subtitle", "issue", "school_type", "class_years", "tags", "authors", "publisher", "kind"]
            writer = csv.DictWriter(f, fieldnames)
            # writer.writeheader()
            for doc in documentList:
                writer.writerow(doc.__dict__)

