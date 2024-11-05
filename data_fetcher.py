import pandas as pd
import numpy as np

class DataFetcher:
    def __init__(self, symbol, timeframe="4h"):
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch_data(self):
        """
        Simulate fetching OHLCV data. Replace this with real API data fetching.
        """
        # Here, we're simulating data. In practice, replace with API calls.
        data = {
            "timestamp": pd.date_range(start="2023-01-01", periods=500, freq="4H"),
            "open": np.random.random(500) * 100,
            "high": np.random.random(500) * 100,
            "low": np.random.random(500) * 100,
            "close": np.random.random(500) * 100,
            "volume": np.random.random(500) * 1000,
        }
        df = pd.DataFrame(data)
        df = df.sort_values(by="timestamp")
        return df

    def preprocess_data(self, df):
        """
        Preprocess the data (e.g., calculate moving averages or indicators).
        """
        df["20_SMA"] = df["close"].rolling(window=20).mean()  # Example moving average
        return df
