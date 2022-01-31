from flask import Flask, render_template
import plotly
import json

from api import *
from chart import *
from percent import *
from crc_conversion import *
from createFrontData import *
app = Flask(__name__)

cryptos = addToList("USD")


@ app.route('/')
def home():

    return render_template("home.html", cryptos=cryptos)


@ app.route('/<currency>/<crypto>/<time>/<interval>/')
def home1(currency, crypto, time, interval):
    # get graph
    fig = getGraph(currency, crypto, time, interval)
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

    prediction = predict(crypto, currency)

    # list with cryptocurrencies data to display
    cryptos = addToList(currency)

    x = getCrypto(crypto, '2022-01-01', today)
    result = x.to_html()

    return render_template("crypto.html", currentData=currentData, cryptos=cryptos, graphJSON=graphJSON, crypto=crypto, time=time, currency=currency, result=result, prediction=prediction, interval=interval)


if __name__ == '__main__':
    app.run(debug=True)
