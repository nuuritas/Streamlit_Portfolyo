import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_echarts import st_echarts

gunluk_ozet = pd.read_parquet("gunluk_ozet.parquet")
haftalık_ozet = pd.read_parquet("haftalık_ozet.parquet")
port_all = pd.read_parquet("port_all.parquet")
if datetime.today().hour < 18:
    today_str = (datetime.today() - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
else:
    today_str = (datetime.today()).strftime("%d-%m-%Y")
hisse_gunluk = pd.read_parquet("hisse_gunluk.parquet")

st.title("haftalık Bazda Sonuçlar")
st.header("Burada haftalık kazanç ve portfolyo değişimi yer alır.")

# gunluk_ozet
# Extracting data
haftalık_dates = haftalık_ozet["date"].dt.strftime("%Y-%m-%d").tolist()
haftalık_dpy_values = [round(val, 2) for val in haftalık_ozet["d_p_y"].tolist()]

# Formatting series data for colors
haftalık_formatted_values = []
for val in haftalık_dpy_values:
    if val >= 0:
        haftalık_formatted_values.append(
            {"value": val, "itemStyle": {"color": "#00a900"}}
        )  # green for positive
    else:
        haftalık_formatted_values.append(
            {"value": val, "itemStyle": {"color": "#a90000"}}
        )  # red for negative

# Updating options
options_bar_haftalık = {
    "tooltip": {
        "trigger": "item",
        "axisPointer": {"type": "shadow"},
    },
    "title": {
        "text": "Günlük Getiri",
        "left": "center",
        "textStyle": {"color": "#ffffff"},
    },
    "xAxis": {
        "type": "category",
        "data": haftalık_dates,
        "axisLabel": {
            "interval": len(haftalık_dates)
            // 6  # This will approximately display 6 dates on the x-axis
        },
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": haftalık_formatted_values,
            "type": "bar",
        }
    ],
}

st_echarts(
    options=options_bar_haftalık,
    height="400px",
)

haftalık_t_v_values = haftalık_ozet["t_v"].tolist()
haftalık_a_inv_values = haftalık_ozet["a_inv"].tolist()

options_portfoy = {
    "title": {"text": "Portföy ve Yatırım", "textStyle": {"color": "#ffffff"}},
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
    },
    "legend": {
        "data": ["Portfolyo", "Yatırım"],
        "textStyle": {"color": "#ffffff "},
    },
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": [
        {
            "type": "category",
            "boundaryGap": False,
            "data": haftalık_dates,
        }
    ],
    "yAxis": [{"type": "value"}],
    "series": [
        {
            "name": "Portfolyo",
            "type": "line",
            "stack": "总量",
            "areaStyle": {},
            "emphasis": {"focus": "series"},
            "data": haftalık_t_v_values,
        },
        {
            "name": "Yatırım",
            "type": "line",
            "stack": "总量",
            "areaStyle": {},
            "emphasis": {"focus": "series"},
            "data": haftalık_a_inv_values,
        },
    ],
}

st_echarts(options=options_portfoy, height="400px")