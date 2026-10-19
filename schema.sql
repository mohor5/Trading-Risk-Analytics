CREATE TABLE IF NOT EXISTS stocks (
    symbol TEXT PRIMARY KEY,
    name   TEXT
);

CREATE TABLE IF NOT EXISTS prices (
    symbol     TEXT NOT NULL REFERENCES stocks(symbol),
    trade_date TEXT NOT NULL,              -- ISO format: YYYY-MM-DD
    close      REAL NOT NULL CHECK (close > 0),
    PRIMARY KEY (symbol, trade_date)
);

CREATE TABLE IF NOT EXISTS holdings (
    symbol   TEXT PRIMARY KEY REFERENCES stocks(symbol),
    quantity REAL NOT NULL CHECK (quantity > 0)
);

CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(trade_date);
