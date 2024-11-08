import os
import time
import MetaTrader5 as mt5
from data_fetcher import DataFetcher
from trend_analyzer import TrendAnalyzer
from signal_generator import SignalGenerator
from risk_manager import RiskManager
from execution_manager import ExecutionManager

# Load MT5 credentials from environment variables
MT5_LOGIN = os.getenv("MT5_LOGIN")
MT5_PASSWORD = os.getenv("MT5_PASSWORD")
MT5_SERVER = os.getenv("MT5_SERVER")

# Initialize MetaTrader 5 with credentials
if not mt5.initialize(login=int(MT5_LOGIN), password=MT5_PASSWORD, server=MT5_SERVER):
    print("MT5 initialization failed.")
    mt5.shutdown()
    exit()

print("MT5 initialized successfully")

# Define the trading symbol and bot parameters
SYMBOL = "EURUSD"

# Initialize bot components
fetcher = DataFetcher(SYMBOL)
analyzer = None
generator = None
risk_manager = None
executor = None

def run_bot():
    global analyzer, generator, risk_manager, executor

    # Fetch data
    data_4hr = fetcher.fetch_4hr_data()
    data_30min = fetcher.fetch_30min_data()

    # Initialize and run the trend analysis
    analyzer = TrendAnalyzer(data_4hr)
    trend_data = analyzer.analyze_trend()

    # Generate trade signals based on trend data
    generator = SignalGenerator(trend_data)
    signal_data = generator.generate_signals()

    # Manage risk based on the generated signals
    risk_manager = RiskManager(signal_data)
    executor = ExecutionManager(signal_data, risk_manager, SYMBOL, dry_run=False)

    # Execute trades based on signals
    for i, row in signal_data.iterrows():
        executor.execute_trade(row['signal'], row['entry_price'], row['stop_loss'])

while True:
    try:
        run_bot()
        print("Bot cycle complete. Waiting 15 minutes before the next cycle.")
    except Exception as e:
        print(f"Error during bot execution: {e}")
    
    # Wait for 15 minutes before the next execution cycle
    time.sleep(900)  # 900 seconds = 15 minutes

# Shutdown MetaTrader5 after completion (this will not be reached due to infinite loop)
mt5.shutdown()
