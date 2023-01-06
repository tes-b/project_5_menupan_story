from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    return render_template("index.html"),200

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return render_template("dashboard.html"),200

@app.route('/search/<rg>', methods=['GET'])
def search(rg):
    

    # 클라이언트 ID / Secret
    client_id = "mxgcd10clr"
    client_secret = "m3YwoBpcyRrId5zOXQP0DLSZzAGdmdpSzHrrKvky"

    # 좌표 (경도, 위도)
    coords = "129.1133567,35.2982640"
    output = "json"
    orders = "=addr,admcode,roadaddr"
    endpoint = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?"
    url = f"{endpoint}coordsToaddr&coords={coords}&sourcecrs=epsg:4326&output={output}&orders={orders}"

    # 헤더
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }

    # 요청
    res = requests.get(url, headers=headers)
    res.json()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='127.0.0.1',port='5000')
    # app.run(debug=True, host='0.0.0.0',port='5000')