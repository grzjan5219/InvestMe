from api import *
import datetime

today = datetime.date.today()


def get(crp, currency):
    x = getCrypto(crp, today, today)
    for keys, values in x["Open"].items():
        pricee = values

    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    c = RealTimeCurrencyConverter(url)

    return round(c.convert("USD", currency, pricee), 2)
