from backend.strategies.consensusv1_strat import calculate_consensus_score_v1


def signal_calculator(ticker: str) -> float:
    from backend.stock import Stock
    
    stock = Stock(ticker)
    stock.set_symbol(ticker)
    stock.set_currentPrice()
    score = calculate_consensus_score_v1(stock)
    if score >= 75:
        return 1
    elif score <= 25:
        return -1       
    else:
        return 0
    