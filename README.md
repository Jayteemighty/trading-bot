# MT5 Trading Bot

This is a Python-based trading bot that connects to MetaTrader 5 (MT5) to automate trading strategies on the EURUSD currency pair. The bot uses two main strategies based on trend detection, double bottom formations, and trendline breaks.

## **Overview of the Trading Strategies**

### **Strategy 1: 4HR Uptrend Confirmation and Trade Setup**
1. **Trend Detection**: Identifies an uptrend with two higher highs and higher lows. The higher lows must touch the trendline.
2. **Trade Setup**: After the trend is confirmed, the bot enters a long position when the next high is broken (based on a 4HR candle close above the broken high).
3. **Stop Loss**: The stop loss is set below the last low of the broken high.
4. **Exit Strategy**:
   - Close half of the position if one 4HR red candle forms.
   - Set the remaining position to break-even.
   - Close all trades if the price reaches past a high, the trend changes, or the stop loss is triggered.

### **Strategy 2: 30MIN Uptrend Trade Setup after 4HR Trend Confirmation**
1. **Support Zone**: The support zone is determined from the 4HR timeframe.
2. **Trade Setup**:
   - Wait for a double bottom or a trendline break.
   - Enter a long position if the double bottom breaks its neckline or the trendline breaks the last high.
3. **Exit Strategy**:
   - Exit half of the position if two 4HR red candles form or one long 4HR red candle forms.
   - Set the remaining position to break-even.

---

## **Setup Instructions**

### **Step 1: Install MetaTrader 5 and Python API**

1. **Download and Install MetaTrader 5 (MT5)**:
   - Go to the [MetaTrader 5 website](https://www.metatrader5.com/en) and download the platform.
   - Install MT5 on your computer and create a demo or live trading account.

2. **Install the MetaTrader 5 Python API**:
   - Open a terminal or command prompt and install the MetaTrader 5 API using pip:
     ```bash
     pip install MetaTrader5
     ```

### **Step 2: Set Up Python Script**

1. **Save the Python Script**:
   - Copy the provided Python code into a `.py` file (e.g., `mt5_trading_bot.py`).

2. **Set Up Your MT5 Account**:
   - In the MT5 platform, ensure your account is connected to the broker and has sufficient margin to test the strategies.
   - Take note of your login credentials for the account, as you will need them to connect MT5 through Python.

### **Step 3: Run the Python Script**

1. **Run the Script**:
   - Open a terminal or command prompt and navigate to the folder where the Python script is located.
   - Run the script using the following command:
     ```bash
     python mt5_trading_bot.py
     ```

2. **Check Results**:
   - The bot will analyze the EURUSD market using the 4HR and 30MIN timeframes.
   - If the strategy conditions are met, it will place a buy order with the specified stop loss and take profit.
   - The bot will shut down after running.

### **Step 4: Monitor the Trades**

- In MetaTrader 5, you can monitor the trades opened by the bot under the "Trade" tab.
- The bot will manage the position based on the strategy conditions (such as closing half of the position after a red candle).

---

## **Additional Notes**

- The bot currently only trades EURUSD, but it can be modified to support other pairs.
- The strategies implemented follow the provided rules, including trend detection, double bottom formation, and trade management (stop loss, take profit, closing half of the position, etc.).
- Ensure that you have a demo account set up before running the bot on a live account to avoid financial risks.
- The stop loss and take profit values can be adjusted based on your risk management preferences.

---

## **Acknowledgments**

This trading bot is built using the MetaTrader 5 Python API. For more information, visit the official MetaTrader 5 website and the Python API documentation.

---

**License**: MIT
