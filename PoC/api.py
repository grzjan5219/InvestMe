import yfinance as yf
import pandas as pd
import requests
import datetime
from pandas_datareader import data as pdr


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


def getCrypto(crp, data_start, data_end):
    crphistory = pdr.get_data_yahoo(crp, start=data_start, end=data_end)

    return crphistory


def exchange(crp, data_start, data_end, currency, interval=1):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    df = getCrypto(crp, data_start, data_end)
    keys_to_remove = ["Adj Close", "Volume"]
    for key in keys_to_remove:
        df.pop(key)
    format = "%Y-%m-%d"
    start = datetime.datetime.strptime(data_start, format)
    end = datetime.datetime.strptime(data_end, format)
    delta = datetime.timedelta(days=1)
    days = end - start

    start -= delta

    lista_calosc = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}
    data = start
    if int(interval) > int(days.days):
        interval = 1
    for i in range(1, days.days, int(interval)):
        lista_calosc["Date"].append(str(data)[:10])
        lista_calosc["Open"].append(converter.convert(
            "USD", f'{currency}', df["Open"][i]))
        lista_calosc["High"].append(converter.convert(
            "USD", f'{currency}', df["High"][i]))
        lista_calosc["Low"].append(converter.convert(
            "USD", f'{currency}', df["Low"][i]))
        lista_calosc["Close"].append(converter.convert(
            "USD", f'{currency}', df["Close"][i]))
        data += delta
    trend = 0
    for i in range(1, 7):
        if lista_calosc["Open"][-i] > lista_calosc["Open"][-i-1]:
            trend = trend + 1
        elif lista_calosc["Open"][-i] == lista_calosc["Open"][-i-1]:
            trend = trend + 0
        else:
            trend = trend - 1
    print(trend)
    if trend >= 2:
        lista_calosc["Trend"] = "Up trend"
    elif trend < 2 and trend > -2:
        lista_calosc["Trend"] = "Flat trend"
    else:
        lista_calosc["Trend"] = "Down trend"


    return lista_calosc
