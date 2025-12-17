# Stock Outlook App — Version 1  
## Stock Consensus & Scoring Engine

## Overview

The **Stock Outlook App** is a backend-driven stock analysis application that computes a weighted consensus score for individual equities using analyst recommendations, price momentum, and fundamental financial metrics.

Version 1 focuses on **evaluating stocks at a single point in time**, producing an interpretable score and human-readable rating (Strong Buy → Strong Sell).

---

## Purpose of Version 1

The goal of Version 1 is to answer the question:

> **“Given currently available data, how attractive does this stock look based on a defined set of rules?”**

This version is intentionally **rule-based and transparent**, prioritizing interpretability over prediction or automation.

---

## Key Features

- Composite stock scoring system (0–100)
- Weighted factor model combining:
  - Analyst consensus
  - Price momentum
  - Valuation metrics
  - Dividend yield
- Clear mapping from score → rating
- REST API built with FastAPI
- Modular backend architecture
- Live market data integration

---

## Scoring Model

Each stock is evaluated using a weighted combination of factors:

| Factor | Weight |
|------|-------|
| Analyst consensus (Yahoo Finance) | 40% |
| 1-year price momentum | 25% |
| P/E ratio | 15% |
| P/B ratio | 10% |
| Dividend yield | 10% |
| **Total** | **100%** |

Each factor is scored independently on a normalized scale and combined into a single composite score.

---

## Output

For a given stock symbol, the system returns:

- Stock symbol
- Company name
- Current market price
- Composite score (0–100)
- Consensus rating:
  - Strong Buy
  - Buy
  - Hold
  - Sell
  - Strong Sell

---

## Architecture Overview

### Backend
- FastAPI for API routing
- Service-based design for scoring logic
- Domain model representing a stock entity
- External API integrations:
  - Finnhub (pricing & fundamentals)
  - Yahoo Finance (analyst recommendations & historical prices)

### API Endpoint

