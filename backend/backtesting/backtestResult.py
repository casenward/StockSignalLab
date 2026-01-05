from datetime import date
from typing import List
from backend.backtesting.trade import Trade

class BacktestResult:
    def __init__(
        self,
        ticker: str,
        start_date: date,
        end_date: date,
        trades: List[Trade],
        price_data: List[dict] = None
    ):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.trades = trades
        self.price_data = price_data or []

        self.num_trades = len(trades)
        self.total_return_pct = self._compute_total_return()
        self.buy_and_hold_return_pct = self._compute_buy_and_hold_return()
        self.win_rate_pct = self._compute_win_rate()
        self.avg_trade_duration_days = self._compute_avg_duration()
        self.time_in_market_pct = self._compute_time_in_market()
        self.max_drawdown_pct = self._compute_max_drawdown()

    ## Internal computation methods
    def _compute_total_return(self) -> float:
        equity = 1.0
        for trade in self.trades:                
            equity *= (1 + trade.return_pct / 100)
        return (equity - 1) * 100

    def _compute_buy_and_hold_return(self) -> float:
        if not self.price_data or len(self.price_data) < 2:
            return 0.0
        start_price = self.price_data[0]["close"]
        end_price = self.price_data[-1]["close"]
        return ((end_price - start_price) / start_price) * 100

    def _compute_win_rate(self) -> float:
        if self.num_trades == 0:
            return 0.0
        wins = sum(1 for t in self.trades if t.return_pct > 0)
        return (wins / self.num_trades) * 100

    def _compute_avg_duration(self) -> float:
        if self.num_trades == 0:
            return 0.0
        return sum(t.duration_days for t in self.trades) / self.num_trades

    def _compute_time_in_market(self) -> float:
        total_days = (self.end_date - self.start_date).days
        if total_days <= 0:
            return 0.0
        invested_days = sum(t.duration_days for t in self.trades)
        return (invested_days / total_days) * 100

    def _compute_max_drawdown(self) -> float:
        peak = 1.0
        equity = 1.0
        max_dd = 0.0

        for trade in self.trades:
            equity *= (1 + trade.return_pct / 100)
            peak = max(peak, equity)
            drawdown = (peak - equity) / peak
            max_dd = max(max_dd, drawdown)

        return max_dd * 100

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "num_trades": self.num_trades,
            "total_return_pct": self.total_return_pct,
            "buy_and_hold_return_pct": self.buy_and_hold_return_pct,
            "win_rate_pct": self.win_rate_pct,
            "avg_trade_duration_days": self.avg_trade_duration_days,
            "time_in_market_pct": self.time_in_market_pct,
            "max_drawdown_pct": self.max_drawdown_pct,
        }
