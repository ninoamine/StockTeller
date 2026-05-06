import sqlite3
from pathlib import Path

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
