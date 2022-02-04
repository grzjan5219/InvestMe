from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter
import yfinance as yf
from api import *
import datetime
today = datetime.date.today()


def currentNameFunc(crypto, currency):
    if crypto == 'ETH-USD':
        currentName = 'Ethereum'
    elif crypto == 'BTC-USD':
        currentName = 'Bitcoin'
    elif crypto == 'DGD-USD':
        currentName = 'DigixDAO Coin'
    elif crypto == 'DOGE-USD':
        currentName = 'Dogecoin'
    elif crypto == "USDT-USD":
        currentName = 'Tether'
    elif crypto == 'AVAX-USD':
        currentName = 'Avalanche'
    elif crypto == 'SOL-USD':
        currentName = 'Solana'
    elif crypto == 'LINK-USD':
        currentName = 'Chainlink'
    return currentName


def get():
    data = yf.download(tickers="BTC-USD ETH-USD DOGE-USD USDT-USD LINK-USD SOL-USD AVAX-USD DGD-USD", period='2d',
                       interval='1d')['Close']
    return data


d = get()


def ex(pricee, currency):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    c = RealTimeCurrencyConverter(url)

    return round(c.convert("USD", currency, float(pricee)), 2)


def to_percentage(crypto):
    crp_data = d[f'{crypto}'].to_dict()
    crp_list = list(crp_data.values())
    percentage = (crp_list[1] - crp_list[0]) / crp_list[0] * 100

    return round(percentage, 2)


def createDictCryptos(crypto, currency):
    crp_data = d[f'{crypto}'].to_dict()
    crp_list = list(crp_data.values())[1]
    x = to_percentage(crypto)
    result = {}
    result["name"] = crypto
    result["price"] = ex(crp_list, currency)
    result["img"] = "{{url_for('static', filename='img/{crypto}')}"
    result["symbol"] = CurrencySymbols.get_symbol(currency)
    result["percentage"] = x
    result["percentage_display"] = str(x)

    return result


def addToList(currency):
    cryptos = []
    cryptos.extend((createDictCryptos('BTC-USD', currency),
                   createDictCryptos('ETH-USD', currency),
                    createDictCryptos('DGD-USD', currency),
                    createDictCryptos('SOL-USD', currency),
                    createDictCryptos('AVAX-USD', currency),
                    createDictCryptos('LINK-USD', currency),
                    createDictCryptos('USDT-USD', currency),
                   createDictCryptos('DOGE-USD', currency)
                    ))
    return cryptos
