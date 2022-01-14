from flask import Flask, render_template
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from cgitb import reset
from logging import FileHandler
from xml.etree.ElementTree import XML
from pandas._libs.tslibs.timestamps import Timestamp
import requests

app = Flask(__name__)

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

def getCrypto(crp, data_start, data_end, type):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end)
    x = crphistory.to_dict()
    return x[f"{type}"]

def exchange(crp, data_start, data_end, currency, type):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    x = getCrypto(crp, data_start, data_end, type)
    dates = []
    prices = []
    exchanged_prices = []
    for key, value in x.items():
        dates.append(key)
        prices.append(value)

    for _ in prices:
        exchanged_prices.append(converter.convert('USD', f'{currency}', _))

    result = dict(zip(dates, exchanged_prices))

    #filehandler = open("krypto.txt", "wt")
    #data = str(result)
    #filehandler.write(data)

    return result

def getGraph():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])])
    fig.update_layout(
    plot_bgcolor='#312929',
    paper_bgcolor="#312929",
    font_color = "#EEE4E4",
    font_family = "Poppins",
    )

    fig.update_xaxes(color="#EEE4E4", gridcolor="#443838")
    fig.update_yaxes(color="#EEE4E4", gridcolor="#443838")
    return fig

@app.route('/')
def home():

    fig = getGraph() 
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("home.html", graphJSON=graphJSON)

@app.route('/crypto')
def home1():
    return render_template("crypto.html")
