import streamlit as st
import pandas as pd
from datetime import date, timedelta

from data import fetch_stock_data, fetch_stock_info, add_moving_averages
from charts import make_candlestick_chart, make_volume_chart

st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """,
    unsafe_allow_html=True,
)
