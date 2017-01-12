import mysql.connector as db
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Table, Column, ForeignKey, Sequence
from sqlalchemy.sql import select, text
from log import Logger
from config_loader import ConfigLoader

class MysqlRepository:
    def __init__(self):
        self.conn = None
        self.engine = None
        cfg = ConfigLoader()
        self.config = cfg.get_config()
        self.mysql_host = self.config.get('mysql_host')
        self.mysql_user = self.config.get('mysql_user')
        self.mysql_pass = self.config.get('mysql_pass')
        self.mysql_database = self.config.get('mysql_database')
        self.logging = Logger()
        conn_string = "mysql+mysqldb://{0}:{1}@{2}/{3}".format(self.mysql_user, self.mysql_pass,
                                                               self.mysql_host, self.mysql_database)
        self.engine = create_engine(conn_string)
        meta = MetaData(bind=self.engine)
        self.dbconn = None

        ### Recommendations Table ###
        self.recommendations = Table('product_recommendations', meta,
                                     Column('product_id', TEXT, nullable=False),
                                     Column('related_product_id', TEXT, nullable=False),
                                     Column('school_code', Integer, nullable=True),
                                     Column('subject_code', Integer, nullable=True),
                                     Column('class_year', Integer, nullable=True),
                                     Column('tag_similarity', Integer, nullable=True),
                                     Column('similarity', Integer, nullable=True),
                                     Column('similarity_score', Integer, nullable=True)
                                     )


    def connect(self):

        try:
            self.conn = db.connect(user=self.mysql_user, password=self.mysql_pass,
                                   host=self.mysql_host, database=self.mysql_database)

        except db.Error as err:
            print(err)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def setup_db(self):

        conn_string = "mysql+mysqldb://{0}:{1}@{2}/{3}".format(self.mysql_user, self.mysql_pass,
                                                                self.mysql_host, self.mysql_database)
        self.engine = create_engine(conn_string)
        meta = MetaData(bind=self.engine)

        ### Recommendations Table ###
        self.recommendations = Table('product_recommendations', meta,
                                     Column('product_id', TEXT, nullable=False),
                                     Column('related_product_id', TEXT, nullable=False),
                                     Column('school_code', Integer, nullable=True),
                                     Column('subject_code', Integer, nullable=True),
                                     Column('class_year', Integer, nullable=True),
                                     Column('tag_similarity', Integer, nullable=True),
                                     Column('similarity', Integer, nullable=True),
                                     Column('similarity_score', Integer, nullable=True)
                                     )


        # create tables in db
        meta.create_all(self.engine)

    def populate_data(self, products):
        if not self.conn:
            self.connect()

        products.to_sql('product_recommendations', self.conn, flavor='mysql', if_exists='append', index=True)

        self.logging.debug('Wrote {0} rows to mysql'.format(len(products)))

    def get_document_by_id(self, doc_id, docs_to_exclude):

        conn = self.engine.connect()
        # sel = select([self.recommendations]).where(self.recommendations.c.product_id == doc_id)

        # query excludes other school types from the recommendations
        # in theory a user will only be teaching at one school

        query = text(
            "Select * from product_recommendations where school_code = "
            "(select school_code from product_recommendations where product_id =:product_id and `index`=0 LIMIT 1)"
            "and product_id = :product_id order by similarity_score DESC;")
        result = conn.execute(query, product_id=doc_id)

        # we use this tuple to exclude already seen documents
        # they add no particular value
        exclusions = tuple(docs_to_exclude)
        recommendations = []
        for r in result:
            if not r["related_product_id"] in exclusions:
                # recommendation_item = {'related_product_id': r["related_product_id"], 'product_id': r["product_id"], 'tag_similarity': r["tag_similarity"], 'similarity_score': r["similarity_score"]}
                recommendation_item = {'doc_id': r['related_product_id']}
                recommendations.append(recommendation_item)
        result.close()
        return recommendations
