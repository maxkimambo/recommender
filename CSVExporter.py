import csv


#TODO: clean up unwanted fields from being exported.

class CSVExporter:
    def export_users(self, path, userList):
        with open(path, "wb") as f:
            fieldnames = ["id", "gender", "country", "classes", "school_type", "subjects", "realm", "doc_id", 'city', 'school_type_list', 'area_code', 'school_classes', 'realms', 'schools', 'subjects_list']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for user in userList:
                writer.writerow(user.__dict__)