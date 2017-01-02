from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import ssl
import re
from Model import LogMessage
from Model import LogMessage
import json
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Text, Integer, String, Table, Column, ForeignKey, DateTime
from sqlalchemy import insert
from datetime import datetime

class CassandraImporter:
    def __init__(self):
        self.connection = None
        self.engine = create_engine('mysql+mysqlconnector://root:cassandro@localhost/analytics')
        self.CLUSTER = ['176.9.117.101', '144.76.93.244', '176.9.147.230']
        self.KEYSPACE = 'plutarchus_4'
        self.PAGE_SIZE = 5000
        self.progress_counter = 0
        self.restart_count = 0
        self.errors = ""

    def fetch_log_messages(self):
        """ Fetches log messages from cassandra """
        ssl_cert_path = "/etc/cassandra/lana.cer"
        # ssl_cert_path = "lana.cer"

        cluster = Cluster(self.CLUSTER,
                          ssl_options=dict(ca_certs=ssl_cert_path, ssl_version=ssl.PROTOCOL_TLSv1))

        try:

            session = cluster.connect(self.KEYSPACE)
            print("Connection established")
            # query = "Select * from log_messages"

            query = "select * from log_messages WHERE time >= '2016-01-01' ALLOW FILTERING"
            statement = SimpleStatement(query, fetch_size=self.PAGE_SIZE)

            results = session.execute(statement)

            session_state = {'paging_stage': results.paging_state}

            for res in self.parse_results(results):
                #self.insert_to_sql(res)
                self.progress_counter += 1
                if (self.progress_counter % 100) == 0:
                    print("--------------------- ***--------------------------")
                    print('processed {0} events '.format(self.progress_counter))
                    print('restart count {0}'.format(self.restart_count))
                    print('errors occured {0}'.format(self.errors))
                    print('----------------------------------------------------')
        except Exception as err:
            # restart the process on failure
            print('Error occured {0} ... restarting ....'.format(err))
            self.restart_count += 1
            self.errors += str(err)
            ps = session_state['paging_stage']
            self.resume(ps)

    def resume(self, ps):

        """ Fetches log messages from cassandra """
        ssl_cert_path = "/etc/cassandra/lana.cer"

        cluster = Cluster(self.CLUSTER,
                          ssl_options=dict(ca_certs=ssl_cert_path, ssl_version=ssl.PROTOCOL_TLSv1))

        try:

            session = cluster.connect(self.KEYSPACE)
            print("Connection established")
            query = "Select * from log_messages"
            statement = SimpleStatement(query, fetch_size=self.PAGE_SIZE)

            results = session.execute(statement, paging_state=ps)
            session_state = {'paging_stage': results.paging_state}

            for res in self.parse_results(results):
                self.insert_to_sql(res)
                self.progress_counter += 1
                if (self.progress_counter % 100) == 0:
                    print("--------------------- ***--------------------------")
                    print('processed {0} events '.format(self.progress_counter))
                    print('restart count {0}'.format(self.restart_count))
                    print('errors occured {0}'.format(self.errors))
                    print('----------------------------------------------------')
        except Exception as err:
            # restart the process on failure
            print('Error occured {0} ... restarting ....'.format(err))
            self.restart_count += 1
            self.errors += str(err)
            ps = session_state['paging_stage']
            self.resume(ps)

    def parse_results(self, results):

        for res in results:
            log = LogMessage()
            yield log.parse(res)

    def connect(self):
        if not self.connection:
            self.connection = self.engine.connect()
        return self.connection

    def insert_to_sql(self, log):

        conn = self.connect()

        metadata = MetaData(bind=self.engine)

        log_messages = Table('log_messages_2016', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('client_id', Text),
                             Column('event_time', DateTime),
                             Column('days_since_registration', Integer),
                             Column('request_input', Text),
                             Column('request_method', Text),
                             Column('realm', Text),
                             Column('resource', Text),
                             Column('specifier', Text),
                             Column('error_count', Integer),
                             Column('request_id', Text),
                             Column('results', Text),
                             Column('user_ids', Text),
                             Column('document_ids', Text),
                             Column('link_ids', Text),
                             Column('desktop_ids', Text),
                             Column('results_ids', Text),
                             Column('routing_key', Text),
                             Column('user_id', Text),
                             Column('email', Text),
                             Column('url', Text),
                             Column('input_client_id', Text),
                             Column('input_specifier', Text),
                             Column('input_params', Text),
                             Column('input_document', Text),
                             Column('input_command', Text),
                             Column('input_constraint', Text),
                             Column('input_query', Text),
                             Column('subject_filter', Text),
                             Column('class_years_filter', Text),
                             Column('search_term', Text),
                             Column('school_type_filter', Text)
                             )

        try:

            stmt = log_messages.insert()
            conn.execute(stmt, log.__dict__)

        except Exception as err:
            print(err)
            print('Carrying on as if nothing happened ... ')


# create the repo
ci = CassandraImporter()
ci.fetch_log_messages()
