class TrendAnalyzer:
    def __init__(self, data):
        self.data = data

    def is_uptrend(self, row):
        """
        Checks for higher highs and higher lows to identify an uptrend.
        """
        previous_low = self.data["low"].shift(1)
        previous_high = self.data["high"].shift(1)
        is_higher_low = row["low"] > previous_low
        is_higher_high = row["high"] > previous_high
        return is_higher_low and is_higher_high

    def is_double_top(self, row):
        """
        Checks for a double top pattern within the defined criteria.
        """
        previous_high = self.data["high"].shift(1)
        current_high = row["high"]
        within_range = abs(current_high - previous_high) <= previous_high * 0.01
        return within_range

    def analyze_trend(self):
        """
        Analyzes the entire data and adds trend signals.
        """
        self.data["uptrend"] = self.data.apply(self.is_uptrend, axis=1)
        self.data["double_top"] = self.data.apply(self.is_double_top, axis=1)
        return self.data
