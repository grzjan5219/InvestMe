from flask import Flask, render_template
import plotly
import json
import pandas as pd

from api import *
from chart import *
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
    data_pocz = getGraph(currency, crypto, time, interval)[1]
    x = exchange(crypto, data_pocz, today, currency, interval="1d")
    print(x)
    x = pd.DataFrame.from_dict(x)
    x = x.iloc[::-1]
    trend = predict(crypto)
    result = x.to_html(index=False)
    return render_template("crypto.html", currentData=currentData, cryptos=cryptos, graphJSON=graphJSON, crypto=crypto, time=time, currency=currency, result=result, prediction=trend, interval=interval)


if __name__ == '__main__':
    app.run(debug=True)
