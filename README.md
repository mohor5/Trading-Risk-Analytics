# Trading Risk Analytics

A Python and SQL project that stores stock prices and portfolio holdings in a database, computes portfolio risk metrics, and shows them on a web dashboard.

## What it does
- Stores prices and holdings in SQLite with primary keys, foreign keys and CHECK constraints
- SQL window functions (LAG, running MAX), joins and CTEs for daily returns, portfolio value and drawdown
- Annualized volatility, historical Value at Risk (95% and 99%) and maximum drawdown
- REST API (FastAPI) with input validation
- Dashboard with metric cards, value and drawdown charts, and a holdings table
- Unit and API tests, including hand-checked values and database constraint checks

## Run it
    pip install -r requirements.txt
    python generate_data.py
    python -m uvicorn api:app --reload

Open http://127.0.0.1:8000/ for the dashboard or http://127.0.0.1:8000/docs for the API docs.

Command-line report:

    python report.py

## API
| Endpoint | Returns |
|---|---|
| GET /summary | Volatility, VaR (95% and 99%), maximum drawdown |
| GET /var?confidence=0.95 | VaR at a chosen confidence level (between 0 and 1) |
| GET /portfolio/value | Portfolio value per day |
| GET /portfolio/drawdown | Drawdown per day |
| GET /holdings | Holdings with latest value and weight |

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