import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data(ttl=3600)
def fetch_stock_data(ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=True, progress=False)
    if df.empty:
        return df
    # Flatten MultiIndex columns produced by newer yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


@st.cache_data(ttl=3600)
def fetch_stock_info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}


def add_moving_averages(df: pd.DataFrame, windows: list[int]) -> pd.DataFrame:
    df = df.copy()
    for w in windows:
        df[f"MA_{w}"] = df["Close"].rolling(w).mean()
    return df


def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    df = df.copy()
    rolling = df["Close"].rolling(window)
    df["BB_mid"] = rolling.mean()
    df["BB_upper"] = df["BB_mid"] + num_std * rolling.std()
    df["BB_lower"] = df["BB_mid"] - num_std * rolling.std()
    return df
