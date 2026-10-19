# Trading Risk Analytics

A Python and SQL project that stores stock prices and portfolio holdings in a database and computes portfolio risk metrics.

## What it does
- Stores prices and holdings in SQLite with primary keys, foreign keys and CHECK constraints
- SQL window functions (LAG, running MAX) for daily returns and drawdown
- Portfolio value per day using a join and aggregation
- Annualized volatility, historical Value at Risk (95% and 99%) and maximum drawdown
- Unit tests, including hand-checked values and database constraint checks

## Run it
    python generate_data.py
    python report.py

## Run the tests
    python -m unittest -v

## Metrics
| Metric | Definition |
|---|---|
| Annualized volatility | Standard deviation of daily returns x sqrt(252) |
| Historical VaR | Loss at the chosen percentile of past daily returns |
| Maximum drawdown | Largest fall from a previous portfolio peak |

## Note on data
Prices are simulated (random walk with a fixed seed, fictional tickers), not real market data. Any CSV with columns symbol, trade_date, close can be loaded instead.

## Status
In progress. Next: a REST API and a dashboard with charts.