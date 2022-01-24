from percent import *
from crc_conversion import *
from currency_symbols import CurrencySymbols


# create current name
def currentNameFunc(crypto, currency):
    if crypto == 'ETH-USD':
        currentName = 'Ethereum'
    elif crypto == 'BTC-USD':
        currentName = 'Bitcoin'
    # elif crypto == 'BNB-USD':
    #     currentName = 'Binance Coin'
    elif crypto == 'DOGE-USD':
        currentName = 'Dogecoin'
    elif crypto == "USDT-USD":
        currentName = 'Tether USD'
    elif crypto == 'SOL1-USD':
        currentName = 'Solana USD'
    return currentName


# creat dictionaries for cryptocurrencies list
def createDictCryptos(crypto, currency):
    result = {}
    result["name"] = crypto
    result["price"] = get(crypto, currency)
    result["img"] = "{{url_for('static', filename='img/{crypto}')}"
    result["percentage"] = to_percentage(crypto)
    result["symbol"] = CurrencySymbols.get_symbol(currency)

    return result


def addToList(currency):
    cryptos = []
    cryptos.extend((createDictCryptos('BTC-USD', currency),
                    createDictCryptos('ETH-USD', currency),
                    # createDictCryptos('BNB-USD', currency),
                    createDictCryptos('DOGE-USD', currency),
                    createDictCryptos('USDT-USD', currency),
                    createDictCryptos('SOL1-USD', currency)))
    return cryptos
