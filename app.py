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

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📈 Stock Dashboard")
    st.markdown("---")

    ticker = st.text_input("Ticker Symbol", value="SPY", max_chars=10).upper().strip()

    interval_label = st.radio("Interval", ["Hour", "Day", "Week", "Month"], horizontal=True, index=1)
    interval = {"Hour": "1h", "Day": "1d", "Week": "1wk", "Month": "1mo"}[interval_label]

    today = date.today()
    default_start = today - timedelta(days=365)
    start_date = st.date_input("Start Date", value=default_start, max_value=today)
    end_date = st.date_input("End Date", value=today, max_value=today)

    if interval == "1h" and (today - start_date).days > 729:
        st.warning("Hourly data is limited to the last 730 days. Start date has been clamped.")
        start_date = today - timedelta(days=729)

    st.markdown("---")
    st.subheader("Indicators")
    st.subheader("Moving Averages")
    show_ma20 = st.checkbox("MA 20", value=True)
    show_ma40 = st.checkbox("MA 40", value=True)
    show_ma100 = st.checkbox("MA 100", value=True)
    show_ma200 = st.checkbox("MA 200", value=True)

    st.markdown("---")
    st.caption("Data provided by Yahoo Finance via yfinance.")

# ── Validation ────────────────────────────────────────────────────────────────
if not ticker:
    st.warning("Enter a ticker symbol in the sidebar.")
    st.stop()

if start_date >= end_date:
    st.error("Start date must be before end date.")
    st.stop()

# ── Data ──────────────────────────────────────────────────────────────────────
ma_windows = [w for w, show in [(20, show_ma20), (40, show_ma40), (100, show_ma100), (200, show_ma200)] if show]

with st.spinner(f"Fetching data for {ticker}…"):
    df = fetch_stock_data(ticker, str(start_date), str(end_date), interval)
    info = fetch_stock_info(ticker)

if df.empty:
    st.error(
        f"No data found for **{ticker}**. "
        "Check the ticker symbol (e.g. AAPL, TSLA, BTC-USD) and date range."
    )
    st.stop()

df = add_moving_averages(df, ma_windows)
if show_bb:
    df = add_bollinger_bands(df)
