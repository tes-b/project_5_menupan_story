from flask import Flask, render_template
import requests
import os
import sys
import urllib
from modules.dbModule import Database


app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    # db = Database()
    # query = """
    # SELECT * FROM restaurants 
    # WHERE dongmyun = '상도동';
    # """
    # result = db.executeAll(query)
    # db.close()

    return render_template("index.html"),200

@app.route('/dashboard/<kw>',methods=['GET'])
def dashboard(kw):
    database = Database()
    query_total = f"""
    SELECT COUNT(*) FROM restaurants 
    WHERE dongmyun = '{kw}'
    """
    res_total = database.execute_all(query_total)

    query_cat_ratio = f"""
    SELECT category, COUNT(category) AS cnt 
    FROM restaurants 
    WHERE dongmyun = '{kw}' 
    GROUP BY category;
    """

    res_cat_ratio = database.execute_all(query_cat_ratio)


    database.close()
    return render_template("dashboard.html",
    kw=kw,
    res_total=res_total,
    res_cat_ratio=res_cat_ratio,
    ),200


@app.route('/search/<kw>',methods=['GET'])
def search(kw):
    return render_template('dashboard.html'),200

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, host='127.0.0.1',port='5000')
    # app.run(debug=True, host='0.0.0.0',port='5000')