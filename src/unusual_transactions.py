
import pandas as pd

# Fictional banking transactions
data = {
    "TransactionID": [3001, 3002, 3003, 3004, 3005, 3006],
    "Account": ["A001", "A002", "A001", "A003", "A002", "A004"],
    "Type": [
        "Deposit", "Withdrawal", "Withdrawal",
        "Deposit", "Withdrawal", "Deposit"
    ],
    "Amount": [100000, 50000, 2500000, 150000, 180000, 500000]
}

df = pd.DataFrame(data)

# Define a simple review threshold
threshold = 200000

# Flag transactions at or above the threshold
df["Flag"] = df.apply(
    lambda row: "REVIEW"
    if row["Type"] == "Withdrawal"
    and row["Amount"] >= threshold
    else "Normal",
    axis=1
)
print("=== TRANSACTION MONITORING REPORT ===")
print(df.to_string(index=False))

# Show transactions flagged for review
flagged = df[df["Flag"] == "REVIEW"]

print("\n=== TRANSACTIONS REQUIRING REVIEW ===")
print(flagged.to_string(index=False))

print(f"\nTotal transactions: {len(df)}")
print(f"Transactions flagged: {len(flagged)}")
