from data_fetcher import DataFetcher
from trend_analyzer import TrendAnalyzer
from signal_generator import SignalGenerator
from risk_manager import RiskManager
from execution_manager import ExecutionManager
import MetaTrader5 as mt5

# Define parameters
SYMBOL = "EURUSD"

# Initialize MetaTrader 5
fetcher = DataFetcher(SYMBOL)
if not fetcher.initialize_mt5():
    raise SystemExit("MT5 initialization failed.")

# Fetch and preprocess data
raw_data = fetcher.fetch_data()
processed_data = fetcher.preprocess_data(raw_data)

# Analyze trend
analyzer = TrendAnalyzer(processed_data)
trend_data = analyzer.analyze_trend()

# Generate signals
generator = SignalGenerator(trend_data)
signal_data = generator.generate_signals()

# Manage risk and execute trades
risk_manager = RiskManager(signal_data)
#executor = ExecutionManager(signal_data, risk_manager, SYMBOL)
executor = ExecutionManager(signal_data, risk_manager, SYMBOL, dry_run=True)


# Execute trades based on signals
for i, row in signal_data.iterrows():
    if row["signal"] == "BUY":
        executor.execute_trade("BUY")
    elif row["signal"] == "SELL":
        executor.execute_trade("SELL")

# Shutdown MetaTrader5 after completion
mt5.shutdown()
import MetaTrader5 as mt5

if mt5.initialize():
    print("MetaTrader 5 initialized successfully!")
    mt5.shutdown()
else:
    print("Failed to initialize MetaTrader 5")



import logging

logging.basicConfig(
    filename="trade_log.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
