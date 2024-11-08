import MetaTrader5 as mt5
import pandas as pd

class DataFetcher:
    def __init__(self, symbol):
        self.symbol = symbol

    def fetch_data(self, timeframe=mt5.TIMEFRAME_H4, num_candles=500):
        """
        Fetch candlestick data from MT5.
        """
        rates = mt5.copy_rates_from_pos(self.symbol, timeframe, 0, num_candles)
        if rates is None:
            raise ValueError(f"Failed to get data for symbol: {self.symbol}")

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def fetch_4hr_data(self):
        return self.fetch_data(mt5.TIMEFRAME_H4)

    def fetch_30min_data(self):
        return self.fetch_data(mt5.TIMEFRAME_M30)
