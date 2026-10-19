"""Risk metrics computed from the database."""
import math
import statistics

from queries import DRAWDOWN_SQL, PORTFOLIO_RETURNS_SQL

TRADING_DAYS = 252


def portfolio_returns(conn):
    """Daily portfolio returns (the first day has no return and is skipped)."""
    rows = conn.execute(PORTFOLIO_RETURNS_SQL).fetchall()
    return [r for _, r in rows if r is not None]


def annualized_volatility(returns):
    """Standard deviation of daily returns scaled to a year."""
    if len(returns) < 2:
        raise ValueError("need at least 2 returns")
    return statistics.stdev(returns) * math.sqrt(TRADING_DAYS)


def historical_var(returns, confidence=0.95):
    """One-day historical Value at Risk, as a positive fraction of value.

    Example: 0.03 at 95% means that on 95% of past days the portfolio
    lost less than 3%.
    """
    if not returns:
        raise ValueError("no returns")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    ordered = sorted(returns)
    index = int(len(ordered) * (1 - confidence))
    return max(-ordered[index], 0.0)


def max_drawdown(conn):
    """Largest peak-to-trough fall, as a negative fraction (e.g. -0.12)."""
    rows = conn.execute(DRAWDOWN_SQL).fetchall()
    if not rows:
        raise ValueError("no data")
    return min(row[3] for row in rows)
