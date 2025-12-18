from backend.calculators.score_calculator import calculate_score


def signal_calculator(ticker: str) -> float:
    from backend.stock import Stock
    
    stock = Stock(ticker)
    stock.set_symbol(ticker)
    stock.set_currentPrice()
    score = calculate_score(stock)
    if score >= 75:
        return 1
    elif score <= 25:
        return -1       
    else:
        return 0
    