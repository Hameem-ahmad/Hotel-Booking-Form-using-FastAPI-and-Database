import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# If SQLSERVER_CONN is provided in .env, use SQL Server via pyodbc.
# Otherwise fall back to a local SQLite database in the `sql` folder.
SQLSERVER_CONN = os.getenv("SQLSERVER_CONN")


def init_db():
    if SQLSERVER_CONN:
        try:
            import pyodbc
        except Exception as e:
            raise RuntimeError("pyodbc is required for SQL Server connections: install pyodbc") from e

        conn = pyodbc.connect(SQLSERVER_CONN, autocommit=True)
        cur = conn.cursor()
        cur.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='bookings' and xtype='U')
        CREATE TABLE bookings (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(255),
            email NVARCHAR(255),
            room_type NVARCHAR(100),
            check_in DATE,
            check_out DATE
        )
        """)
        cur.close()
        conn.close()
        print("Initialized SQL Server database (table 'bookings').")
    else:
        import sqlite3

        DB_PATH = Path("sql") / "hotel.db"
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            room_type TEXT,
            check_in TEXT,
            check_out TEXT
        )''')
        conn.commit()
        conn.close()
        print(f"Initialized SQLite database at {DB_PATH}")


if __name__ == "__main__":
    init_db()
