from flask import Flask, render_template
from datetime import datetime, date, timedelta
from pandas._libs.tslibs.timestamps import Timestamp
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd

app = Flask(__name__)
cg = CoinGeckoAPI()

yf.pdr_override()
pd.set_option("display.max_rows", None, "display.max_columns", None)

def getCrypto(crp, data_start, data_end):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end)
    x = crphistory.to_dict()
    return x["Open"]

@app.route('/')
def home():
    return render_template("home.html", zmienna="Hello world")
