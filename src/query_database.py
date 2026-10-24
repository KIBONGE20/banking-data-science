
import sqlite3
import pandas as pd

DATABASE = "banking_data.db"

with sqlite3.connect(DATABASE) as connection:

    # Query 1: Display all transactions
    print("\nALL TRANSACTIONS")

    all_transactions = pd.read_sql_query(
        "SELECT * FROM transactions",
        connection
    )
    print(all_transactions.to_string(index=False))

    # Query 2: Calculate deposits and withdrawals
    print("\nTOTAL AMOUNT BY TRANSACTION TYPE")

    summary = pd.read_sql_query("""
        SELECT
            transaction_type,
            COUNT(*) AS transaction_count,
            SUM(amount) AS total_amount
        FROM transactions
        GROUP BY transaction_type
    """, connection)

    print(summary.to_string(index=False))

    # Query 3: Find withdrawals of at least TZS 200,000
    print("\nWITHDRAWALS OF TZS 200,000 OR MORE")

    large_withdrawals = pd.read_sql_query("""
        SELECT
            transaction_id,
            account,
            transaction_date,
            amount
        FROM transactions
        WHERE transaction_type = 'Withdrawal'
          AND amount >= 200000
        ORDER BY amount DESC
    """, connection)

    print(large_withdrawals.to_string(index=False))
