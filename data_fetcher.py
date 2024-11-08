import MetaTrader5 as mt5
import pandas as pd

class DataFetcher:
    def __init__(self, symbol, timeframe=mt5.TIMEFRAME_H4):
        self.symbol = symbol
        self.timeframe = timeframe

    def initialize_mt5(self):
        if not mt5.initialize():
            print("Failed to initialize MT5")
            return False
        print("MT5 initialized successfully")
        return True

    def fetch_data(self, num_candles=500):
        """
        Fetch 4-hour candlestick data from MT5.
        """
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, num_candles)
        if rates is None:
            raise ValueError(f"Failed to get data for symbol: {self.symbol}")

        # Convert to DataFrame and format the timestamp
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def preprocess_data(self, df):
        """
        Preprocess data (e.g., calculate moving averages).
        """
        df["20_SMA"] = df["close"].rolling(window=20).mean()  # Example moving average
        return df