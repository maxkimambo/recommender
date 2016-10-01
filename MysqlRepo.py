import mysql.connector

class MysqlRepo:

    def connect(self):
        conn = mysql.connector.connect(user='root', password='alexandra', host='mysql', database='recommender')
        cursor = conn.cursor()
        return cursor

    def save(self, data):

        query = ''

        try:
            cursor = self.connect()

            cursor.execute(query)
            cursor.commit()

        except TypeError as err:
            print(err)


