import pymysql
import pymysql.cursors

TABLE_RESTAURANTS = "restaurants"

class Database:
    def __init__(self):
        host = 'localhost'
        user = 'testid'
        password = 'mysql1234'
        db = 'menupan_main'

        self.con = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
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
