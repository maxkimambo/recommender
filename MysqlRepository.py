import mysql.connector as db
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Table, Column, ForeignKey
import pandas as pd
from config_loader import ConfigLoader

class MysqlRepository:
    def __init__(self):
        self.conn = None
        self.engine = None
        cfg = ConfigLoader()
        self.config = cfg.get_config()
        self.mysql_host = self.config.mysql_host
        self.mysql_user = self.config.mysql_user
        self.mysql_pass = self.config.mysql_pass
        self.mysql_database = self.config.mysql_database

    def connect(self):
        try:
            self.conn = db.connect(user=self.mysql_user, password=self.mysql_pass,
                                   host=self.mysql_host, database=self.mysql_database)
            cursor = self.conn.cursor()
            return cursor
        except db.Error as err:
            print(err)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def setup_db(self):

        conn_string = "mysql+mysqldb://{0}:{1} @{2}/{3}".format(self.mysql_user, self.mysql_pass,
                                                                self.mysql_host, self.mysql_database)
        self.engine = create_engine(conn_string)
        meta = MetaData(bind=self.engine)

        ### Recommendations Table ###
        table_recommendations = Table('product_recommendations', meta,
                                      Column('product_id', TEXT, nullable=False),
                                      Column('related_product_id', TEXT, nullable=False),
                                      Column('school_code', Integer, nullable=True),
                                      Column('subject_code', Integer, nullable=True),
                                      Column('class_year', Integer, nullable=True),
                                      Column('tag_similarity', Integer, nullable=True),
                                      Column('similarity', Integer, nullable=True),
                                      Column('similarity_score', Integer, nullable=True)
                                      )

        ### Recommendations Table ###
        related_products = Table('related_product_recommendations', meta,
                                 Column('id', Integer, primary_key=True, autoincrement=False),
                                 Column('product_id', TEXT, nullable=False),
                                 Column('related_product_id', TEXT, nullable=False),
                                 Column('school_code', Integer, nullable=True),
                                 Column('subject_code', Integer, nullable=True),
                                 Column('similarity', Integer, nullable=True),
                                 Column('tag_similarity', Integer, nullable=True),
                                 Column('similarity_score', Integer, nullable=True)
                                 )
        # create tables in db
        meta.create_all(self.engine)

    def populate_data(self, products):
        self.connect()
        products.to_sql('product_recommendations', self.conn, flavor='mysql', if_exists='append', index=True)
        # related_products.to_sql('related_product_recommendations', self.conn, flavor='mysql', if_exists='replace',index=True)
        self.disconnect()
