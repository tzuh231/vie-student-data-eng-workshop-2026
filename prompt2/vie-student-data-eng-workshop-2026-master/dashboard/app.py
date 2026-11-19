"""Research dashboard: candles at 1m-1h + 30-min Rolling Realized Volatility.
Run from repo root:  streamlit run dashboard/app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

DATA = Path(__file__).resolve().parents[1] / "data"
# Reads the 1-minute output of our Part 1 pipeline: data/clean/<TICKER>/<DATE>/bars_1min.csv
FILES = sorted(DATA.glob("clean/*/*/bars_1min.csv")) or sorted(DATA.glob("raw/*.csv"))  # fallback: raw
FREQS = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min", "1h": "1h"}
TZ = {"MC.PA": "Europe/Paris"}  # others: New York


@st.cache_data
def load() -> pd.DataFrame:
    df = pd.concat([pd.read_csv(f).drop(columns="Unnamed: 0", errors="ignore") for f in FILES], ignore_index=True)
    df["ticker"] = df["ticker"].str.strip().replace({"LVMH": "MC.PA"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="mixed")
    df["received_at"] = pd.to_datetime(df.get("received_at"), utc=True, format="mixed", errors="coerce")
    # latest correction wins, drop invalid rows
    df = df.sort_values("received_at", na_position="first").drop_duplicates(["ticker", "timestamp"], keep="last")
    df = df[(df["volume"] >= 0) & (df["low"] <= df["high"])]
    df["ts"] = [t.tz_convert(TZ.get(k, "America/New_York")).tz_localize(None)
                for t, k in zip(df["timestamp"], df["ticker"])]
    df["date"] = df["ts"].dt.date
    return df.sort_values("ts")


@st.cache_data
def day(ticker, date) -> pd.DataFrame:
    d = load().query("ticker == @ticker and date == @date").set_index("ts")
    r = np.log(d["close"] / d["close"].shift())                 # 1-min log returns, intraday only
    d["rv"] = 100 * np.sqrt((r**2).rolling(30, min_periods=30).sum())
    return d


st.set_page_config("Research Dashboard", layout="wide")
data = load()
a, b, c = st.columns([1, 1, 2])
ticker = a.selectbox("Ticker", sorted(data["ticker"].unique()))
date = b.selectbox("Date", sorted(data.loc[data.ticker == ticker, "date"].unique(), reverse=True))
freq = c.segmented_control("Frequency", list(FREQS), default="5m") or "5m"

d = day(ticker, date)
bars = d.resample(FREQS[freq], origin="start").agg(
    {"open": "first", "high": "max", "low": "min", "close": "last", "rv": "last"}).dropna(subset=["open"])

fig = make_subplots(rows=2, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.03)
fig.add_candlestick(x=bars.index, open=bars.open, high=bars.high, low=bars.low, close=bars.close,
                    increasing_line_color="#26a69a", decreasing_line_color="#ef5350", row=1, col=1)
fig.add_scatter(x=bars.index, y=bars.rv, line=dict(color="#5c6bc0", width=1.6), row=2, col=1)
fig.update_layout(height=650, showlegend=False, xaxis_rangeslider_visible=False,
                  margin=dict(l=0, r=0, t=10, b=0), template="plotly_white")
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="RV 30m, %", row=2, col=1)
st.plotly_chart(fig, width="stretch")
