from flask import Flask, render_template
from pycoingecko import CoinGeckoAPI
from datetime import datetime, date, timedelta

app = Flask(__name__)
cg = CoinGeckoAPI()

def crypto(crp="bitcoin", currency="usd", data="01-01-2015"):
    #funkcja przyjmuje wartości domyślne dla Bitcoina, dolarów i daty aktualnej
    result = {}
    cena = cg.get_coin_history_by_id(crp, data)
    result["Typ kryptowaluty"] = crp
    result["Cena"] = round(cena["market_data"]["current_price"][currency], 2)
    result["Data"] = data
    return result 

def getCrypto(crp, currency, data_pocz, data_kon):
    result = {}
    lista_dat = []
    date_format_original = "%Y-%m-%d"
    date_format_new = "%d-%m-%Y"
    numer_wiersza = 0
    delta = datetime.strptime(data_kon, date_format_original) - datetime.strptime(data_pocz, date_format_original)
    division_number = 30 # szacowana liczba wyników
    #liczy ile dni jest pomiędzy datą końcową a początkową
    for i in range(0, delta.days + 1, delta.days//division_number):
        data = datetime.strptime(data_pocz, date_format_original) + timedelta(days = i)
        lista_dat.append(data.strftime(date_format_new))
    for x in lista_dat:
        numer_wiersza = numer_wiersza + 1
        result[numer_wiersza] = (crypto(crp, currency, x))
    return result

@app.route('/')
def strona_glowna():
    pass
