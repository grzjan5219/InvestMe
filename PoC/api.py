import yfinance as yf
import pandas as pd
import requests
import datetime
from pandas_datareader import data as pdr

now = str(datetime.datetime.now())[:10] # Zapisuje aktualną datę jako string (YYYY-MM-DD)
tydzien = str(datetime.datetime.now() - datetime.timedelta(days=7))[:10]

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

def predict(crp="BTC-USD", data_start=tydzien, data_end=now):
    dane = getCrypto(crp, data_start, data_end, interval="1d")
    keys_to_remove = ["High", "Low", "Close", "Adj Close", "Volume", "Date"]
    trend = 0
    for key in keys_to_remove:
        dane.pop(key)
    dane = dane.values.tolist()
    for i in range(1, len(dane)):
        if dane[-i] > dane[-i-1]:
            trend = trend + 1
        elif dane[-i] == dane[-i-1]:
            trend = trend + 0
        else:
            trend = trend - 1
    if trend >= 1:
        return "Up trend"
    elif trend < 1 and trend > -1:
        return "Flat Trend"
    else:
        return "Down trend"