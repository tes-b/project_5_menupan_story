import pymysql
import pymysql.cursors
from modules.db_id import dbId

TABLE_RESTAURANTS = "restaurants"

class Database:
    def __init__(self):
        dbid = dbId();

        self.con = pymysql.connect(
            host=dbid.get_host(),
            user=dbid.get_user(),
            password=dbid.get_password(),
            db=dbid.get_dbName(),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
            )
        if isinstance(self.con, pymysql.connections.Connection):
            print("db connected")
            self.cur = self.con.cursor()
            if isinstance(self.cur, pymysql.cursors.Cursor):
                print("db initiation")

    def close(self):
        self.cur.close()
        self.con.close()
        print("db closed")
        

    def execute(self, query, args={}):
        self.cur.execute(query, args)  
 
    def execute_one(self, query, args={}):
        self.cur.execute(query, args)
        row = self.cur.fetchone()
        return row
 
    def execute_all(self, query, args={}):
        self.cur.execute(query, args)
        row = self.cur.fetchall()
        return row
 
    def commit(self):
        self.con.commit()
