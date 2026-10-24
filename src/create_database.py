
import sqlite3

DATABASE = "banking_data.db"

transactions = [
    (2001, "A001", "2026-10-01", "Withdrawal", 50000),
    (2002, "A002", "2026-10-02", "Deposit", 200000),
    (2003, "A001", "2026-10-03", "Withdrawal", 2500000),
    (2004, "A003", "2026-10-05", "Deposit", 150000),
    (2005, "A002", "2026-10-08", "Withdrawal", 180000),
    (2006, "A003", "2026-10-10", "Deposit", 300000),
    (2007, "A001", "2026-10-15", "Deposit", 450000),
    (2008, "A002", "2026-10-20", "Withdrawal", 120000),
]

with sqlite3.connect(DATABASE) as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            account TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount >= 0)
        )
    """)

    connection.executemany("""
        INSERT OR IGNORE INTO transactions
        (transaction_id, account, transaction_date,
         transaction_type, amount)
        VALUES (?, ?, ?, ?, ?)
    """, transactions)

print(f"Database created: {DATABASE}")
print(f"Sample transactions processed: {len(transactions)}")
