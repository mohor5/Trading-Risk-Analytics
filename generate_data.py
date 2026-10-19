"""Generate SIMULATED daily prices (geometric random walk, fixed seed).

The tickers are fictional and the prices are not real market data.
Writes data/prices.csv and data/holdings.csv.
"""
import csv
import math
import random
from datetime import date, timedelta

SEED = 42
START = date(2024, 1, 1)
DAYS = 500  # weekdays
# symbol: (start price, daily drift, daily volatility, shares held)
STOCKS = {
    "ALPHA": (1500.0, 0.0004, 0.012, 20),
    "BETA":  (3200.0, 0.0003, 0.010, 10),
    "GAMMA": (900.0,  0.0005, 0.018, 40),
    "DELTA": (450.0,  0.0002, 0.008, 60),
    "OMEGA": (2200.0, 0.0006, 0.022, 15),
}


def weekdays(start, count):
    day = start
    while count:
        if day.weekday() < 5:
            yield day
            count -= 1
        day += timedelta(days=1)


def main():
    rng = random.Random(SEED)
    dates = list(weekdays(START, DAYS))
    with open("data/prices.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "trade_date", "close"])
        for symbol, (price, drift, vol, _) in STOCKS.items():
            for d in dates:
                price *= math.exp(drift + vol * rng.gauss(0, 1))
                writer.writerow([symbol, d.isoformat(), round(price, 2)])
    with open("data/holdings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "quantity"])
        for symbol, (_, _, _, qty) in STOCKS.items():
            writer.writerow([symbol, qty])
    print(f"Wrote {len(STOCKS) * DAYS} price rows for {len(STOCKS)} simulated stocks")


if __name__ == "__main__":
    main()
