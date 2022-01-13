from flask import Flask, render_template
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

def getCrypto(crp, data_start, data_end):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end)
    x = crphistory.to_dict()
    return x["Open"]

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
