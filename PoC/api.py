import yfinance as yf
import pandas as pd
import requests
import datetime
from pandas_datareader import data as pdr

global trend


class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        # first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

        # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


yf.pdr_override()
pd.set_option("display.max_rows", None, "display.max_columns", None)


def getCrypto(crp, data_start, data_end, interval):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end, interval=interval)
    crphistory = crphistory.reset_index()
    for i in ['Open', 'High', 'Close', 'Low']:
        crphistory[i] = crphistory[i].astype('float64')
    return crphistory


def exchange(crp, data_start, data_end, currency, interval="1mo"):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    df = getCrypto(crp, data_start, data_end, interval)
    keys_to_remove = ["Adj Close", "Volume"]
    for key in keys_to_remove:
        df.pop(key)
    
    lista_calosc = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}

    for i in range(len(df["Open"])): 
        lista_calosc["Date"].append(str(df["Date"][i])[:10])
        lista_calosc["Open"].append(converter.convert("USD", f'{currency}', df["Open"][i]))
        lista_calosc["High"].append(converter.convert("USD", f'{currency}', df["High"][i]))
        lista_calosc["Low"].append(converter.convert("USD", f'{currency}', df["Low"][i]))
        lista_calosc["Close"].append(converter.convert("USD", f'{currency}', df["Close"][i]))

    return lista_calosc
