"""
Consensus Strategy Version 1

This module computes a trading signal (+1, 0, -1) for a stock
based on a weighted consensus of financial factors.

This file represents BOTH:
- the scoring model
- the signal decision logic

Execution timing is handled by the backtest engine.
"""

from backend.calculators.momentum import get_momentum_score
from backend.calculators.pb_ratio_score import get_pb_ratio_score
from backend.calculators.pe_ratio_score import get_pe_ratio_score
from backend.calculators.dividend_yield_score import get_dividend_yield_score
from backend.calculators.yahoo_consensus_score import get_yahoo_consensus_score


# -----------------------------
# Configuration (V1)
# -----------------------------

BUY_THRESHOLD = 70
SELL_THRESHOLD = 30

YAHOO_WEIGHT = 0.40
MOMENTUM_WEIGHT = 0.25
PB_WEIGHT = 0.10
PE_WEIGHT = 0.15
DIVIDEND_WEIGHT = 0.10


class ConsensusV1Strategy:
    def calculate_signal(self, historical_data) -> int:
        """
        Calculate trading signal for the current day.

        Parameters
        ----------
        historical_data : list[dict]
            Historical snapshots up to *today*.
            The last element represents the current day.

        Returns
        -------
        int
            1  -> Buy
            0  -> Hold
           -1  -> Sell
        """

        # Use most recent snapshot (today)
        stock_obj = historical_data[-1]["stock_obj"]

        # ---- SCORE CALCULATION ----
        yahoo_score = get_yahoo_consensus_score(stock_obj.symbol)
        momentum_score = get_momentum_score(stock_obj)
        pb_score = get_pb_ratio_score(stock_obj)
        pe_score = get_pe_ratio_score(stock_obj)
        dividend_score = get_dividend_yield_score(stock_obj)

        score = (
            yahoo_score * YAHOO_WEIGHT +
            momentum_score * MOMENTUM_WEIGHT +
            pb_score * PB_WEIGHT +
            pe_score * PE_WEIGHT +
            dividend_score * DIVIDEND_WEIGHT
        )

        # ---- SIGNAL DECISION ----
        if score >= BUY_THRESHOLD:
            return 1
        elif score <= SELL_THRESHOLD:
            return -1
        else:
            return 0
