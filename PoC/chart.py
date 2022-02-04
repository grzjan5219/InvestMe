import datetime
import plotly.graph_objects as go

from api import *

# Zapisuje aktualną datę jako string (YYYY-MM-DD)
now = str(datetime.datetime.now())[:10]

crypto_release = {
    "BTC-USD": "2014-09-30",
    "ETH-USD": "2017-11-10",
    "DGD-USD": "2017-11-18",
    "DOGE-USD": "2017-11-10",
    "SOL-USD": "2021-09-28",
    "USDT-USD": "2017-11-10",
    "AVAX-USD": "2020-09-21",
    "LINK-USD": "2017-11-06",
}


def getGraph(currency, crypto, time, interval):
    stopDelta = False
    if (time == "5y"):
        delta = datetime.timedelta(days=365) * 5
    elif (time == "1y"):
        delta = datetime.timedelta(days=365)
    elif (time == "6m"):
        delta = datetime.timedelta(days=182)
    elif (time == "1m"):
        delta = datetime.timedelta(days=30)
    elif (time == "7d"):
        delta = datetime.timedelta(days=7)
    elif (time == "max"):
        data_pocz = crypto_release[crypto]
        stopDelta = True
    if stopDelta == False:
        data_pocz = str(datetime.datetime.now() - delta)[:10]
    try:
        df = exchange(crypto, data_pocz, now, currency, interval)
    except IndexError as e:
        print(str(e))
        delta = datetime.timedelta(days=7)
        data_pocz = str(datetime.datetime.now() - delta)[:10]
        df = exchange(crypto, data_pocz, now, currency)
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    fig.update_layout(
        plot_bgcolor='#312929',
        paper_bgcolor="#312929",
        font_color="#EEE4E4",
        font_family="Poppins",
    )

    fig.update_xaxes(color="#EEE4E4", gridcolor="#443838")
    fig.update_yaxes(color="#EEE4E4", gridcolor="#443838")
    return fig, data_pocz
