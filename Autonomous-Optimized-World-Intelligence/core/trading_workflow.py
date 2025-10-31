"""
Trading workflow for Autonomous‑Optimized‑World‑Intelligence
-----------------------------------------------------------

This script orchestrates the execution of trading strategies and outputs trade
instructions. It is designed to work in two modes:

* **Simulation mode**: When the MetaTrader5 package is not installed or a
  broker connection cannot be established, the script will run the
  strategies and simply print the orders that would be placed.  This is
  useful for development and testing without risking real capital.
* **Live mode**: If the `MetaTrader5` package is available and a running
  MetaTrader terminal is detected, the script will attempt to connect and
  execute orders.  Note that live order execution requires valid
  credentials and a configured terminal; this example does not handle
  authentication details and will still run in simulation mode without them.

Usage example::

    # Make sure the repository root is on PYTHONPATH
    PYTHONPATH=/path/to/Autonomous-Optimized-World-Intelligence \
        python Autonomous-Optimized-World-Intelligence/core/trading_workflow.py

"""

from __future__ import annotations

import sys
from typing import Dict, Any

try:
    import MetaTrader5 as mt5  # type: ignore[import]
    HAVE_MT5 = True
except ImportError:
    # If the MetaTrader5 package is not installed, we operate in simulation mode.
    HAVE_MT5 = False

from modules.ultra_scalp.strategy import UltraScalpStrategy
from modules.liquidity_sweep.strategy import LiquiditySweepStrategy
from modules.vwap_magnet.strategy import VWAPMagnetStrategy


def load_config() -> Dict[str, Any]:
    """Load configuration for strategies.

    In a real implementation, this would read configuration values from a
    file under the ``config/`` directory.  For now, it returns empty
    dictionaries for each strategy.
    """
    return {
        "ultra_scalp": {},
        "liquidity_sweep": {},
        "vwap_magnet": {},
    }


def connect_to_broker() -> bool:
    """Attempt to connect to a MetaTrader5 terminal.

    Returns ``True`` if a connection is established; otherwise returns
    ``False`` and the script will proceed in simulation mode.
    """
    if not HAVE_MT5:
        print("MetaTrader5 package not installed. Running in simulation mode.")
        return False

    # Attempt to initialise a connection to a running MT5 terminal.  This
    # requires that the terminal is running locally and configured for API
    # access.
    if not mt5.initialize():
        err = mt5.last_error()
        print(f"Failed to initialise MT5: {err}")
        return False
    print("Connected to MetaTrader5 terminal.")
    return True


def disconnect_broker() -> None:
    """Shut down the MetaTrader5 connection if it was initialised."""
    if HAVE_MT5:
        mt5.shutdown()


def simulate_signal(strategy_name: str) -> Dict[str, Any]:
    """Return a dummy trade signal for a given strategy.

    This function is a stand‑in for real signal generation.  In a production
    system, the strategies themselves would compute entry/exit signals and
    risk parameters.  Here, we return hardcoded examples for each strategy.
    """
    if strategy_name == "UltraScalpStrategy":
        return {
            "symbol": "EURUSD",
            "type": "buy",
            "volume": 0.10,
            "comment": "UltraScalp demo order",
        }
    if strategy_name == "LiquiditySweepStrategy":
        return {
            "symbol": "GBPUSD",
            "type": "sell",
            "volume": 0.05,
            "comment": "LiquiditySweep demo order",
        }
    if strategy_name == "VWAPMagnetStrategy":
        return {
            "symbol": "USDJPY",
            "type": "buy",
            "volume": 0.20,
            "comment": "VWAPMagnet demo order",
        }
    return {}


def place_trade(order: Dict[str, Any], live: bool) -> None:
    """Execute a trade or simulate it depending on ``live``.

    :param order: A dictionary representing the order parameters.
    :param live: If ``True``, attempts to send the order via MetaTrader5.
                 If ``False``, just prints the order details.
    """
    if not order:
        return
    if live and HAVE_MT5:
        # Construct a simple market order.  For a real system, you'd want
        # to include price, slippage, stop loss (sl), take profit (tp) etc.
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order["symbol"],
            "volume": order["volume"],
            "type": mt5.ORDER_TYPE_BUY if order["type"].lower() == "buy" else mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(order["symbol"]).ask if order["type"].lower() == "buy" else mt5.symbol_info_tick(order["symbol"]).bid,
            "deviation": 10,
            "magic": 0,
            "comment": order.get("comment", "AOWI auto order"),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to place order: {result.retcode}, {result.comment}")
        else:
            print(f"Order placed successfully: ticket {result.order}")
    else:
        # Simulation mode: just print the order details
        print(f"[SIMULATION] Would place order: {order}")


def main() -> None:
    """Entry point for the trading workflow."""
    config = load_config()

    # Instantiate strategy objects
    strategies = [
        UltraScalpStrategy(config.get("ultra_scalp")),
        LiquiditySweepStrategy(config.get("liquidity_sweep")),
        VWAPMagnetStrategy(config.get("vwap_magnet")),
    ]

    live_trading = connect_to_broker()
    try:
        print("Running trading workflow…")
        for strat in strategies:
            # Run the strategy's logic (currently just prints a message)
            strat.run()
            # Generate a dummy signal for demonstration
            signal = simulate_signal(strat.__class__.__name__)
            # Place the trade or simulate it
            place_trade(signal, live_trading)
    finally:
        if live_trading:
            disconnect_broker()
        print("Trading workflow finished.")


if __name__ == "__main__":
    main()
