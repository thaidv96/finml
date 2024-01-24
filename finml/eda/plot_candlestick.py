import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_candlestick(df: pd.DataFrame, symbol:str, time = 'bucket', open = 'open', high = 'high', low = 'low', close = 'close', volume = 'volume'):
    # Create figure with secondary y-axis
    candlesticks = go.Candlestick(
        x=df[time],
        open=df[open],
        high=df[high],
        low=df[low],
        close=df[close],
        showlegend=False,

    )

    volume_bars = go.Bar(
        x=df[time],
        y=df[volume],
        showlegend=False,
        marker={
            "color": "rgba(128,128,128,0.5)",
        }
    )

    fig = go.Figure(candlesticks)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(candlesticks, secondary_y=True)
    fig.add_trace(volume_bars, secondary_y=False)
    fig.update_layout(
        title=f"Candlestick Chart of {symbol}",
        height=800,
        # Hide Plotly scrolling minimap below the price chart
        # xaxis={"rangeslider": {"visible": False}},
    )
    fig.update_yaxes(title="Price (VND)", secondary_y=True, showgrid=True)
    fig.update_yaxes(title="Volume", secondary_y=False, showgrid=False)
    fig.show()
