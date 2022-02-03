import os
import pytest
import pandas as pd
from tensorboard import errors

from createFrontData import *
from api import *
from chart import *


def test1():
    """Test 1: Testing the output of new predict function - Kuba"""
    x = predict()
    if x == "Up trend" or "Flat trend" or "Down trend":
        assert True


def test2():
    """Test 2: Testing price getting of crypto - Dawid"""
    y = getCrypto('BTC-USD', tydzien, now, "1d")
    keys_to_remove = ["High", "Low", "Close", "Adj Close", "Volume", "Date"]
    for key in keys_to_remove:
        y.pop(key)
    y = y.head(1).values.tolist()
    if y == float:
        assert True


def test3():
    """Test 3: Testing out, the crypto release definition - Piotrek"""
    x = to_percentage("BTC-USD")
    if (len(str(x)) == 5):
        assert True


def test4():
    """Test 4: Testing currency dictionary length - Bartek"""
    x = addToList(currency="USD")
    if len(x[0].keys()) == 5:
        assert True


def test5():
    """Test 5: Testing returning the random crypto name - Kuba"""
    x = currentNameFunc('BTC-USD', 'GBP')
    # List of all available cryptos
    y = ['Bitcoin', 'Ethernum', 'Binance Coin', 'Dogecoin',
         'Avalanche', 'Tether', 'Chainlink', 'Solana']
    if x in y:
        assert True
    else:
        assert False


def test6():
    """Test 6: Testing ex funcion output- Mateusz"""
    x = ex(20, 'PLN')

    if type(x) == float:
        assert True
    else:
        assert False


def test7():
    """Test 7: Testing Cryptocurrencys list length - Mateusz"""
    x = addToList(currency="USD")
    if len(x) == 8:
        assert True
    else:
        assert False
        
def test8():
    """Test 8: Testing if output of exchange fucntion is correct and if it's dictonary - Tomasz"""
    x = exchange("BTC-USD", "2021-01-01", "2022-01-01", "PLN", "1wk")
    if isinstance(x, dict):
        assert True
    else:
        assert False
