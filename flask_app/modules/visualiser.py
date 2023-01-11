import plotly
import plotly.graph_objects as go
import pandas as pd
from modules.dbModule import Database


class Visualiser:
    def __init__(self):
        pass

    def pie(self, data=None, title=""):
        df = pd.DataFrame(data=data,columns=['장르','작품수']).set_index("장르")
        fig = go.Figure(data=[go.Pie(labels=df.index, values=df["작품수"], hole=.5, title=title)])
        fig.write_html("./flask_app/static/charts/piechart.html")

    def pie_cat_ratio(self,data=None, title=""):
        print("pie_cat_ratio")
        df = pd.DataFrame.from_dict(data=data)
        df = df.rename(columns={"category":"업종", "cnt":"점포수"}).set_index("업종")
        # df = df.sort_values(by="점포수",ascending=True)
        fig = go.Figure(data=[go.Pie(labels=df.index, 
                                    values=df["점포수"], 
                                    hole=.4, 
                                    title=title, 
                                    textinfo='label+percent', 
                                    textposition='inside',
                                    showlegend=False)])
        fig.update_layout(
            font=dict(size=15),
            margin=dict(t=20, b=20, l=20, r=20),
            )
        fig.write_html("./flask_app/static/charts/pie_cat_ratio.html")

    def pie_household(self,data=None, title=""):

        dict_col = {
        "total":"전체",
        "1p":"1인",
        "2p":"2인",
        "3p":"3인",
        "4p":"4인",
        "5p_over":"5인이상"
        }
        df = data.rename(dict_col)

        fig = go.Figure(data=[go.Pie(labels=df.index, 
                                    values=df.values, 
                                    hole=.4, 
                                    title=title, 
                                    textinfo='label+percent', 
                                    textposition='inside',
                                    rotation=90,
                                    sort=False,
                                    showlegend=False)])
        fig.update_layout(
            font=dict(size=15),
            margin=dict(t=20, b=20, l=20, r=20),
            )
        fig.write_html("./flask_app/static/charts/pie_household.html")
        return fig

    def hbar_cat_ratio(self, data=None, title=""):
        
        # df = pd.DataFrame(data=data,columns=['업종','점포수']).set_index("업종")
        df = pd.DataFrame.from_dict(data=data)
        df = df.rename(columns={"category":"업종", "cnt":"점포수"}).set_index("업종")
        df = df.sort_values(by="점포수",ascending=True)
        fig = go.Figure(data=[go.Bar(
            x=df["점포수"],
            y=df.index,
            orientation='h')])
        fig.update_layout(title_text=title)
        fig.write_html(f"./static/charts/cat_ratio.html")
        return fig

    def vbar(self, data=None, title=""):
        df = pd.DataFrame(data=data,columns=['장르','평균별점']).set_index("장르")
        fig = go.Figure(data=[go.Bar(
            x=df.index,
            y=df["평균별점"],
            orientation='v')])
        fig.update_layout(title_text=title)
        fig.update_yaxes(range=[9.0, 10])
        fig.write_html("./flask_app/static/charts/vbarchart.html")

    def table_cat_cnt(self,data=None, title=""):
        print("table_cat_cnt")
        cat,cnt = [],[]
        for v in data:
            cat.append(v["category"])
            cnt.append(v["cnt"])

        fig = go.Figure(data=[go.Table(
                header=dict(values=['<b>업종</b>', '<b>업체수</b>'], height=30, align='center'),
                cells=dict(values=[cat,cnt], height=30, align=['left', 'center']),
                columnwidth = [100,50]
                )])
        fig.update_layout(
            font=dict(size=15),
            margin=dict(t=10, b=10, l=20, r=20),
            )
        fig.write_html(f"./flask_app/static/charts/table_cat_cnt.html")

    def table_senior(self,data=None, title=""):

        print("table_senior")
        ratio = data["over65_total"] / data["total"] * 100
        ratio = ratio.round(2)
        ratio = str(ratio) + "%"
        title = "<b>고령 인구 비율</b><br>(65세 이상)"
        fig = go.Figure(data=[go.Table(
                header=dict(values=[title], height=30, align='center',font_size=30),
                cells=dict(values=[ratio], height=60, align='center', font_size=50),
                )])

        fig.update_layout(
            font=dict(size=15),
            margin=dict(t=10, b=10, l=20, r=20),
            )
        fig.write_html(f"./flask_app/static/charts/table_senior.html")

    def table_area(self,data=None, title=""):

        print("table_cat_cnt")
        area,cnt = [],[]
        for v in data:
            area.append(v["area"])
            cnt.append(v["cnt"])

        fig = go.Figure(data=[go.Table(
                header=dict(values=['<b>주변지역</b>', '<b>업체수</b>'], height=30, align='center'),
                cells=dict(values=[area,cnt], height=30, align=['left', 'center']),
                columnwidth = [100,50]
                )])
        fig.update_layout(
            font=dict(size=15),
            margin=dict(t=10, b=10, l=20, r=20),
            )
        fig.write_html(f"./flask_app/static/charts/table_area.html")