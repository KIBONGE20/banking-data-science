
import pandas as pd

# Fictional banking transactions
transactions = {
    "TransactionID": [2001, 2002, 2003, 2004, 2005],
    "Account": ["A001", "A002", "A001", "A003", "A002"],
    "Type": [
        "Withdrawal",
        "Deposit",
        "Withdrawal",
        "Deposit",
        "Withdrawal"
    ],
    "Amount": [50000, 200000, 2500000, 150000, 180000]
}

df = pd.DataFrame(transactions)

# Calculate totals
total_deposits = df.loc[
    df["Type"] == "Deposit", "Amount"
].sum()

total_withdrawals = df.loc[
    df["Type"] == "Withdrawal", "Amount"
].sum()

net_movement = total_deposits - total_withdrawals

# Identify large withdrawals
large_withdrawals = df.loc[
    (df["Type"] == "Withdrawal") &
    (df["Amount"] >= 100000)
]

# Display results
print("=== BANK TRANSACTION REPORT ===")
print("Total deposits:", total_deposits)
print("Total withdrawals:", total_withdrawals)
print("Net movement:", net_movement)

print("\nTransactions by type:")
print(df["Type"].value_counts())

print("\nLarge withdrawals for review:")
print(large_withdrawals)

# Export reports to Excel
with pd.ExcelWriter(
    "C:/Users/HP/bank_analysis_report.xlsx",
    engine="openpyxl"
) as writer:
    df.to_excel(writer, sheet_name="Transactions", index=False)
    large_withdrawals.to_excel(
        writer, sheet_name="Large Withdrawals", index=False
    )

    summary = pd.DataFrame({
        "Metric": [
            "Total Deposits",
            "Total Withdrawals",
            "Net Movement"
        ],
        "Amount_TZS": [
            total_deposits,
            total_withdrawals,
            net_movement
        ]
    })

    summary.to_excel(writer, sheet_name="Summary", index=False)

print("\nExcel report saved successfully.")
