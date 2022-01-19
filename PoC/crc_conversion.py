import yfinance as yf
from currency_converter import CurrencyConverter

def get(crypto, currency):
    data = yf.download(tickers=f'{crypto}', period='1d', interval='1d')
    b = list(data.Open)
    pricee = round(b[0], 1)
    c = CurrencyConverter()

    return round(c.convert(pricee, 'USD', currency), 1)