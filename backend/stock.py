# Base class for a stock
# Casen Ward

import backend.apis.finnhub as finnhub
import yfinance as yahoo


def final_rating(score: float) -> str:
    if score >= 80:
        return "Strong Buy"
    elif score >= 65:
        return "Buy"
    elif score >= 45:
        return "Hold"
    elif score >= 25:
        return "Sell"
    else:
        return "Strong Sell"


class Stock:
    def __init__(self, symbol):
        self.signal = None
        self.symbol = None
        self.name = None
        self.current_price = None
        self.score = None
        self.consensus = None

    def set_symbol(self, symbol):
        self.symbol = symbol.upper() 

    def set_name(self):
        ticker = yahoo.Ticker(self.symbol)
        self.name = ticker.info.get("longName", "Unknown Company")

    def set_currentPrice(self):
        self.current_price = finnhub.get_quote(self.symbol)["c"] # Current price is in the "c" field of the quote response

        
    