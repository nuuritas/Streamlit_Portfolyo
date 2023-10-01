import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_echarts import st_echarts
st.set_page_config(layout="wide")

gunluk_ozet = pd.read_parquet("gunluk_ozet.parquet")
haftalık_ozet = pd.read_parquet("haftalık_ozet.parquet")
port_all = pd.read_parquet("port_all.parquet")

now = datetime.now()
if now.weekday() >= 5:  # 5: Saturday, 6: Sunday
    # If today is Saturday, subtract 1 day to get Friday's data
    # If today is Sunday, subtract 2 days to get Friday's data
    days_to_subtract = now.weekday() - 4
    today_str = (now - timedelta(days=days_to_subtract)).strftime("%d-%m-%Y")
else:
    # For weekdays, if the current time is before 18:00, use yesterday's date
    if now.hour < 18:
        today_str = (now - timedelta(days=1)).strftime("%d-%m-%Y")
    else:
        # If the current time is 18:00 or later, use today's date
        today_str = now.strftime("%d-%m-%Y")

hisse_gunluk = pd.read_parquet("hisse_gunluk.parquet")

# st.dataframe(gunluk_ozet)
st.title(f"{datetime.today().strftime('%d-%m-%Y')} Özet")

toplam_buyukluk = port_all.query("date == @today_str").t_v.sum()
gunluk_net = gunluk_ozet.query("date == @today_str").d_p.values[0]
gunluk_yuzde = gunluk_ozet.query("date == @today_str").d_p_y.values[0]

son_hafta = gunluk_ozet[-7:]
son_hafta.reset_index(drop=True, inplace=True)
haftalik_net = (
    son_hafta.iloc[-1]["t_v"] - son_hafta.iloc[0]["t_v"] - son_hafta["d_inv"].sum()
)
haftalik_yuzde = round(
    (1 - (son_hafta.iloc[-7]["t_v"] / son_hafta.iloc[-1]["t_v"])) * 100, 2
)

son_ay = gunluk_ozet[-30:]
son_ay.reset_index(drop=True, inplace=True)
aylik_net = son_ay.iloc[-1]["t_v"] - son_ay.iloc[0]["t_v"] - son_ay["d_inv"].sum()
aylik_yuzde = round(
    (1 - (son_ay.iloc[0]["t_v"] / (son_ay.iloc[-1]["t_v"] - son_ay["d_inv"].sum())))
    * 100,
    2,
)

son_gun = hisse_gunluk[hisse_gunluk["date"] == today_str].sort_values(
    by="t_v", ascending=True
)
son_gun.dropna(how="any", inplace=True)
data_list = [
    {"name": ticker, "value": round(value, 1)}
    for ticker, value in son_gun[["ticker", "t_v"]].values
]

st.subheader(f"Portfolyo Büyüklüğü: {int(toplam_buyukluk)}₺")

options_pie_main = {
    "title": {
        "text": "Portfolyo",
        "left": "center",
        "textStyle": {"color": "#ffffff"},
    },
    "tooltip": {"trigger": "item", 
    "formatter": "{b} <br/>{c}₺ (%{d})"},
    "series": [
        {
            "name": "Hisse",
            "type": "pie",
            "radius": "40%",
            "avoidLabelOverlap": "false",
            "data": [
                {"value": 1048, "name": "搜索引擎"},
                {"value": 735, "name": "直接访问"},
                {"value": 580, "name": "邮件营销"},
                {"value": 484, "name": "联盟广告"},
                {"value": 300, "name": "视频广告"},
            ],
            "label": {
                "color": "#ffffff",
                "fontSize": 16,
            },
            "emphasis": {
                "label": {
                    "show": "true",
                    "fontWeight": "bold",
                    "fontSize": 16,
                    "fontColor": "#ffffff"
                }
            },
        }
    ],
}
options_pie_main["series"][0]["data"] = data_list

st_echarts(
    options=options_pie_main,
    height="500px",
)

m1, m2, m3 = st.columns((3))

m1.metric(
    label="Günlük(%)",
    value=round(gunluk_yuzde, 2),
    delta=str(int(gunluk_net)) + "₺",
    delta_color="normal",
)
m2.metric(
    label="Haftalık(%)",
    value=round(haftalik_yuzde, 2),
    delta=str(int(haftalik_net)) + "₺",
    delta_color="normal",
)
m3.metric(
    label="Aylık(%)",
    value=round(gunluk_yuzde, 2),
    delta=str(int(aylik_net)) + "₺",
    delta_color="normal",
)

