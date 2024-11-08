class RiskManager:
    def __init__(self, trend_data):
        self.trend_data = trend_data

    def set_stop_loss(self, entry_price, trend):
        """
        Calculate stop loss based on the trend direction.
        """
        if trend == "uptrend":
            last_low = self.trend_data[self.trend_data["signal"] == "BUY"]["low"].iloc[-1]
            stop_loss = last_low * 0.98
        elif trend == "downtrend":
            last_high = self.trend_data[self.trend_data["signal"] == "SELL"]["high"].iloc[-1]
            stop_loss = last_high * 1.02
        return stop_loss
