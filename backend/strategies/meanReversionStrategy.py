class MeanReversionStrategy:
    """
    Mean reversion strategy using RSI:
    - Buy when RSI < 30
    - Sell when RSI > 50
    """

    def calculate_signal(self, historical_data):
        if len(historical_data) < 15:
            return 0

        closes = [day["close"] for day in historical_data]

        gains = []
        losses = []

        for i in range(1, 15):
            delta = closes[-i] - closes[-i - 1]
            if delta > 0:
                gains.append(delta)
            else:
                losses.append(abs(delta))

        if not gains:
            return 1
        if not losses:
            return -1

        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        if rsi < 30:
            return 1
        elif rsi > 50:
            return -1
        else:
            return 0
