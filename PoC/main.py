from flask import Flask, render_template
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
from currency_converter import CurrencyConverter
from pandas._libs.tslibs.timestamps import Timestamp
import csv
import datetime
import requests

global crphistory


app = Flask(__name__)

now = str(datetime.datetime.now())[:10] # Zapisuje aktualną datę jako string (YYYY-MM-DD)

def getGraph(currency, crypto, time):
    if (time == "5y"):
        delta = datetime.timedelta(days=365) * 5
    elif (time == "1y"):
        delta = datetime.timedelta(days=365)
    elif (time == "6m"):
        delta = datetime.timedelta(days=182)
    elif (time == "7d"):
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
    font_color = "#EEE4E4",
    font_family = "Poppins",
    )

    fig.update_xaxes(color="#EEE4E4", gridcolor="#443838")
    fig.update_yaxes(color="#EEE4E4", gridcolor="#443838")
    return fig


class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
          amount = amount / self.currencies[from_currency] 
  
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount


yf.pdr_override()
pd.set_option("display.max_rows", None, "display.max_columns", None)


def getCrypto(crp, data_start, data_end):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end)
    return crphistory

def exchange(crp, data_start, data_end, currency):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    df = getCrypto(crp, data_start, data_end)
    keys_to_remove = ["Adj Close", "Volume"]
    for key in keys_to_remove:
        df.pop(key)
    format = "%Y-%m-%d"
    start = datetime.datetime.strptime(data_start, format)
    end = datetime.datetime.strptime(data_end, format)
    delta = datetime.timedelta(days=1)
    days = end - start
    
    start -= delta

    lista_calosc = {"Date" : [], "Open" : [], "High" : [], "Low" : [], "Close" : []}
    data = start
    for i in range(days.days):  
        lista_calosc["Date"].append(str(data)[:10])
        lista_calosc["Open"].append(converter.convert("USD", f'{currency}', df["Open"][i]))
        lista_calosc["High"].append(converter.convert("USD", f'{currency}', df["High"][i]))
        lista_calosc["Low"].append(converter.convert("USD", f'{currency}', df["Low"][i]))
        lista_calosc["Close"].append(converter.convert("USD", f'{currency}', df["Close"][i]))
        data += delta
    return lista_calosc 


def get(crypto, currency):
    data = yf.download(tickers=f'{crypto}', period='1d', interval='1d')
    b = list(data.Open)
    pricee = round(b[0], 1)
    c = CurrencyConverter()

    return round(c.convert(pricee, 'USD', currency), 1)



def to_percentage(crypto):
    data = yf.download(tickers=f'{crypto}', period='2d', interval='1d')
    a = data.Open
    prices = list(a)

    for a, b in zip(prices[::1], prices[1::1]):
        percentage = 100 * (b - a) / a
    return round(percentage, 2)



@ app.route('/')
def home():
    return render_template("home.html" )


@ app.route('/<currency>/<crypto>/<time>')
def home1(currency, crypto, time):
    # get graph
    fig = getGraph(currency, crypto, time)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # get currency price
    currentPrice = get(crypto, currency)
    # # get currency Procentage
    currentProcentage = to_percentage(crypto)

    cryptos = [
        {
            'name': 'ETH-USD',
            'price': get('ETH-USD', currency),
            'img': "{{url_for('static', filename='img/ETH-USD')}",
            'percentage': float(to_percentage('ETH-USD'))

        },
        {
            'name': 'BTC-USD',
            'price': get('BTC-USD', currency),
            'img': "{{url_for('static', filename='img/BTC-USD')}",
            'percentage': float(to_percentage('BTC-USD'))


        },
    ]

    return render_template("crypto.html", currentPrice=currentPrice, cryptos=cryptos, crypto=crypto, currentProcentage=currentProcentage, graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
