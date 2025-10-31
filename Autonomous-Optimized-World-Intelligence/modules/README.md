# Modules

Strategy modules live in this directory.  Each module encapsulates a specific trading or prediction strategy, including entry/exit logic, indicator calculations and parameter configurations.  Examples of modules include:

- `ultra_scap` – high‑frequency scalping strategy.
- `liquidity_sweep` – algorithm that detects and exploits liquidity spikes.
- `vwap_magnet` – strategy that trades reversions toward VWAP.
- `risk_reversion` – module that adjusts positions based on market conditions.

Modules should expose a clear API for integration into the core engine or deployment scripts, and include tests where applicable.