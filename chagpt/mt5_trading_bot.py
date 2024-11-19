import MetaTrader5 as mt5
import pandas as pd

# Initialize MT5 connection
def initialize_mt5():
    if not mt5.initialize():
        print("Failed to initialize MetaTrader5")
        mt5.shutdown()

# Fetch data from MT5 (OHLCV data)
def fetch_data(symbol, timeframe, num_bars):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data

# Trend detection - Identify higher highs and higher lows for an uptrend
def is_uptrend(data, timeframe):
    highs = data['high']
    lows = data['low']
    # Identify swing highs and lows
    swing_highs = [i for i in range(1, len(highs)-1) if highs[i] > highs[i-1] and highs[i] > highs[i+1]]
    swing_lows = [i for i in range(1, len(lows)-1) if lows[i] < lows[i-1] and lows[i] < lows[i+1]]
    
    if len(swing_highs) >= 2 and len(swing_lows) >= 2:
        # Check higher highs and higher lows
        return highs[swing_highs[-1]] > highs[swing_highs[-2]] and lows[swing_lows[-1]] > lows[swing_lows[-2]]
    return False

# Trendline validation (Checks if higher lows touch the trendline)
def is_trendline_valid(data, swing_lows):
    if len(swing_lows) >= 2:
        low1 = swing_lows[-2]
        low2 = swing_lows[-1]
        for i in range(low2, len(data)):
            projected_low = data['low'][low1] + (data['low'][low2] - data['low'][low1]) * (i - low1) / (low2 - low1)
            if data['low'][i] < projected_low:
                return False
        return True
    return False

# Double bottom detection
def is_double_bottom(data, support_zone):
    lows = data['low']
    candidates = [i for i in range(1, len(lows)-1) if lows[i] < lows[i-1] and lows[i] < lows[i+1]]
    if len(candidates) >= 2:
        return abs(lows[candidates[-1]] - lows[candidates[-2]]) <= support_zone
    return False

# Place buy order in MT5
def place_order(direction, stop_loss):
    lot_size = 0.1  # Adjust based on your risk management
    symbol = "EURUSD"
    price = mt5.symbol_info_tick(symbol).ask
    sl = stop_loss
    tp = price + (price - sl)  # Example: 1:1 Risk-Reward Ratio

    if direction == 'BUY':
        order = mt5.order_send(
            {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot_size,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 20,
                "magic": 234000,
                "comment": "Strategy1 Trade",
            }
        )
        print(f"Order placed: {order}")

# Strategy 1 (4HR Uptrend Confirmation and Trade Setup)
def strategy1(data):
    if is_uptrend(data, '4HR') and is_trendline_valid(data, data['low']):
        next_high = max(data['high'][-10:])
        if data['close'][-1] > next_high:
            stop_loss = min(data['low'][-10:])
            place_order('BUY', stop_loss)

# Strategy 2 (30MIN Uptrend Trade Setup after 4HR Trend Confirmation)
def strategy2(data_4hr, data_30min):
    if is_uptrend(data_4hr, '4HR'):
        support_zone = min(data_4hr['low'][-10:])
        if is_double_bottom(data_30min, support_zone):
            neckline = max(data_30min['high'][-5:])
            if data_30min['close'][-1] > neckline:
                stop_loss = support_zone
                place_order('BUY', stop_loss)

# Main function to run the bot
def run_bot():
    initialize_mt5()
    
    # Fetch 4HR and 30MIN data for EURUSD
    data_4hr = fetch_data('EURUSD', mt5.TIMEFRAME_H4, 500)
    data_30min = fetch_data('EURUSD', mt5.TIMEFRAME_M30, 500)
    
    # Apply Strategy 1 and Strategy 2
    strategy1(data_4hr)
    strategy2(data_4hr, data_30min)

    # Shut down MT5
    mt5.shutdown()

# Run the bot
if __name__ == "__main__":
    run_bot()
