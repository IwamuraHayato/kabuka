import requests
# BeautifulSoupの機能をインポート
from bs4 import BeautifulSoup
import streamlit as st # フロントエンドを扱うstreamlitの機能をインポート

st.title('Streamlit Hello World　テスト')

#アクセス先をREQUEST_URLを代入
REQUEST_URL = 'https://travel.rakuten.co.jp/yado/okinawa/nahashi.html' 

#リクエストしたデータをresに代入
res = requests.get(REQUEST_URL) 

# resの文字データがISO-8859-1なので、utf-8に変換して文字化けを防止します。
res.encoding = 'utf-8' 

# BeautifulSoup(解析したいデータ,解析する方法)を指定し、解析したデータをsoupに代入します。
soup = BeautifulSoup(res.text,"html.parser") 

# すべてのsectionタグを取得します。
hotel_section_from_html = soup.select('section') 

# hotel_section_from_htmlからsctionを抽出して残しておく、hotel_sectionとして空の配列を用意しておきます。
hotel_section = []
for hs in hotel_section_from_html:
    a = hs.select_one('p.area')
    if (a != None):
        hotel_section.append(hs) # aに情報がある時に実行したいので、条件はNoneではないというa != Noneになります。


# ホテル名を格納する空配列を用意します。
hotelName = [] 
# ホテルの料金を格納する空配列を用意します。
hotelMinCharge = [] 
# ホテル評価を格納する空配列を用意します。
reviewAverage = [] 
# ホテル住所を格納する空配列を用意します。
hotel_locate = [] 


# hotel_sectionからsectionを1つずつ取り出してhsに代入して実行します。
for hs in hotel_section:
     #ホテル名をhs1に代入
    hs1 = hs.select_one('h1 a').text
    if (hs.select_one('p.htlPrice span') != None):
        # 値段をhs2に代入
        hs2 = hs.select_one('p.htlPrice span').text.replace("円〜","").replace(",","") 
    else:
        # 値段が記入されていない場合があるので、わかりやすく-1にしておきましょう。
        hs2 = -1 

    # 評価をhs3に代入
    hs3 = hs.select_one('p.cstmrEvl strong').text 
    # 住所をhs4に代入
    hs4 = hs.select_one('p.htlAccess').text.replace("\n","").replace(" ","").replace("[地図を見る]","").replace("　","") 

    #抽出したホテル名をhotelNameに追加
    hotelName.append(hs1) 
    #抽出したホテルの料金をhotelMinChargeに追加
    hotelMinCharge.append(hs2) 
    #抽出したホテルの評価をreviewAverageに追加
    reviewAverage.append(hs3) 
    #抽出したホテル住所をhotel_locateに追加
    hotel_locate.append(hs4) 

# pandasのデータフレームに使うデータを定義します。
data_list = {
    "hotelName" : hotelName,
    "hotelMinCharge" : hotelMinCharge,
    "reviewAverage" : reviewAverage,
    "hotel_locate" : hotel_locate,
}

import pandas as pd
df = pd.DataFrame(data_list)
# drop_duplicates()で重複したデータを削除してくれます。
# drop_duplicates(inplace=True)とすることで、処理したデータを出力だけでなく、出力したデータを元のdfに代入して変更してくれます。
df.drop_duplicates(inplace=True)
# 列の認識番号であるindexが列の順番と一致していないので、reset_indexで番号を振り直します。
# reset_index(drop=True,inplace=True)とすることで、元のindexを削除して新たに生成したindexを作成し、元のデータを更新してくれます。
df.reset_index(drop=True,inplace=True)

import numpy as np # 数列を扱う機能をインポート

# foliumの機能をインポートします
import folium 
# 数列を得意とするライブラリnumpyをインポートする
import numpy as np
# グラフにプロットする機能をインポートし、pltの省略形として呼べるようにする
import matplotlib.pyplot as plt

# 数字に変換したホテル料金を追加するための空配列
x = [] 
# 数字に変換したホテル評価を追加するための空配列
y = [] 

for i in range(0 ,len(df)):
    # ホテル料金を数字の型に変換
    a1 = int(df["hotelMinCharge"][i]) 
    # ホテル評価を数字の型に変換
    a2 = float(df["reviewAverage"][i]) 

    # -1として入力した欠損したホテル料金データを条件で追加処理しない事で、排除します。
    if (a1 > 0):
        # xに数字に変換したホテル料金を追加
        x.append(a1) 
        # yに数字に変換したホテル評価を追加
        y.append(a2) 

# 表の描画します。
st.dataframe(df.head(n=36))
# データフレームのチャートの描画します。
st.line_chart(df)
