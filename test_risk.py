import math
import sqlite3
import statistics
import unittest

from db import connect
from risk import (annualized_volatility, drawdown_series, historical_var,
                  holdings_summary, max_drawdown, portfolio_returns,
                  portfolio_value_series)


def tiny_db():
    """One stock, 10 shares, closes 100 -> 110 -> 99 -> 108.9."""
    conn = connect()
    conn.execute("INSERT INTO stocks(symbol) VALUES ('AAA')")
    for day, close in [("2024-01-01", 100), ("2024-01-02", 110),
                       ("2024-01-03", 99), ("2024-01-04", 108.9)]:
        conn.execute("INSERT INTO prices VALUES ('AAA', ?, ?)", (day, close))
    conn.execute("INSERT INTO holdings VALUES ('AAA', 10)")
    return conn


class TestRisk(unittest.TestCase):
    def test_portfolio_returns(self):
        returns = portfolio_returns(tiny_db())
        for got, want in zip(returns, [0.1, -0.1, 0.1]):
            self.assertAlmostEqual(got, want)

    def test_max_drawdown(self):
        self.assertAlmostEqual(max_drawdown(tiny_db()), -0.1)

    def test_volatility_matches_definition(self):
        returns = [0.1, -0.1, 0.1]
        expected = statistics.stdev(returns) * math.sqrt(252)
        self.assertAlmostEqual(annualized_volatility(returns), expected)

    def test_var_picks_worst_tail_loss(self):
        returns = [0.1, -0.1, 0.1]
        self.assertAlmostEqual(historical_var(returns, 0.95), 0.1)

    def test_var_on_100_returns(self):
        returns = [i / 1000 - 0.05 for i in range(100)]  # -5% .. +4.9%
        self.assertAlmostEqual(historical_var(returns, 0.95), 0.045)

    def test_var_never_negative(self):
        self.assertEqual(historical_var([0.01, 0.02, 0.03], 0.95), 0.0)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            historical_var([])
        with self.assertRaises(ValueError):
            historical_var([0.1], confidence=1.5)
        with self.assertRaises(ValueError):
            annualized_volatility([0.1])


class TestSeries(unittest.TestCase):
    def test_value_series(self):
        series = portfolio_value_series(tiny_db())
        self.assertEqual(len(series), 4)
        self.assertAlmostEqual(series[1]["value"], 1100)

    def test_drawdown_series(self):
        series = drawdown_series(tiny_db())
        self.assertEqual(series[0]["drawdown"], 0)
        self.assertAlmostEqual(min(s["drawdown"] for s in series), -0.1)

    def test_holdings_summary_single_stock(self):
        rows = holdings_summary(tiny_db())
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["market_value"], 1089)
        self.assertAlmostEqual(rows[0]["weight"], 1.0)

    def test_holdings_weights_sum_to_one(self):
        conn = tiny_db()
        conn.execute("INSERT INTO stocks(symbol) VALUES ('BBB')")
        conn.execute("INSERT INTO prices VALUES ('BBB', '2024-01-04', 50)")
        conn.execute("INSERT INTO holdings VALUES ('BBB', 20)")
        rows = holdings_summary(conn)
        self.assertAlmostEqual(sum(r["weight"] for r in rows), 1.0)
        self.assertEqual(rows[0]["symbol"], "AAA")  # largest first


class TestSchema(unittest.TestCase):
    def test_duplicate_price_rejected(self):
        conn = tiny_db()
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO prices VALUES ('AAA', '2024-01-01', 5)")

    def test_non_positive_quantity_rejected(self):
        conn = connect()
        conn.execute("INSERT INTO stocks(symbol) VALUES ('BBB')")
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO holdings VALUES ('BBB', 0)")

    def test_unknown_symbol_rejected(self):
        conn = connect()
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO prices VALUES ('ZZZ', '2024-01-01', 5)")


if __name__ == "__main__":
    unittest.main()
