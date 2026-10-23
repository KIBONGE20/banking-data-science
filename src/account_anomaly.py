
import pandas as pd

data = {
    "TransactionID": [4001, 4002, 4003, 4004, 4005, 4006, 4007],
    "Account": ["A001", "A001", "A001", "A002", "A002", "A002", "A001"],
    "Amount": [20000, 25000, 30000, 50000, 55000, 60000, 800000]
}

df = pd.DataFrame(data)

# Establish the order in which transactions occurred
df["PreviousAverage"] = (
    df.groupby("Account")["Amount"]
    .transform(lambda amounts: amounts.shift().expanding().mean())
)

# Flag a transaction if it is more than 3 times
# the average of the account's previous transactions
df["Flag"] = df.apply(
    lambda row: "REVIEW"
    if pd.notna(row["PreviousAverage"])
    and row["Amount"] > 3 * row["PreviousAverage"]
    else "Normal",
    axis=1
)

print("=== PREVIOUS-TRANSACTION ANALYSIS ===")
print(df.round(2).to_string(index=False))

print("\n=== TRANSACTIONS FOR REVIEW ===")
print(df[df["Flag"] == "REVIEW"].round(2).to_string(index=False))
