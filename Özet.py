import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide")

gunluk_ozet = pd.read_parquet("data/parquet/gunluk_ozet.parquet")
haftalık_ozet = pd.read_parquet("data/parquet/haftalık_ozet.parquet")
port_all = pd.read_parquet("data/parquet/port_all.parquet")

from datetime import datetime, timedelta
now = datetime.now()
if now.weekday() >= 5:  # 5: Saturday, 6: Sunday
    days_to_subtract = now.weekday() - 4
    today = now.date() - timedelta(days=days_to_subtract)
    today_str = (now - timedelta(days=days_to_subtract)).strftime("%d-%m-%Y")
else:
    if now.hour < 18:
        today = now.date() - timedelta(days=1)
        today_str = (now - timedelta(days=1)).strftime("%d-%m-%Y")
    else:
        today = now.date()
        today_str = now.strftime("%d-%m-%Y")

hisse_gunluk = pd.read_parquet("data/parquet/hisse_gunluk.parquet")

# st.dataframe(gunluk_ozet)
st.title(f"{datetime.today().strftime('%d-%m-%Y')} Özet")

toplam_buyukluk = port_all.query("date == @today").t_v.sum()
gunluk_net = gunluk_ozet.query("date == @today").d_p.values[0]
gunluk_yuzde = gunluk_ozet.query("date == @today").d_p_y.values[0]

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

son_gun = hisse_gunluk.query("date == @today").sort_values(
    by="t_v", ascending=True
)
son_gun.dropna(how="any", inplace=True)
data_list = [
    {"name": ticker, "value": round(value)}
    for ticker, value in son_gun[["ticker", "t_v"]].values
]

st.subheader(f"Portfolyo Büyüklüğü: {int(toplam_buyukluk)}₺")

options_pie_main = {
    "tooltip": {"trigger": "item", 
    "formatter": "{b} <br> {c}₺ (%{d})"
    },
    "series": [
        {
            "name": "Hisse",
            "type": "pie",
            "radius": ["30%","50%"],
            "center": ["50%", "40%"],
            "avoidLabelOverlap": "falses",
            "data": [],
            "label": {
                "color": "#ffffff",
                "fontSize": 14,
            },
            "emphasis": {
                "label": {
                    "show": "true",
                    "fontWeight": "bold",
                    "fontSize": 16,
                    "fontColor": "#ffffff"
                },
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                },
                "focus": "data",
            },
        }
    ],
}


# {
#     "type": "pie",
#     "id": "pie",
#     "radius": "30%",
#     "center": ["50%", "25%"],
#     "emphasis": {"focus": "data"},
#     "label": {"formatter": "{b}: {@2012} ({d}%)"},
#     "encode": {"itemName": "product", "value": "2012", "tooltip": "2012"},
# },
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

