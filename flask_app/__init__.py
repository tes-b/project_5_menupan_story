from flask import Flask, render_template
import requests
from modules.dbModule import Database
from modules.visualiser import Visualiser
from modules.db_id import dbId
import pandas as pd


# import time
import json

app = Flask(__name__)

# 인덱스
@app.route('/',methods=['GET'])
def index():
    dbid = dbId()
    mapapi_id = dbid.get_mapapiId()
    return render_template("index.html",mapapi_id=mapapi_id),200

# 대시보드
@app.route('/dashboard/<kw>',methods=['GET'])
def dashboard(kw):
    # start = time.time()
    # 지역 분류
    kw = eval(kw)
    sido = kw['sido']
    sigu = kw['sigu']
    sigu2 = kw['sigu2']
    dongmyun = kw['dongmyun']
    kw = " ".join([sido, sigu, sigu2, dongmyun])
    print(sido, sigu, sigu2, dongmyun, kw)

    # 데이터베이스 초기화
    database = Database()
    dbid = dbId()
    mapapi_id = dbid.get_mapapiId()
    
    #===============================================================
    # 업체수
    query_total = f"""
    SELECT COUNT(*) AS total FROM restaurant 
    WHERE sido = '{sido}' AND sigu = '{sigu}' AND dongmyun = '{dongmyun}'
    """

    res_total = database.execute_one(query_total)
    print("RESULT_TOTAL : ",res_total)

    #===============================================================
    # 업종
    query_cat_ratio = f"""
    SELECT category, COUNT(category) AS cnt 
    FROM restaurant
    WHERE sido = '{sido}' AND sigu = '{sigu}' AND dongmyun = '{dongmyun}'
    GROUP BY category
    ORDER BY cnt DESC
    ;
    """

    res_cat_ratio = database.execute_all(query_cat_ratio)
    print("RESULT_CATEGORY : ",res_cat_ratio)

    #===============================================================
    # 주변지역분류
    query_area = f"""
    SELECT area, COUNT(area) AS cnt 
    FROM restaurant
    WHERE sido = '{sido}' AND sigu = '{sigu}' AND dongmyun = '{dongmyun}'
    GROUP BY area
    ORDER BY cnt DESC
    ;
    """
    
    res_area = database.execute_all(query_area)
    res_area.pop() # 기타 항목 제거

    #===============================================================
    # 가구당 인원수 분포
    dm = dongmyun[:-1]
    if dm[-1] in ["1","2","3","4","5","6","7","8","9"]:
        dm = dm[:-1]
        if dm[-1] == "제":
            dm = dm[:-1]
    # SELECT sido, sigu, dongmyun, total, 1p, 2p, 3p, 4p, 5p_over
    query_hh = f"""
    SELECT total, 1p, 2p, 3p, 4p, 5p_over
    FROM household
    WHERE sido = '{sido}' AND dongmyun LIKE '{dm}%%'
    ;
    """
    res_hh = database.execute_all(query_hh)

    print("RESULT_HOUSEHOLD : ",res_hh)

    #===============================================================
    # 고령인구 
    query_senior = f"""
    SELECT total, over65_total
    FROM senior
    WHERE sido = '{sido}' AND dongmyun LIKE '{dm}%%'
    ;
    """

    res_sn = database.execute_all(query_senior)

    print("RESULT_SENIOR : ", res_sn)

    #===============================================================
    #지역 경계
    query_code = f"""
    SELECT code
    FROM codes
    WHERE sido = '{sido}' AND dongmyun LIKE '{dm}%%'
    ;
    """
    res_code = database.execute_one(query_code)

    if res_code:
        service_url = dbid.get_service_url()
        geocode = res_code["code"]
        key = dbid.get_vworld_key()
        url_geo = f"http://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADEMD_INFO&key={key}&domain={service_url}&attrFilter=emdCd:=:{geocode}"

        with requests.get(url_geo) as page:
            try:
                page.raise_for_status()
            except requests.exceptions.HTTPError as Err:
                print(Err)
            else:
                res_geo = json.loads(page.content)
                if res_geo["response"]["status"] != "OK":
                    print(res_geo["response"])
                coord = res_geo["response"]["result"]["featureCollection"]["features"][0]["geometry"]["coordinates"][0][0]
                # print(coord)
    else:
        res_code = None
    # print("RESULT : ", res_code)
    
    
    # 데이터베이스 닫기
    database.close()
   

    # 차트 생성
    visualiser = Visualiser()
    visualiser.pie_cat_ratio(res_cat_ratio,"업종비율")
    visualiser.table_cat_cnt(res_cat_ratio)
    visualiser.pie_household(res_hh,"가구원수 비율")
    visualiser.table_senior(res_sn)
    visualiser.table_area(res_area)

    # end = time.time()
    # print("python 수행시간 : " + str(end-start))


    return render_template("dashboard.html",
        kw=kw,
        mapapi_id=mapapi_id,
        res_total=res_total,
        # res_cat_ratio=res_cat_ratio,
        # res_hh=res_hh,
        # res_sn=res_sn,
        # res_area=res_area,
        # res_geo=res_geo,
        coord=coord,
    ),200

# 지역검색
@app.route('/search/<kw>',methods=['GET'])
def search(kw):
    # 데이터베이스 초기화
    database = Database()
    
    # 검색
    try:
        query_search_region=f"""
        SELECT DISTINCT sido, sigu, sigu2, dongmyun
        FROM codes
        WHERE dongmyun IS NOT NULL
        AND (
        sido LIKE '%%{kw}%%' 
        OR sigu LIKE '%%{kw}%%'
        OR sigu2 LIKE '%%{kw}%%'
        OR dongmyun LIKE '%%{kw}%%'
        )
        ;
        """
        res_region = database.execute_all(query_search_region)
        database.close()
    except:
        database.close()

    print(res_region)
    for v in res_region:
        if v["sigu"] == None:
            v["sigu"] = ""
        if v["sigu2"] == None:
            v["sigu2"] = ""
    
    dbid = dbId()
    mapapi_id = dbid.get_mapapiId()

    return render_template('search.html', 
        kw=kw, 
        mapapi_id=mapapi_id,
        res_region=res_region
    ),200

@app.route('/info/',methods=['GET'])
def info():
    return render_template('info.html', 
    ),200

@app.route('/contact/',methods=['GET'])
def contact():
    return render_template('contact.html', 
    ),200

if __name__ == '__main__':
    
    dbid = dbId()
    port=dbid.get_service_port()
    app.run(debug=False, host="0.0.0.0", port=port)
    # app.run(debug=True, host="0.0.0.0", port=port)