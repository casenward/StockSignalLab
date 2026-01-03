from typing import List
from datetime import date

from backend.backtesting.trade import Trade
from backend.backtesting.backtestResult import BacktestResult


class BacktestEngine:
    def __init__(self, ticker: str, price_data: List[dict], strategy):
        
        self.ticker = ticker
        self.price_data = price_data
        self.strategy = strategy

        # position state
        self.in_position = False
        self.entry_price = None
        self.entry_date = None

        self.trades: List[Trade] = []
        self.previous_signal = 0

    def run(self) -> BacktestResult:
        if len(self.price_data) < 2:
            raise ValueError("Not enough price data to run backtest")

        for i in range(len(self.price_data) - 1):
            tomorrow = self.price_data[i + 1]

            # --- SIGNAL PHASE (end of day t) ---
            historical_data = self.price_data[: i + 1]
            signal = self.strategy.calculate_signal(historical_data)

            # --- EXECUTION PHASE (day t+1) ---
            if not self.in_position:
                if self.previous_signal == 1:
                    self.entry_price = tomorrow["open"]
                    self.entry_date = tomorrow["date"]
                    self.in_position = True

            else:  # in_position == True
                if self.previous_signal == -1:
                    trade = Trade(
                        ticker=self.ticker,
                        entry_price=self.entry_price,
                        exit_price=tomorrow["open"],
                        entry_date=self.entry_date,
                        exit_date=tomorrow["date"]
                    )
                    self.trades.append(trade)

                    self.in_position = False
                    self.entry_price = None
                    self.entry_date = None

            self.previous_signal = signal

        # --- CLEANUP PHASE ---
        if self.in_position:
            last_day = self.price_data[-1]
            trade = Trade(
                ticker=self.ticker,
                entry_price=self.entry_price,
                exit_price=last_day["close"],
                entry_date=self.entry_date,
                exit_date=last_day["date"]
            )
            self.trades.append(trade)

        return BacktestResult(
            ticker=self.ticker,
            start_date=self.price_data[0]["date"],
            end_date=self.price_data[-1]["date"],
            trades=self.trades
        )
