from numpy import double
import backend.apis.finnhub as finnhub
import backend.apis.yahoo as yahoo
import time
import pandas as pd


def calculate_score(stock_obj) -> float:
    yahoo_score = yahoo.getYahoo_consensus(stock_obj.symbol)[1] * 0.4    #40% weight
    momentum_score = get_momentum_score(stock_obj) * 0.25   #25% weight
    pb_score = get_pb_ratio_score(stock_obj) * 0.1      #10% weight
    pe_score = get_pe_ratio_score(stock_obj) * 0.15      #15% weight
    dividend_score = get_dividend_yield_score(stock_obj) * 0.1          #10% weight
    total_score = yahoo_score + momentum_score + pb_score + pe_score + dividend_score   # Sum weighted scores
    return total_score                                       
  
import time

def get_momentum_score(stock_obj: "Stock") -> float:

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



def get_pb_ratio_score(stock_obj) -> float:
    current_price = stock_obj.current_price     # Ensure current price is set
    if current_price is None:
        stock_obj.set_currentPrice()
        current_price = stock_obj.current_price
    metrics = finnhub.get_metrics(stock_obj.symbol)["metric"]
    bvps = metrics.get("bookValuePerShareAnnual")
    if bvps is None or bvps == 0:
        return 50  # Neutral score if no data or invalid book value
    pb_ratio = current_price / bvps
    if pb_ratio < 1:
        return 100
    elif pb_ratio < 2:
        return 80
    elif pb_ratio < 3:                    # Scoring can be adjusted based on testing and analysis
        return 60
    elif pb_ratio < 4:
        return 40
    elif pb_ratio < 5:
        return 20
    else:
        return 0

    


def get_pe_ratio_score(stock_obj) -> float:
    metrics = finnhub.get_metrics(stock_obj.symbol)["metric"]
    pe_ratio = metrics.get("peBasicExclExtraTTM")
    if pe_ratio is None or pe_ratio <= 0:
        return 50  # Neutral score if no data or invalid PE ratio
    if pe_ratio < 10:
        return 100
    elif pe_ratio < 15:
        return 80
    elif pe_ratio < 20:                    # Scoring can be adjusted based on testing and analysis
        return 60
    elif pe_ratio < 25:
        return 40
    elif pe_ratio < 30:
        return 20
    else:
        return 0

def get_dividend_yield_score(stock_obj) -> float:
    metrics = finnhub.get_metrics(stock_obj.symbol)["metric"]
    dividend_yield = metrics.get("dividendYield")
    if dividend_yield is None or dividend_yield < 0:
        return 50  # Neutral score if no data or invalid dividend yield
    if dividend_yield > 5:
        return 100
    elif dividend_yield > 4:
        return 80
    elif dividend_yield > 3:
        return 60
    elif dividend_yield > 2:
        return 40
    elif dividend_yield > 1:
        return 20
    else:
        return 0

if __name__ == "__main__":
    from backend.stock import Stock
    test_stock = Stock("SMCI")
    test_stock.set_currentPrice()
    test_stock.set_score()
    print(f"Stock: {test_stock.symbol}, Current Price: {test_stock.current_price}, Score: {test_stock.score}")
