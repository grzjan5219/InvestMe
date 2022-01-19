import yfinance as yf

def to_percentage(crypto):
    data = yf.download(tickers=f'{crypto}', period='2d', interval='1d')
    a = data.Open
    prices = list(a)

    for a, b in zip(prices[::1], prices[1::1]):
        percentage = 100 * (b - a) / a
    return round(percentage, 2)