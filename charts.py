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

    for w in ma_windows:
        col = f"MA_{w}"
        if col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    mode="lines",
                    name=f"MA {w}",
                    line=dict(color=_MA_COLORS.get(w, "#ffffff"), width=1.5),
                )
            )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=_DARK_BG,
        plot_bgcolor=_DARK_BG,
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
        title=dict(text=f"{ticker} — Price", font=dict(size=16)),
    )
    rangebreaks = [dict(bounds=["sat", "mon"])] if interval == "1h" else []
    fig.update_xaxes(showgrid=True, gridcolor=_GRID_COLOR, rangebreaks=rangebreaks)
    fig.update_yaxes(showgrid=True, gridcolor=_GRID_COLOR, tickprefix="$")

    return fig

