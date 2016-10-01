from cassandra.cluster import Cluster
import ssl
import MysqlRepo
import LogMessage
import json

class CassandraImporter:

    def __init__(self, mysqlRepo):
        self.mysql_repo = mysqlRepo

    def fetch_log_messages(self):
        """ Fetches log messages from cassandra """
        ssl_cert_path = "/etc/cassandra/lana.cer"

        cluster = Cluster(['176.9.117.101', '144.76.93.244', '176.9.147.230'],
                          ssl_options=dict(ca_certs=ssl_cert_path, ssl_version=ssl.PROTOCOL_TLSv1))
        keyspace = 'plutarchus_4'

        session = cluster.connect(keyspace)
        query = "Select * from log_messages LIMIT 100"
        results = session.execute(query)

        for res in self.parse_results(results):
            next(res)
            print(res.specifier)

    def parse_results(self, results):

        for res in results:
            # do some processing of the results pack it into an object
            #yield it to a function that will write it into mysql

            log = LogMessage()
            log.client_id = res.clientId
            log.event_time = res.time
            log.input = res.input
            log.method = res.method
            log.realm = res.realm
            log.resource = res.resource
            log.specifier = res.specifier


            # process input
            #log.input = json.decode(res.input)

            # process results
            #log.result = json.decode(res.result)

            yield log


# create the repo

repo = MysqlRepo()

ci = CassandraImporter(repo)

ci.fetch_log_messages()
