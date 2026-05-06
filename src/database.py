import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "stocks.db"


def init_db():
    """Create the stocks database and the daily_prices table if they don't exist."""
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_prices (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker     TEXT    NOT NULL,
            company    TEXT    NOT NULL,
            sector     TEXT,
            price      REAL    NOT NULL,
            change_1d  REAL,
            ytd        REAL,
            market_cap REAL,
            date       TEXT    NOT NULL,
            UNIQUE(ticker, date)
        )
    """)
    conn.commit()
    return conn


def insert_daily_prices(df: pd.DataFrame) -> None:
    """Insert a DataFrame of daily prices into the database.

    Uses parameterized queries to prevent SQL injection.
    Duplicate (ticker, date) rows are silently ignored.
    """
    columns = ["ticker", "company", "sector", "price",
               "change_1d", "ytd", "market_cap", "date"]
    records = list(df[columns].itertuples(index=False, name=None))

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executemany("""
            INSERT OR IGNORE INTO daily_prices
                (ticker, company, sector, price, change_1d, ytd, market_cap, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, records)
        conn.commit()
    finally:
        conn.close()