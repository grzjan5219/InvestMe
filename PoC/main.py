from flask import Flask, render_template
import plotly
import json
import pandas as pd

from api import *
from chart import *
from percent import *
from crc_conversion import *
from createFrontData import *
import datetime
app = Flask(__name__)

cryptos = addToList("USD")


@ app.route('/')
def home():

    return render_template("home.html", cryptos=cryptos)


@ app.route('/<currency>/<crypto>/<time>/<interval>/')
def home1(currency, crypto, time, interval):
    # get graph
    fig = getGraph(currency, crypto, time, interval)[0]
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # list with data abaout current cryptocurrency to display
    c = d[f'{crypto}'].to_dict()
    a = list(c.values())[1]
    currentData = [
        {
            'currentSymbol': CurrencySymbols.get_symbol(currency),
            'currentName': currentNameFunc(crypto, currency),
            'currentPrice':  ex(a, currency),
            'currentProcentage': to_percentage(crypto)
        }
    ]


    # list with cryptocurrencies data to display
    cryptos = addToList(currency)
    tydzien = str(datetime.datetime.now() - datetime.timedelta(days=14))[:10]
    data_pocz = getGraph(currency, crypto, time, interval)[1]
    x = getCrypto(crypto, data_pocz,  today, interval) 
    # trend = exchange(crypto, data_start=tydzien, data_end=now, currency=currency)["Trend"]
    result = x.to_html()
    return render_template("crypto.html", currentData=currentData, cryptos=cryptos, graphJSON=graphJSON, crypto=crypto, time=time, currency=currency, result=result, prediction=None, interval=interval)


if __name__ == '__main__':
    app.run(debug=True)
