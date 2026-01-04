# StockSignalLab — Version 3  
## Backtesting Engine

## Overview

**Version 3** adds a working **backtesting engine** to StockSignalLab.

This version answers a simple question:

> *If I followed my signals in the past, what would have happened?*

The focus of Version 3 is correctness and clean execution, not profitability.

---

## What Version 3 Does

- Runs trading strategies on historical price data
- Executes trades using next-day prices (no look-ahead)
- Tracks each trade from entry to exit
- Produces basic performance metrics
- Allows strategy and time period selection from the terminal

---

## How It Works

### Backtest Engine
- Loops through historical data day by day
- Asks the strategy for a signal (`1 = buy`, `0 = hold`, `-1 = sell`)
- Executes trades at the next day’s open
- Records completed trades and results

### Strategies
- Use historical price data only
- Return a buy, hold, or sell signal
- Do not fetch data or manage trades

---

## Output

Each backtest produces:
- A list of trades with entry date, exit date, and return
- A summary including total return, win rate, and time in market

---

## Version History

- **Version 1** — Consensus scoring  
- **Version 2** — Signal generation  
- **Version 3** — Backtesting and execution  

---
