from flask import Flask, render_template
import requests
import os
import sys
import urllib

app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    return render_template("index.html"),200

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return render_template("dashboard.html"),200


@app.route('/search/<kw>', methods=['GET'])
def search(kw):
    

    # 클라이언트 ID / Secret
    client_id = "rmn6_jUkJLItPG1eAU4z"
    client_secret = "VsqpuaDsIl"

    # 좌표 (경도, 위도)
    encText = urllib.parse.quote("검색할 단어")
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과

    # output = "json"
    # url = f"https://openapi.naver.com/v1/search/local.{output}?query=%EC%A3%BC%EC%8B%9D&display=10&start=1&sort=random"


    # 헤더
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    # 요청
    res = requests.get(url, headers=headers)
    res.json()


    # 네이버 검색 API 예제 - 블로그 검색

    client_id = "rmn6_jUkJLItPG1eAU4z"
    client_secret = "VsqpuaDsIl"
    encText = urllib.parse.quote(kw)
    endpoint = "&display=10&start=1&sort=random"

    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + endpoint # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='127.0.0.1',port='5000')
    # app.run(debug=True, host='0.0.0.0',port='5000')