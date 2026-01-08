class TrendFollowerStrategy:
    """
    Classic trend-following strategy:
    - Buy when price > 200-day MA
    - Sell when price < 200-day MA
    """

    def calculate_signal(self, historical_data):
        if len(historical_data) < 200:
            return 0  # not enough data

        closes = [day["close"] for day in historical_data]
        price_today = closes[-1]
        ma_200 = sum(closes[-200:]) / 200

        if price_today > ma_200:
            return 1
        elif price_today < ma_200:
            return -1
        else:
            return 0
