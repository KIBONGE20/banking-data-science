
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Bank Transaction Dashboard",
    layout="wide"
)

st.title("Bank Transaction Analysis Dashboard")
st.caption("Training project using fictional transaction data")

data = {
    "TransactionID": [2001, 2002, 2003, 2004, 2005],
    "Account": ["A001", "A002", "A001", "A003", "A002"],
    "Type": [
        "Withdrawal", "Deposit", "Withdrawal",
        "Deposit", "Withdrawal"
    ],
    "Amount": [50000, 200000, 2500000, 150000, 180000]
}

df = pd.DataFrame(data)

deposits = df.loc[df["Type"] == "Deposit", "Amount"].sum()
withdrawals = df.loc[
    df["Type"] == "Withdrawal", "Amount"
].sum()
net_movement = deposits - withdrawals

col1, col2, col3 = st.columns(3)

col1.metric("Total Deposits", f"TZS {deposits:,.0f}")
col2.metric("Total Withdrawals", f"TZS {withdrawals:,.0f}")
col3.metric("Net Movement", f"TZS {net_movement:,.0f}")

st.subheader("Transactions by Type")
chart_data = df.groupby("Type")["Amount"].sum()
st.bar_chart(chart_data)

st.subheader("Transaction Records")

selected_type = st.selectbox(
    "Filter by transaction type",
    ["All", "Deposit", "Withdrawal"]
)

if selected_type == "All":
    filtered_df = df
else:
    filtered_df = df[df["Type"] == selected_type]

st.dataframe(filtered_df, use_container_width=True)

st.caption(
    "Large transactions are flagged for review, "
    "not automatically classified as fraud."
)
