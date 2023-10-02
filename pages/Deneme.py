import streamlit as st
from datetime import datetime

st.set_page_config(layout="centered")


wch_colour_font = (255, 255, 255)
fontsize = 24
lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'


def generate_sparkline(values, color="white"):
    """Generate an SVG sparkline from a list of values."""
    # Normalize values to fit within SVG viewBox
    max_val = max(values)
    min_val = min(values)

    height = 30
    width = 100

    normalized_values = [
        (val - min_val) / (max_val - min_val) * height for val in values
    ]
    path_data = "M 0," + str(height - normalized_values[0])  # Move to starting point

    # Create path data from normalized values
    for i, val in enumerate(normalized_values, start=1):
        path_data += f" L {i * (width / (len(values)-1))},{height - val}"

    # Check if the last value is above or below the start value to decide the color of the sparkline
    if normalized_values[-1] > normalized_values[0]:
        color = "green"
    else:
        color = "red"

    # Return SVG string
    return f"""
    <svg width="100%" height="100%" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
        <line x1="0" y1="{height - normalized_values[0]}" x2="100" y2="{height - normalized_values[0]}" stroke="white" stroke-dasharray="2,2" stroke-width="1"/>
        <path d="{path_data}" fill="none" stroke="{color}" stroke-width="1.5"/>
    </svg>
    """


values = [10, 12, 8, 13, 7, 10, 11, 14, 12, 15]
values2 = [20, 12, 8, 13, 7, 10, 11, 14, 12, 15]
sparkline_aapl = generate_sparkline(values)
sparkline_tesla = generate_sparkline(values2)


# HTML Structure for the stocks
def stock_html(stock_code, sparkline_svg, holding_value, daily_gain, gain_color):
    return f"""
    <link href="https://fonts.googleapis.com/css2?family=Rubik+Mono+One&display=swap" rel="stylesheet">
    <div style='display: flex; justify-content: space-between; align-items: center;
                background-color: transparent; font-family: "Rubik Mono One", cursive;
                color: rgb({wch_colour_font[0]}, {wch_colour_font[1]}, {wch_colour_font[2]}); 
                border-radius: 7px; padding: 12px; line-height: 25px; border: 1px solid white;'>
        <div style='flex: 1; text-align: left; font-size: {fontsize}px;'>{stock_code}</div>
        <div style='flex: 1;'>{sparkline_svg}</div>
        <div style='flex: 1; text-align: right;'>
            <span style='font-size: {fontsize}px; display: block;'>{holding_value}</span>
            <span style='font-size: 20px; color: {gain_color}; display: block;'>{daily_gain}</span>
        </div>
    </div>
    """


# Markdown for AAPL and TESLA
aapl_html = stock_html("AAPL", sparkline_aapl, "$1500", "+$25", "green")
tesla_html = stock_html("TESLA", sparkline_tesla, "$1400", "-$20", "red")


# Main Holdings Info Box
def main_holdings_html(
    total_value,
    days_gain,
    days_gain_perc,
    total_gain,
    total_gain_perc,
    days_gain_color,
    total_gain_color,
):
    current_date = datetime.now().strftime("%B %d, %Y")
    return f"""
    <link href="https://fonts.googleapis.com/css2?family=Rubik+Mono+One&display=swap" rel="stylesheet">
    <div style='background-color: transparent; color: white; border-radius: 7px; padding: 12px; line-height: 25px; border: 1px solid white; margin-bottom: 12px;font-family: "Rubik Mono One", cursive;'>
        <span style='font-size: 22px; display: block;'>BAKİYE</span>
        <span style='font-size: 28px; display: block;'>₺{total_value}</span>
        <br>
        <div style='display: flex; justify-content: space-between;'>
            <span style='font-size: 16px; display: block;'>Günlük Kazanç:</span>
            <span style='font-size: 20px; color: {days_gain_color}; display: block;'>${days_gain}({days_gain_perc})</span>
        </div>
        <div style='display: flex; justify-content: space-between;'>
            <span style='font-size: 16px; display: block;'>Toplam Kazanç:</span>
            <span style='font-size: 20px; color: {total_gain_color}; display: block;'>${total_gain}({total_gain_perc})</span>
        </div>
        <span style='font-size: 12px; display: block; color:lightgrey'>{current_date}</span>
    </div>
    """


# HTML for Main Holdings, AAPL, and TESLA
main_html = main_holdings_html("5000", "75", "2","-50", "-3", "green", "red")
aapl_html = stock_html("AAPL", sparkline_aapl, "$1500", "+$25", "green")
tesla_html = stock_html("TESLA", sparkline_tesla, "$1400", "-$20", "red")

st.markdown(lnk + main_html, unsafe_allow_html=True)

st.markdown(lnk + aapl_html, unsafe_allow_html=True)
st.markdown(lnk + tesla_html, unsafe_allow_html=True)
