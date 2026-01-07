from typing import List
from datetime import date, timedelta
import importlib
import yfinance as yf

# -------------------------------------------------
# Configuration
# -------------------------------------------------

STRATEGIES = {
    "mock": "backend.strategies.mockStrategy.MockStrategy",
}

TIME_PERIODS = {
    "1mo": 30,
    "6mo": 180,
    "1y": 365,
    "5y": 1825
}

LARGE_CAP_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "JNJ", "PG", "KO", "V", "BRK-B"
]

# -------------------------------------------------
# Result Container (simple + explicit)
# -------------------------------------------------

class BacktestResult:
    def __init__(
        self,
        ticker: str,
        start_date: date,
        end_date: date,
        strategy_return_pct: float,
        buy_and_hold_return_pct: float,
        max_drawdown_pct: float,
        trades_count: int,
        time_in_market_pct: float,
    ):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.strategy_return_pct = strategy_return_pct
        self.buy_and_hold_return_pct = buy_and_hold_return_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.trades_count = trades_count
        self.time_in_market_pct = time_in_market_pct


# -------------------------------------------------
# Backtest Engine (Single-Ticker, Deterministic)
# -------------------------------------------------

class BacktestEngine:
    def __init__(self, ticker: str, price_data: List[dict], strategy):
        self.ticker = ticker
        self.price_data = price_data
        self.strategy = strategy

    def run(self) -> BacktestResult:
        if len(self.price_data) < 2:
            raise ValueError("Not enough price data")

        # ---- Reset state (critical) ----
        in_position = False
        entry_price = None
        equity = 1.0
        peak_equity = 1.0

        trades = 0
        days_in_market = 0

        # ---- Main simulation loop ----
        for i in range(len(self.price_data) - 1):
            today = self.price_data[i]
            tomorrow = self.price_data[i + 1]

            historical_data = self.price_data[: i + 1]
            signal = self.strategy.calculate_signal(historical_data)

            if not in_position and signal == 1:
                entry_price = tomorrow["open"]
                in_position = True
                trades += 1

            elif in_position:
                days_in_market += 1

                if signal == -1:
                    exit_price = tomorrow["open"]
                    equity *= exit_price / entry_price
                    in_position = False
                    entry_price = None

                    peak_equity = max(peak_equity, equity)

        # ---- Force close at end ----
        if in_position:
            last_close = self.price_data[-1]["close"]
            equity *= last_close / entry_price
            peak_equity = max(peak_equity, equity)

        # ---- Metrics ----
        strategy_return = equity - 1

        first_open = self.price_data[0]["open"]
        last_close = self.price_data[-1]["close"]
        buy_and_hold_return = (last_close / first_open) - 1

        max_drawdown = (peak_equity - equity) / peak_equity if peak_equity > 0 else 0

        time_in_market_pct = days_in_market / len(self.price_data)

        # ---- Sanity guards ----
        assert 0 <= time_in_market_pct <= 1
        assert 0 <= max_drawdown <= 1

        return BacktestResult(
            ticker=self.ticker,
            start_date=self.price_data[0]["date"],
            end_date=self.price_data[-1]["date"],
            strategy_return_pct=strategy_return,
            buy_and_hold_return_pct=buy_and_hold_return,
            max_drawdown_pct=max_drawdown,
            trades_count=trades,
            time_in_market_pct=time_in_market_pct
        )

    # -------------------------------------------------
    # Test 1: Large-Cap Stability Test
    # -------------------------------------------------

    def run_large_cap_stability_test(self):
        results = []

        end_date = date.today()
        start_date = end_date - timedelta(days=TIME_PERIODS["5y"])

        for ticker in LARGE_CAP_TICKERS:
            df = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=False
            )

            if df.empty or len(df) < 2:
                continue
            
            price_data = []
            for row in df.itertuples(index=True, name=None):
                price_data.append({
                "date": row[0].date(),     # index
                    "open": float(row[1]),     # Open
                    "close": float(row[4]),    # Close
                    "symbol": ticker
                })

            engine = BacktestEngine(
                ticker=ticker,
                price_data=price_data,
                strategy=self.strategy
            )

            result = engine.run()

            results.append({
                "ticker": ticker,
                "strategy_return": result.strategy_return_pct,
                "buy_and_hold_return": result.buy_and_hold_return_pct,
                "alpha": result.strategy_return_pct - result.buy_and_hold_return_pct,
                "max_drawdown": result.max_drawdown_pct,
                "trades": result.trades_count,
                "time_in_market": result.time_in_market_pct
            })

        return results


# -------------------------------------------------
# Research Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    # Load strategy
    strategy_name = "mock"
    module_path, class_name = STRATEGIES[strategy_name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    StrategyClass = getattr(module, class_name)
    strategy = StrategyClass()

    engine = BacktestEngine(
        ticker=None,
        price_data=None,
        strategy=strategy
    )

    results = engine.run_large_cap_stability_test()

    print("\n=== Test 1: Large-Cap Stability Results ===\n")

    for r in results:
        print(
            f"{r['ticker']}: "
            f"Strategy={r['strategy_return']:.2%}, "
            f"Buy&Hold={r['buy_and_hold_return']:.2%}, "
            f"Alpha={r['alpha']:.2%}, "
            f"MaxDD={r['max_drawdown']:.2%}, "
            f"Trades={r['trades']}, "
            f"TimeInMarket={r['time_in_market']:.2%}"
        )

    alphas = [r["alpha"] for r in results]

    print("\n=== Aggregate Summary ===")
    print(f"Tickers tested: {len(results)}")
    print(f"Median Alpha: {sorted(alphas)[len(alphas)//2]:.2%}")
    print(f"Best Alpha: {max(alphas):.2%}")
    print(f"Worst Alpha: {min(alphas):.2%}")
