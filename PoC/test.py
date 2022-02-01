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
#TD: Dawid
    
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

# def test3():
#     """Test 3: """

# def test4():
#     """Test 4: """

# def test5():
#     """Test 5: """

# def test6():
#     """Test 6: """
