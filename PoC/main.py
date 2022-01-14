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

def getCrypto(crp, data_start, data_end):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end)
    x = crphistory.to_dict()
    return x

def exchange(crp, data_start, data_end, currency):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    x = getCrypto(crp, data_start, data_end)
    keys_to_remove = ["Adj Close", "Volume"]
    for key in keys_to_remove:
        x.pop(key)
    format = "%Y-%m-%d"
    start = datetime.datetime.strptime(data_start, format)
    end = datetime.datetime.strptime(data_end, format)
    delta = datetime.timedelta(days=1)
    days = end - start
    

    start -= delta

    lista_calosc = []
    
     
    for i in range(days.days):
        lst = []
        lst.append(str(start.date()))
        lst.append(crp)
        for key in x:
            for date, price in x[key].items():
                if str(date)[:10] == str(start.date()):
                    lst.append(converter.convert('USD', f'{currency}', price))    
        lista_calosc.append(lst)
        start += delta
                           
    return lista_calosc #ZWRACA LISTE ZAGNIEŻDZONĄ W FORMACIE [DATA, CRYPTO, OPEN, HIGH, LOW, CLOSE]

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
