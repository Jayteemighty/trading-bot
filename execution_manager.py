import MetaTrader5 as mt5

class ExecutionManager:
    def __init__(self, signal_data, risk_manager, symbol, dry_run=True):
        self.signal_data = signal_data
        self.risk_manager = risk_manager
        self.symbol = symbol
        self.dry_run = dry_run  # New parameter to control dry run mode

    def execute_trade(self, action, lot_size=0.1, deviation=20):
        """
        Executes a trade based on the action ('BUY' or 'SELL') and calculated stop loss.
        """
        # Get the current market price
        symbol_info = mt5.symbol_info(self.symbol)
        if not symbol_info:
            print(f"{self.symbol} not found")
            return None

        # Ensure the symbol is available for trading
        if not symbol_info.visible:
            mt5.symbol_select(self.symbol, True)

        # Define trade action parameters
        action_type = mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(self.symbol).ask if action == "BUY" else mt5.symbol_info_tick(self.symbol).bid
        stop_loss = self.risk_manager.set_stop_loss(price, "uptrend" if action == "BUY" else "downtrend")

        if self.dry_run:
            # Dry run: only print the action without executing
            print(f"[Dry Run] {action} at {price} with SL at {stop_loss}")
            return None

        # Real trade request structure
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lot_size,
            "type": action_type,
            "price": price,
            "sl": stop_loss,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Trading bot order",
        }

        # Send order
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order failed: {result.retcode}")
            return None

        print(f"Order executed: {action} at {price} with SL at {stop_loss}")
        return result