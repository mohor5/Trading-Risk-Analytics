"""Database setup and CSV loading."""
import csv
import sqlite3
from pathlib import Path

SCHEMA = Path(__file__).parent / "schema.sql"


def connect(path=":memory:", check_same_thread=True):
    conn = sqlite3.connect(path, check_same_thread=check_same_thread)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text())
    return conn


def load_prices(conn, csv_path):
    """Load rows with columns: symbol, trade_date, close."""
    with open(csv_path, newline="") as f, conn:
        for row in csv.DictReader(f):
            conn.execute("INSERT OR IGNORE INTO stocks(symbol) VALUES (?)",
                         (row["symbol"],))
            conn.execute(
                "INSERT INTO prices(symbol, trade_date, close) VALUES (?, ?, ?)",
                (row["symbol"], row["trade_date"], float(row["close"])))


def load_holdings(conn, csv_path):
    """Load rows with columns: symbol, quantity."""
    with open(csv_path, newline="") as f, conn:
        for row in csv.DictReader(f):
            conn.execute("INSERT INTO holdings(symbol, quantity) VALUES (?, ?)",
                         (row["symbol"], float(row["quantity"])))
