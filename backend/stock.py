# Base class for a stock
# Casen Ward

from backend.calculators import signal_calculator
import backend.apis.finnhub as finnhub
from backend.strategies import consensusv1_strat
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
        
    def set_signal(self):
        self.signal = signal_calculator.signal_calculator(self.symbol)

    def set_symbol(self, symbol):
        self.symbol = symbol.upper() 

    def set_name(self):
        ticker = yahoo.Ticker(self.symbol)
        self.name = ticker.info.get("longName", "Unknown Company")

    def set_currentPrice(self):
        self.current_price = finnhub.get_quote(self.symbol)["c"] # Current price is in the "c" field of the quote response
    
    def set_score(self):
        self.score = consensusv1_strat.calculate_consensus_score_v1(self)
        
    def set_consensus(self):
        self.set_score()
        self.consensus = final_rating(self.score)

        
    