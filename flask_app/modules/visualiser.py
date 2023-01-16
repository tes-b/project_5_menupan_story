import plotly
import plotly.graph_objects as go
import pandas as pd
from modules.dbModule import Database


class Visualiser:
    def __init__(self):
        pass

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
        print("pie_household", data)
        
        file_name = "./flask_app/static/charts/pie_household.html"

        if data:
            print("pie_household : data")
            df = pd.DataFrame.from_dict(data)
            df = df.sum(axis=0)
            df = df[["total","5p_over","4p","3p","2p","1p"]]

            print("pie_household : ", df)
            dict_col = {
            "total":"전체",
            "1p":"1인",
            "2p":"2인",
            "3p":"3인",
            "4p":"4인",
            "5p_over":"5인이상"
            }
            df = df.rename(dict_col)

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
            fig.write_html(file_name)            
            
        else: # data None
            print("NO DATA")    
            html_text = "<p>데이터가 없습니다.</p>"
            html_file = open(file_name,'w')
            html_file.write(html_text)
            html_file.close()
            # fig = go.Figure()

        print("pie_household_drawn")

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
        # return fig

    def table_cat_cnt(self,data=None, title=""):
        file_name = "./flask_app/static/charts/table_cat_cnt.html"
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
        fig.write_html(file_name)

    def table_senior(self,data=None, title=""):
        print("table_senior")
        file_name = "./flask_app/static/charts/table_senior.html"

        if data:
            df = pd.DataFrame.from_dict(data)
            df = df.sum(axis=0)
            ratio = df["over65_total"] / df["total"] * 100
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
            fig.write_html(file_name)

        else:
            print("NO DATA")
            html_text = "<p>데이터가 없습니다.</p>"
            html_file = open(file_name,'w')
            html_file.write(html_text)
            html_file.close()
            # fig = go.Figure()


        print("table_senior_drawn")

    def table_area(self,data=None, title=""):
        print("table_area")

        file_name = "./flask_app/static/charts/table_area.html"

        if data:
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
            fig.write_html(file_name)
        else:
            print("NO DATA")
            html_text = "<p>데이터가 없습니다.</p>"
            html_file = open(file_name,'w')
            html_file.write(html_text)
            html_file.close()
    
    def hbar_category_sales(self, data=None, title=""):
        df = pd.DataFrame(data=data,columns=['한식','양식']).set_index("장르")
        df = df.sort_values(by="인기도",ascending=True)
        fig = go.Figure(data=[go.Bar(
            x=df["인기도"],
            y=df.index,
            orientation='h')])
        fig.update_layout(title_text=title)
        fig.write_html("./flask_app/static/charts/hbarchart.html")