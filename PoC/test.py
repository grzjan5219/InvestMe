import os
import pytest
import pandas as pd
from tensorboard import errors

from createFrontData import *
from api import *

def test1():
    """Test 1: Testing the output of new predict function """
    x = predict()
    if x == "Up trend" or "Flat trend" or "Down trend":
        assert True
#TD: Kuba
    
def test2():
    """Test 2: Testing price getting of crypto """
    y = getCrypto('BTC-USD', tydzien, now, "1d")
    keys_to_remove = ["High", "Low", "Close", "Adj Close", "Volume", "Date"]
    for key in keys_to_remove:
        y.pop(key)
    y = y.head(1).values.tolist()
    if y == float:
        assert True
#TD: Dawid

def test3():
     """Test 3: Testing out, the crypto release definition - Piotrek """
     x = to_percentage("BTC-USD")
     if (len(str(x)) == 5):
         assert True

def test4():
    """Test 2: Testing currency dictionary length - Bartek"""
    x = addToList(currency= "USD")
    if len(x[0].keys()) == 5:
       assert True

# def test5():
#     """Test 5: """

# def test6():
#     """Test 6: """
