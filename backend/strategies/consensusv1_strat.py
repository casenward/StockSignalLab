from backend.calculators.momentum import get_momentum_score
from backend.calculators.pb_ratio_score import get_pb_ratio_score
from backend.calculators.pe_ratio_score import get_pe_ratio_score
from backend.calculators.dividend_yield_score import get_dividend_yield_score
from backend.calculators.yahoo_consensus_score import get_yahoo_consensus_score


def calculate_consensus_score_v1(stock_obj) -> float:
    """
    Calculate consensus score for a stock using version 1 strategy.
    
    Weights:
    - Yahoo consensus: 40%
    - Momentum: 25%
    - P/B ratio: 10%
    - P/E ratio: 15%
    - Dividend yield: 10%
    """
    
    yahoo_score = get_yahoo_consensus_score(stock_obj.symbol) * 0.4    # 40% weight
    momentum_score = get_momentum_score(stock_obj) * 0.25              # 25% weight
    pb_score = get_pb_ratio_score(stock_obj) * 0.1                     # 10% weight
    pe_score = get_pe_ratio_score(stock_obj) * 0.15                    # 15% weight
    dividend_score = get_dividend_yield_score(stock_obj) * 0.1         # 10% weight
    
    total_score = yahoo_score + momentum_score + pb_score + pe_score + dividend_score
    return total_score
