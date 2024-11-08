class RiskManager:
    def __init__(self, trend_data):
        self.trend_data = trend_data

    def set_stop_loss_4hr(self, entry_price, low_price):
        """
        Sets stop loss below the last low for the 4-hour timeframe.
        """
        stop_loss = low_price * 0.98  # Example stop loss calculation
        return stop_loss

    def set_stop_loss_30min(self, support_price):
        """
        Sets stop loss below the support level for the 30-minute timeframe.
        """
        stop_loss = support_price * 0.98  # Example stop loss calculation
        return stop_loss
