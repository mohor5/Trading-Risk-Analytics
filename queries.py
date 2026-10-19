"""SQL queries (window functions, joins, CTEs)."""

# Daily return of each stock: today's close / yesterday's close - 1.
DAILY_RETURNS_SQL = """
SELECT symbol,
       trade_date,
       close / LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date) - 1
           AS daily_return
FROM prices
ORDER BY symbol, trade_date
"""

# Total portfolio value per day: sum of close * quantity across holdings.
PORTFOLIO_VALUE_SQL = """
SELECT p.trade_date AS trade_date,
       SUM(p.close * h.quantity) AS value
FROM prices p
JOIN holdings h ON h.symbol = p.symbol
GROUP BY p.trade_date
ORDER BY p.trade_date
"""

# Daily portfolio return, built on the portfolio value CTE.
PORTFOLIO_RETURNS_SQL = f"""
WITH v AS ({PORTFOLIO_VALUE_SQL})
SELECT trade_date,
       value / LAG(value) OVER (ORDER BY trade_date) - 1 AS daily_return
FROM v
ORDER BY trade_date
"""

# Drawdown: how far the portfolio is below its highest value so far.
DRAWDOWN_SQL = f"""
WITH v AS ({PORTFOLIO_VALUE_SQL}),
p AS (
    SELECT trade_date,
           value,
           MAX(value) OVER (
               ORDER BY trade_date
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS peak
    FROM v
)
SELECT trade_date, value, peak, value / peak - 1 AS drawdown
FROM p
ORDER BY trade_date
"""

# Each holding valued at its most recent close.
HOLDINGS_SQL = """
SELECT h.symbol,
       h.quantity,
       p.close AS latest_close,
       h.quantity * p.close AS market_value
FROM holdings h
JOIN prices p ON p.symbol = h.symbol
WHERE p.trade_date = (SELECT MAX(trade_date)
                      FROM prices
                      WHERE symbol = h.symbol)
ORDER BY market_value DESC
"""
