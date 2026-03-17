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

# ── Header ────────────────────────────────────────────────────────────────────
company_name: str = info.get("longName", ticker)
st.title(f"{company_name} ({ticker})")

# ── Metrics Row ───────────────────────────────────────────────────────────────
current_price: float = float(info.get("currentPrice") or df["Close"].iloc[-1])
prev_close: float = float(info.get("previousClose") or (df["Close"].iloc[-2] if len(df) > 1 else current_price))
day_change_pct: float = ((current_price - prev_close) / prev_close * 100) if prev_close else 0.0
week52_high: float = float(info.get("fiftyTwoWeekHigh") or df["High"].max())
week52_low: float = float(info.get("fiftyTwoWeekLow") or df["Low"].min())
market_cap: int | None = info.get("marketCap")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Current Price", f"${current_price:,.2f}")
col2.metric("Day Change", f"{day_change_pct:+.2f}%")
col3.metric("52-Week High", f"${week52_high:,.2f}")
col4.metric("52-Week Low", f"${week52_low:,.2f}")
col5.metric("Market Cap", f"${market_cap / 1e9:.2f}B" if market_cap else "N/A")

st.markdown("---")
