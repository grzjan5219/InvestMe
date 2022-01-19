from flask import Flask, render_template
import plotly
import json

from api import *
from chart import *
from percent import *
from crc_conversion import *

app = Flask(__name__)

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
