import pymysql
# import pandas as pd
# from sqlalchemy import create_engine

TABLE_RESTAURANTS = "restaurants"

class Database:
    def __init__(self):
        host = 'localhost'
        user = 'testid'
        db = 'menupan_main'
        self.con = pymysql.connect(host=host,user=user,db=db,charset='utf8')
        self.cur = self.con.cursor()
        print(type(self.con))
        print(type(self.cur))
        # if isinstance(self.connection,pymysql.connection):
        #     print("db connected")
        #     self.cursor = self.connection.cursor()
        # if isinstance(self.cursor,pymysql):
        #     print("db initiation")

    def close(self):
        self.cur.close()
        self.con.close()
        

