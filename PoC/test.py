import os
import pytest
from tensorboard import errors

from createFrontData import *


def test1():
    """Test 1: Testowanie trendu kryptowalut """
    x = predict('BTC-USD', 'PLN')
    if x == "Up trend" or "Flat trend" or "Down trend":
        assert True
    
# def test2():
#     """Test 2: """

# def test3():
#     """Test 3: """

# def test4():
#     """Test 4: """

# def test5():
#     """Test 5: """

# def test6():
#     """Test 6: """