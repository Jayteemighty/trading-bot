class SignalGenerator:
    def __init__(self, trend_data):
        self.trend_data = trend_data

    def generate_signals(self):
        """
        Generate buy/sell signals based on confirmed trends.
        """
        signals = []
        for i, row in self.trend_data.iterrows():
            if row["uptrend"]:
                signals.append("BUY")
            elif row["double_top"]:
                signals.append("SELL")
            else:
                signals.append("HOLD")
        self.trend_data["signal"] = signals
        return self.trend_data
