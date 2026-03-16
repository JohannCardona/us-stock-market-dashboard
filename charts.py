import pandas as pd
import plotly.graph_objects as go

_MA_COLORS: dict[int, str] = {
    20: "#f5de0b",   # yellow
    40: "#f92116",   # red
    100: "#06d440",  # green
    200: "#a855f7",  # purple
}

_DARK_BG = "#0e1117"
_GRID_COLOR = "#1f2937"


def make_candlestick_chart(
    df: pd.DataFrame, ticker: str, ma_windows: list[int], show_bb: bool = False, interval: str = "1d"
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=ticker,
            increasing_line_color="#26a641",
            decreasing_line_color="#e05252",
            increasing_fillcolor="#26a641",
            decreasing_fillcolor="#e05252",
        )
    )
