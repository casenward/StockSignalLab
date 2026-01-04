## This is the test mock strategy for authentication, this strategy will include apis

from datetime import timedelta
import yfinance as yf


class MockStrategy:
    def calculate_signal(self, historical_data) -> int:
        symbol = historical_data[-1]["symbol"]
        as_of_date = historical_data[-1]["date"]

        start_date = as_of_date - timedelta(days=90)

        df = yf.download(
            symbol,
            start=start_date,
            end=as_of_date,   
            progress=False
        )

        if df.empty or len(df) < 30:
            return 0

        closes = df["Close"]

        ma_20 = closes.rolling(20).mean()

        price_today = float(closes.iloc[-1])
        price_yesterday = float(closes.iloc[-2])

        ma_today = float(ma_20.iloc[-1])
        ma_yesterday = float(ma_20.iloc[-2])

        # ------------------------
        # ENTRY: bullish breakout
        # ------------------------
        if price_today > ma_today and price_yesterday <= ma_yesterday:
            return 1

        # ------------------------
        # EXIT: decisive breakdown
        # ------------------------
        if price_today < ma_today * 0.98:
            return -1

        return 0

