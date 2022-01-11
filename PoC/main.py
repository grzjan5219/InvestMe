from flask import Flask, render_template
from pycoingecko import CoinGeckoAPI
from datetime import datetime, date, timedelta

app = Flask(__name__)
cg = CoinGeckoAPI()

def crypto(crp, currency, data):
    #funkcja przyjmuje wartości domyślne dla Bitcoina, dolarów i daty aktualnej
    result = {}
    cena = cg.get_coin_history_by_id(crp, data)
    result["Typ kryptowaluty"] = crp
    result["Cena"] = round(cena["market_data"]["current_price"][currency], 2)
    result["Data"] = data
    return result 

def getCrypto(crp, currency, data_pocz, data_kon): #DATA MUSI BYĆ W FORMACIE (RRRR, MM, DD) BEZ ZER NP (2020, 5, 5)
    result = {}
    numer_wiersza = 1
    year, month, day = data_pocz #ZMIENIA TYP DANYCH NA INT
    year2, month2, day2 = data_kon
    start_date = date(year, month, day) #TWORZY DATE DO PĘTLI
    end_date = date(year2, month2, day2)
    delta = timedelta(days=1)
    while start_date <= end_date:
      datetimeobject = datetime.strptime(str(start_date), '%Y-%m-%d') #ZMIENIA FORMAT ODPOWIEDI DLA API
      new_format = datetimeobject.strftime('%d-%m-%Y') 
      result[numer_wiersza] = crypto(crp, currency, new_format)
      numer_wiersza += 1
      start_date += delta
    return result

@app.route('/')
def home():
    return render_template("home.html", zmienna="Hello world")
