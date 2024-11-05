import MetaTrader5 as mt5

class ExecutionManager:
    def __init__(self, signal_data, risk_manager, symbol):
        self.signal_data = signal_data
        self.risk_manager = risk_manager
        self.symbol = symbol

    def execute_trade(self, action, lot_size=0.1, deviation=20):
        """
        Executes a trade based on the action ('BUY' or 'SELL') and calculated stop loss.
        """
        symbol_info = mt5.symbol_info(self.symbol)
        if not symbol_info:
            print(f"{self.symbol} not found")
            return None

        if not symbol_info.visible:
            mt5.symbol_select(self.symbol, True)

        action_type = mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(self.symbol).ask if action == "BUY" else mt5.symbol_info_tick(self.symbol).bid
        stop_loss = self.risk_manager.set_stop_loss(price, "uptrend" if action == "BUY" else "downtrend")

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lot_size,
            "type": action_type,
            "price": price,
            "sl": stop_loss,
            "deviation": deviation,
            "magic": 234000,  # Magic number to identify orders by this bot
            "comment": "Trading bot order",
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order failed: {result.retcode}")
            return None

        print(f"Order executed: {action} at {price} with SL at {stop_loss}")
        return result
