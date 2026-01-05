from typing import List
from datetime import date, timedelta
import importlib
import yfinance as yf

from backend.backtesting.trade import Trade
from backend.backtesting.backtestResult import BacktestResult

##Constants - available strategies and time periods for backtesting
STRATEGIES = {
    "mock": "backend.strategies.mockStrategy.MockStrategy",
}

TIME_PERIODS = {
    "1mo": 30,
    "6mo": 180,
    "1y": 365,
    "5y": 1825
}


class BacktestEngine:
    def __init__(self, ticker: str, price_data: List[dict], strategy):
        self.ticker = ticker
        self.price_data = price_data
        self.strategy = strategy
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
            historical_data = self.price_data[: i + 1]
            signal = self.strategy.calculate_signal(historical_data)

            if not self.in_position:
                if self.previous_signal == 1:
                    self.entry_price = tomorrow["open"]
                    self.entry_date = tomorrow["date"]  ## IF not already bought and signal is buy, BUY
                    self.in_position = True
            else:
                if self.previous_signal == -1:
                    trade = Trade(
                        ticker=self.ticker,            ## IF in position and signal is sell, SELL
                        entry_price=self.entry_price,
                        exit_price=tomorrow["open"],
                        entry_date=self.entry_date,
                        exit_date=tomorrow["date"] 
                    )
                    self.trades.append(trade)
                    self.in_position = False         ## Record and reset entry info
                    self.entry_price = None
                    self.entry_date = None

            self.previous_signal = signal

        if self.in_position:
            last_day = self.price_data[-1]
            trade = Trade(
                ticker=self.ticker,
                entry_price=self.entry_price,
                exit_price=last_day["close"],   ## Close any open position at the end of the backtest
                entry_date=self.entry_date,
                exit_date=last_day["date"]
            )
            self.trades.append(trade)

        return BacktestResult(
            ticker=self.ticker,
            start_date=self.price_data[0]["date"],
            end_date=self.price_data[-1]["date"],                
            trades=self.trades,
            price_data=self.price_data
        )


if __name__ == "__main__":
    
    ## User Input Section
    print("Available strategies:", ", ".join(STRATEGIES.keys()))
    strategy_name = input("Enter strategy name: ").lower()
    if strategy_name not in STRATEGIES:
        raise ValueError(f"Invalid strategy: {strategy_name}")

    print("Available time periods:", ", ".join(TIME_PERIODS.keys()))
    time_period = input("Enter time period: ").lower()
    if time_period not in TIME_PERIODS:
        raise ValueError(f"Invalid time period: {time_period}")

    ticker = input("Enter ticker: ").upper()

    module_path, class_name = STRATEGIES[strategy_name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    StrategyClass = getattr(module, class_name)           ##Imports path from dictionary
    strategy = StrategyClass()

    end_date = date.today()
    start_date = end_date - timedelta(days=TIME_PERIODS[time_period])

    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if df.empty:
        raise ValueError("No price data returned")

    price_data = []
    for idx, row in df.iterrows():
        price_data.append({
            "date": idx.date(),
            "open": float(row["Open"]),
            "close": float(row["Close"]),       ## Collecting price data into list of dicts
            "symbol": ticker
        })

    engine = BacktestEngine(
        ticker=ticker,
        price_data=price_data,
        strategy=strategy
    )

    result = engine.run()

    for trade in result.trades:
        print(trade.to_dict())

    print(result.to_dict())
