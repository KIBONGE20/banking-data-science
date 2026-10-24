
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Banking Data Science Dashboard",
    page_icon="📊",
    layout="wide"
)

# Database location: project root folder
DATABASE = Path(__file__).resolve().parent.parent / "banking_data.db"

st.title("Banking Data Science Dashboard")
st.caption("SQL-powered analytics using fictional banking transactions")

# ----------------------------------
# 1. Load records from SQLite
# ----------------------------------
try:
    with sqlite3.connect(DATABASE) as connection:
        df = pd.read_sql_query("""
            SELECT
                transaction_id AS TransactionID,
                account AS Account,
                transaction_date AS Date,
                transaction_type AS Type,
                amount AS Amount
            FROM transactions
            ORDER BY transaction_date, transaction_id
        """, connection)
except sqlite3.Error as error:
    st.error(f"Could not load the database: {error}")
    st.stop()

if df.empty:
    st.warning("The database contains no transactions.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])
df["Amount"] = pd.to_numeric(df["Amount"])

# ----------------------------------
# 2. Sidebar filters
# ----------------------------------
st.sidebar.header("Transaction Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

accounts = ["All"] + sorted(df["Account"].unique().tolist())

selected_account = st.sidebar.selectbox(
    "Account",
    accounts
)

selected_type = st.sidebar.selectbox(
    "Transaction type",
    ["All", "Deposit", "Withdrawal"]
)

search_term = st.sidebar.text_input(
    "Search transaction ID or account"
)

# ----------------------------------
# 3. Filter database results
# ----------------------------------
filtered_df = df.copy()

if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date)
            & (filtered_df["Date"].dt.date <= end_date)
        ]
    elif len(date_range) == 1:
        selected_date = date_range[0]
        filtered_df = filtered_df[
            filtered_df["Date"].dt.date == selected_date
        ]
else:
    filtered_df = filtered_df[
        filtered_df["Date"].dt.date == date_range
    ]

if selected_account != "All":
    filtered_df = filtered_df[
        filtered_df["Account"] == selected_account
    ]

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["Type"] == selected_type
    ]

if search_term.strip():
    search = search_term.strip().lower()

    matches = (
        filtered_df["TransactionID"].astype(str).str.lower().str.contains(
            search, na=False
        )
        | filtered_df["Account"].str.lower().str.contains(
            search, na=False
        )
    )

    filtered_df = filtered_df[matches]

# ----------------------------------
# 4. Calculate summary metrics
# ----------------------------------
deposits = filtered_df.loc[
    filtered_df["Type"] == "Deposit", "Amount"
].sum()

withdrawals = filtered_df.loc[
    filtered_df["Type"] == "Withdrawal", "Amount"
].sum()

net_movement = deposits - withdrawals

st.subheader("Transaction Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deposits", f"TZS {deposits:,.0f}")
col2.metric("Total Withdrawals", f"TZS {withdrawals:,.0f}")
col3.metric("Net Movement", f"TZS {net_movement:,.0f}")
col4.metric("Transactions", f"{len(filtered_df):,}")

# ----------------------------------
# 5. Interactive charts
# ----------------------------------
st.subheader("Transaction Analysis")

if filtered_df.empty:
    st.info("No transactions match your filters.")
else:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("**Deposits vs Withdrawals**")

        type_summary = (
            filtered_df.groupby("Type")["Amount"]
            .sum()
            .reindex(["Deposit", "Withdrawal"], fill_value=0)
        )

        st.bar_chart(type_summary)

    with chart_col2:
        st.write("**Transaction Amounts Over Time**")

        daily_summary = (
            filtered_df.groupby(["Date", "Type"])["Amount"]
            .sum()
            .unstack(fill_value=0)
            .reindex(columns=["Deposit", "Withdrawal"], fill_value=0)
        )

        st.line_chart(daily_summary)

# ----------------------------------
# 6. Transaction table
# ----------------------------------
st.subheader("Transaction Records")
st.write(f"Matching transactions: {len(filtered_df)}")

display_df = filtered_df.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# ----------------------------------
# 7. Download filtered CSV
# ----------------------------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download filtered transactions (CSV)",
    data=csv_data,
    file_name="banking_transactions_report.csv",
    mime="text/csv"
)

st.info(
    "Training project using fictional data. A large transaction is not "
    "automatically fraudulent. This dashboard is not validated for real "
    "banking decisions."
)
