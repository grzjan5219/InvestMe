from api import *
import datetime

today = datetime.date.today()
delta = datetime.timedelta(days=1)
yesterday = today - delta

def to_percentage(crp):
    prices = []
    x = getCrypto(crp, yesterday, today)
    for keys, values in x["Open"].items():
        prices.append(round(values,2))

    percentage = (prices[1] - prices[0]) / prices[0] * 100

    return round(percentage, 2)