from flask import Flask, render_template
import plotly
import json

from api import *
from chart import *
from percent import *
from crc_conversion import *
from createFrontData import *
app = Flask(__name__)


@ app.route('/')
def home():
    return render_template("home.html")


@ app.route('/<currency>/<crypto>/<time>')
def home1(currency, crypto, time):
    # get graph
    fig = getGraph(currency, crypto, time)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # list with data abaout current cryptocurrency to display
    currentData = [
        {
            'currentSymbol': CurrencySymbols.get_symbol(currency),
            'currentName': currentNameFunc(crypto, currency),
            'currentPrice':  round(get(crypto, currency), 1),
            'currentProcentage': to_percentage(crypto)
        }
    ]

    # list with cryptocurrencies data to display
    cryptos = addToList(currency)

    return render_template("crypto.html", currentData=currentData, cryptos=cryptos, graphJSON=graphJSON, crypto=crypto, time=time, currency=currency)


if __name__ == '__main__':
    app.run(debug=True)
