class MockStrategy:
    """
    MockStrategy - A simple AI generated mock trading strategy for backtesting, used to test simple backtest engine functionality.

    Purpose:
    - Validate backtesting engine behavior with a realistic, deterministic strategy
    - NOT designed to be profitable
    - Designed to be fast, repeatable, and architecture-correct

    Strategy Logic:
    - Uses a 20-day simple moving average (SMA)
    - Entry:
        Buy when price crosses ABOVE the 20-day SMA
    - Exit:
        Sell when price falls 2% BELOW the 20-day SMA

    Assumptions:
    - historical_data is a list of daily price dictionaries
    - Each element contains at least:
        {
            "date": datetime.date,
            "close": float
        }
    - historical_data is ordered chronologically
    """

    def calculate_signal(self, historical_data) -> int:
        if len(historical_data) < 21:
            return 0

        closes = [day["close"] for day in historical_data]

        price_today = closes[-1]
        price_yesterday = closes[-2]

        ma_today = sum(closes[-20:]) / 20
        ma_yesterday = sum(closes[-21:-1]) / 20

        if price_today > ma_today and price_yesterday <= ma_yesterday:
            return 1

        if price_today < ma_today * 0.98:
            return -1

        return 0
