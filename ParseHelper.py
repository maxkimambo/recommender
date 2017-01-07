class ParseHelper:
    def parse_constraints(self, log, document):

        search_term = None
        subject = None
        constraints = None
        school_type = None
        class_years = None

        if document:

            constraints = document.get("constraint")

            if constraints:

                subject = self.get_subject(constraints)
                school_type = self.get_school_type(constraints)
                class_years = self.get_class_years(constraints)


        parsed_result = {'subject': subject, 'school_type': school_type,
                         'class_years': class_years}

        return parsed_result

    def get_class_years(self, constraints):
        class_years = None
        if constraints:
            raw_years = constraints.get("classYearsBlock")

            if type(raw_years) is dict:
                # check for and or
                if "$and" in raw_years:
                    class_years = raw_years.get("$and")
                if "$or" in raw_years:
                    class_years = raw_years.get("$or")
                if type(class_years) is list:
                    class_years = ":".join(class_years)
                    class_years = class_years.replace("/", ":")
                return class_years

            if type(raw_years) is list:
                class_years = ":".join(raw_years)
                class_years = class_years.replace("/", ":")

                return class_years

    def get_subject(self, constraints):

        subjects = ""

        if constraints:
            raw_subject = constraints.get("subject")

            # check which type is it
            if type(raw_subject) is dict:

                # do check for and or
                if "$and" in raw_subject:
                    subjects = raw_subject.get("$and")

                if "$or" in raw_subject:
                    subjects = raw_subject.get("$or")

                if type(subjects) is list:
                    subjects = ":".join(subjects)
                    # subjects = subjects.encode('utf8')
                return subjects

            if type(raw_subject) is list:
                subjects = ":".join(raw_subject)
                # subjects = subjects.encode('utf8')
            return subjects

        return subjects

    def get_search_term(self, document):
        search_term = ""
        if document:
            search_term = document.get("query")
            # search_term = search_term.encode('utf8')

        return search_term

    def get_school_type(self, constraint):

        school_type = ""
        if constraint:
            raw_school_type = constraint.get("schoolType")

            if type(raw_school_type) is dict:
                # check for existence of and or
                if "$and" in raw_school_type:
                    school_type = raw_school_type.get("$and")
                if "$or" in raw_school_type:
                    school_type = raw_school_type.get("$or")
                    # if "schoolType" in raw_school_type:
                    #     school_type = raw_school_type.get("schoolType")

            if type(raw_school_type) is list:
                school_type = "".join(raw_school_type)

            if type(school_type) is list:
                school_type = "".join(school_type)

        # school_type = school_type.encode('utf8')

        return school_type

    def get_user_ids(self, log):
        user_ids = ""
        if log:
            try:
                raw_ids = log.results[4]

                if type(raw_ids) is list:
                    user_ids = ":".join(raw_ids)
                return user_ids
            except (AttributeError, TypeError):
                pass

    def get_doc_ids(self, log):
        doc_ids = ""
        if log:
            try:
                raw_ids = log.results[5]

                if type(raw_ids) is list:
                    doc_ids = ":".join(raw_ids)
                return doc_ids
            except (AttributeError, TypeError):
                pass

    def get_link_ids(self, log):
        doc_ids = ""
        if log:
            try:
                raw_ids = log.results[6]

                if type(raw_ids) is list:
                    doc_ids = ":".join(raw_ids)
                return doc_ids
            except (AttributeError, TypeError):
                pass

    def get_desktop_ids(self, log):
        desktop_ids = ""
        if log:
            try:
                raw_ids = log.results[7]

                if type(raw_ids) is list:
                    desktop_ids = ":".join(raw_ids)
                return desktop_ids
            except (AttributeError, TypeError):
                pass

    def get_result_ids(self, log):
        result_ids = ""
        if log:
            try:
                raw_ids = log.resultsIds

                if type(raw_ids) is list:
                    result_ids = ":".join(raw_ids)
                return result_ids
            except (AttributeError, TypeError):
                pass

