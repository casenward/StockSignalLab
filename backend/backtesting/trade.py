from datetime import date

class Trade:
    def __init__(
        self,
        ticker: str,
        entry_price: float,
        exit_price: float,
        entry_date: date,
        exit_date: date
    ):
        
        if entry_price <= 0:
            raise ValueError("entry_price must be > 0")

        self.ticker = ticker
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.return_pct = ((exit_price - entry_price) / entry_price) * 100
        self.duration_days = (exit_date - entry_date).days

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "entry_date": self.entry_date.isoformat(),
            "exit_date": self.exit_date.isoformat(),
            "return_pct": self.return_pct,
            "duration_days": self.duration_days
        }
