"""Print a risk report.

Usage: python report.py
"""
from db import connect, load_holdings, load_prices
from risk import (annualized_volatility, historical_var, max_drawdown,
                  portfolio_returns)


def main():
    conn = connect()
    load_prices(conn, "data/prices.csv")
    load_holdings(conn, "data/holdings.csv")
    returns = portfolio_returns(conn)
    print(f"Days of returns:        {len(returns)}")
    print(f"Annualized volatility:  {annualized_volatility(returns):.2%}")
    print(f"1-day VaR (95%):        {historical_var(returns, 0.95):.2%}")
    print(f"1-day VaR (99%):        {historical_var(returns, 0.99):.2%}")
    print(f"Maximum drawdown:       {max_drawdown(conn):.2%}")
    print("(Data is simulated, not real market data.)")


if __name__ == "__main__":
    main()
