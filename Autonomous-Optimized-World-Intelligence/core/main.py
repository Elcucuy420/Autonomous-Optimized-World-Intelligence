"""
Main entry point for Autonomous‑Optimized‑World‑Intelligence
-----------------------------------------------------------

This script demonstrates how to wire up strategy modules from the `modules` package.  It
loads configuration (currently a placeholder), instantiates each strategy and runs it.  In
a real deployment, this would coordinate data feeds, risk management and order routing.

To run the demonstration:

```
python -m Autonomous-Optimized-World-Intelligence.core.main
```
"""

from modules.ultra_scalp.strategy import UltraScalpStrategy
from modules.liquidity_sweep.strategy import LiquiditySweepStrategy
from modules.vwap_magnet.strategy import VWAPMagnetStrategy


def load_config():
    """Load configuration for strategies (placeholder)."""
    # In a real scenario, you might read from JSON/YAML files in the config/ directory.
    return {
        "ultra_scalp": {"param1": 42},
        "liquidity_sweep": {"param2": 0.01},
        "vwap_magnet": {"param3": 5},
    }


def main():
    config = load_config()

    # Instantiate strategies
    ultra = UltraScalpStrategy(config.get("ultra_scalp"))
    liquidity = LiquiditySweepStrategy(config.get("liquidity_sweep"))
    vwap = VWAPMagnetStrategy(config.get("vwap_magnet"))

    # Run each strategy (demonstration)
    print("Starting A.O.W.I strategies…")
    ultra.run()
    liquidity.run()
    vwap.run()
    print("Finished running strategies.")


if __name__ == "__main__":
    main()