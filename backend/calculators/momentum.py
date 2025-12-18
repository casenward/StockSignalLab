from __future__ import annotations
from typing import TYPE_CHECKING

import time
import pandas as pd
import backend.apis.yahoo as yahoo

if TYPE_CHECKING:
    from backend.stock import Stock


def get_momentum_score(stock_obj: Stock) -> float:

    current_price = stock_obj.current_price         # Ensure current price is set
    if current_price is None:   
        stock_obj.set_currentPrice()              
        current_price = stock_obj.current_price             
    one_year_ago = int(time.time()) - 365 * 24 * 60 * 60      # Timestamp for one year ago
    today = int(time.time())                        # Current timestamp

    candles = yahoo.get_candles(stock_obj.symbol, "1d", one_year_ago, today)
    if candles is None or candles.empty:             # No data available
        return 50

    one_year_ago_price = candles["Close"].iloc[0]      # Closing price one year ago
    if one_year_ago_price == 0 or pd.isna(one_year_ago_price):
        return 50    # Avoid division by zero or NaN

    momentum = ((current_price - one_year_ago_price) / one_year_ago_price) * 100         # Percentage change over the year

    if momentum >= 20:
        return 100
    elif momentum >= 10:
        return 80
    elif momentum >= 0:
        return 60          # Scoring can be adjusted based on testing and analysis
    elif momentum >= -10:
        return 40
    elif momentum >= -20:
        return 20
    else:
        return 0
