"""REST API and dashboard for the trading risk analytics project.

Run with:  python -m uvicorn api:app --reload
Dashboard: http://127.0.0.1:8000/
API docs:  http://127.0.0.1:8000/docs
"""
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

from db import connect, load_holdings, load_prices
from risk import (annualized_volatility, drawdown_series, historical_var,
                  holdings_summary, max_drawdown, portfolio_returns,
                  portfolio_value_series)

BASE_DIR = Path(__file__).parent
app = FastAPI(title="Trading Risk Analytics")

# In-memory database loaded once at startup and only read afterwards.
conn = connect(check_same_thread=False)
load_prices(conn, BASE_DIR / "data" / "prices.csv")
load_holdings(conn, BASE_DIR / "data" / "holdings.csv")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/summary")
def summary():
    returns = portfolio_returns(conn)
    return {
        "days_of_returns": len(returns),
        "annualized_volatility": annualized_volatility(returns),
        "var_95": historical_var(returns, 0.95),
        "var_99": historical_var(returns, 0.99),
        "max_drawdown": max_drawdown(conn),
        "data_note": "Simulated prices, not real market data",
    }


@app.get("/var")
def value_at_risk(confidence: float = Query(0.95, gt=0, lt=1)):
    returns = portfolio_returns(conn)
    return {"confidence": confidence, "var": historical_var(returns, confidence)}


@app.get("/portfolio/value")
def portfolio_value():
    return portfolio_value_series(conn)


@app.get("/portfolio/drawdown")
def portfolio_drawdown():
    return drawdown_series(conn)


@app.get("/holdings")
def holdings():
    return holdings_summary(conn)
