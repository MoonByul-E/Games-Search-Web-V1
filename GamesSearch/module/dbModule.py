import pymysql
from ..config import MYSQL

class Database():
    def __init__(self):
        self.db = pymysql.connect(host=MYSQL["MYSQL_HOST"], port=MYSQL["MYSQL_PORT"], user=MYSQL["MYSQL_USER"], password=MYSQL["MYSQL_PASSWORD"], db=MYSQL["MYSQL_DB"])
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()