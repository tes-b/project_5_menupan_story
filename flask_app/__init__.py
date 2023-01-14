from flask import Flask, render_template
import requests
from modules.dbModule import Database
from modules.visualiser import Visualiser
import pandas as pd
# import time
import json

app = Flask(__name__)

# 인덱스
@app.route('/',methods=['GET'])
def index():
    return render_template("index.html"),200

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

    # 업체수
    query_total = f"""
    SELECT COUNT(*) AS total FROM restaurant 
    WHERE sido = '{sido}' AND sigu = '{sigu}' AND dongmyun = '{dongmyun}'
    """

    res_total = database.execute_one(query_total)
    # print(res_total)

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
    res_area.pop()
    # print(res_area)
    # non = 0
    # i = 0
    # for v in res_area:
    #     if v["area"] == None:
    #         non = v["cnt"]
    #         break
    #     i += 1
    # for v in res_area:
    #     if v["area"] == "기타":
    #         v["cnt"] += non
    #         break
    # del res_area[i]
    
    # print(res_area)

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

    df = pd.DataFrame.from_dict(res_hh)
    df = df.sum(axis=0)
    res_hh = df[["total","5p_over","4p","3p","2p","1p"]]


    # 고령인구 

    # SELECT sido, sigu, dongmyun, total, male, female, over65_total, over65_male, over65_female
    query_senior = f"""
    SELECT total, over65_total
    FROM senior
    WHERE sido = '{sido}' AND dongmyun LIKE '{dm}%%'
    ;
    """

    res_sn = database.execute_all(query_senior)
    
    df = pd.DataFrame.from_dict(res_sn)
    sn = df.sum(axis=0)


    #지역 경계
    query_code = f"""
    SELECT code
    FROM codes
    WHERE sido = '{sido}' AND dongmyun LIKE '{dm}%%'
    ;
    """
    res_code = database.execute_one(query_code)
    print(res_code)
    service_url = "127.0.0.1:5000"
    geocode = res_code["code"]
    url_geo = f"http://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADEMD_INFO&key=CE5EF6B0-B38B-30BE-946C-8F54B767BE7A&domain={service_url}&attrFilter=emdCd:=:{geocode}"

    with requests.get(url_geo) as page:
        try:
            page.raise_for_status()
        except requests.exceptions.HTTPError as Err:
            print(Err)
        else:
            res_geo = json.loads(page.content)
            coord = res_geo["response"]["result"]["featureCollection"]["features"][0]["geometry"]["coordinates"][0][0]
            # print(coord)
       
    
    print("got requet")
    # 데이터베이스 닫기
    database.close()
   

    # 차트 생성
    visualiser = Visualiser()
    visualiser.pie_cat_ratio(res_cat_ratio,"업종비율")
    visualiser.table_cat_cnt(res_cat_ratio)
    visualiser.pie_household(res_hh,"가구원수 비율")
    visualiser.table_senior(sn)
    visualiser.table_area(res_area)

    # end = time.time()
    # print("python 수행시간 : " + str(end-start))
    return render_template("dashboard.html",
        kw=kw,
        res_total=res_total,
        res_cat_ratio=res_cat_ratio,
        res_hh=res_hh,
        res_sn=sn,
        res_area=res_area,
        res_geo=res_geo,
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
    
    return render_template('search.html', 
        kw=kw, 
        res_region=res_region
    ),200
    

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, host='127.0.0.1',port='5000')
    # app.run(debug=True, host='0.0.0.0',port='5000')