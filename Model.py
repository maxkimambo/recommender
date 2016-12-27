import re
from pprint import pprint
import json
from ParseHelper import ParseHelper


class Document:
    def __str__(self):
        string_obj = ""
        for k, v in self.__dict__.items():
            string_obj += " {0}: {1} ".format(k, v)

        return string_obj


class User:
    pass


class LogMessage:
    def parse(self, row):
        helper = ParseHelper()
        request_input = json.loads(row.input)
        params = request_input.get("parameter")
        log = LogMessage()
        log.client_id = row.clientId
        log.event_time = row.time
        log.days_since_registration = row.daysSinceRegistered
        log.request_method = row.method
        log.realm = row.realm
        log.resource = row.resource
        log.specifier = row.specifier
        log.error_count = row.errorCount
        log.request_id = row.requestId


        try:

            log.user_ids = helper.get_user_ids(row)
            log.document_ids = helper.get_doc_ids(row)
            log.link_ids = helper.get_link_ids(row)
            log.desktop_ids = helper.get_desktop_ids(row)
            log.result_ids = helper.get_result_ids(row)

            log.routing_key = row.routingKey
            log.user_id = row.user[0]
            log.email = row.user[1]
            log.url = row.input[10]
            log.input_client_id = request_input.get("clientId")
            log.input_resource = request_input.get("resource")
            log.input_specifier = request_input.get("specifier")

            log.input_params = json.dumps(request_input.get("parameter"))

            document = params.get("document")
            result = helper.parse_constraints(log, document)
            log.search_term = helper.get_search_term(document)

            log.subject_filter = result.get('subject')
            log.school_type_filter = result.get('school_type')
            log.class_years_filter = result.get('class_years')
            log.input_document = json.dumps(document)
            log.input_command = params.get("command")

            log.input_constraint = json.dumps(params.get("constraint"))
            log.input_query = json.dumps(params.get("query"))



        except (AttributeError, TypeError) as err:
            print(err)

        return log

    def __str__(self):
        string_obj = ""
        for k, v in self.__dict__.items():
            print("----------------------------------\r\n")
            string_obj += " {0} : {1} ".format(k, v)

        return string_obj
