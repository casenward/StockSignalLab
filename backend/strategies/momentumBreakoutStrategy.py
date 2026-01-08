class MomentumBreakoutStrategy:
    """
    Momentum breakout strategy:
    - Buy on 20-day breakout
    - Sell on 10-day breakdown
    """

    def calculate_signal(self, historical_data):
        if len(historical_data) < 20:
            return 0

        closes = [day["close"] for day in historical_data]

        price_today = closes[-1]
        high_20 = max(closes[-20:])
        low_10 = min(closes[-10:])

        if price_today >= high_20:
            return 1
        elif price_today <= low_10:
            return -1
        else:
            return 0
