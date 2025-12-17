from backend.services.score_calculator import calculate_score
from backend.stock import Stock


def signal_calculator(ticker: str) -> float:
    stock = Stock(ticker)
    stock.set_symbol(ticker)
    stock.set_currentPrice()
    score = calculate_score(stock)  
    return 1
    if score >= 75:
        return 1
    elif score <= 25:
        return -1       
    else:
        return 0
    