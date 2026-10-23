
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Banking Data Science Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------
# 1. Dashboard heading
# ----------------------------------
st.title("Banking Data Science Dashboard")
st.caption(
    "Transaction analysis using fictional data for educational purposes"
)

# ----------------------------------
# 2. Fictional sample transactions
# ----------------------------------
data = {
    "TransactionID": [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008],
    "Account": [
        "A001", "A002", "A001", "A003",
        "A002", "A003", "A001", "A002"
    ],
    "Date": [
        "2026-10-01", "2026-10-02",
        "2026-10-03", "2026-10-05",
        "2026-10-08", "2026-10-10",
        "2026-10-15", "2026-10-20"
    ],
    "Type": [
        "Withdrawal", "Deposit", "Withdrawal", "Deposit",
        "Withdrawal", "Deposit", "Deposit", "Withdrawal"
    ],
    "Amount": [
        50000, 200000, 2500000, 150000,
        180000, 300000, 450000, 120000
    ]
}

df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])

# ----------------------------------
# 3. Sidebar filters
# ----------------------------------
st.sidebar.header("Transaction Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

accounts = ["All"] + sorted(df["Account"].unique().tolist())

selected_account = st.sidebar.selectbox(
    "Select account",
    accounts
)

transaction_types = ["All", "Deposit", "Withdrawal"]

selected_type = st.sidebar.selectbox(
    "Transaction type",
    transaction_types
)

search_term = st.sidebar.text_input(
    "Search transaction ID or account"
)

# ----------------------------------
# 4. Apply filters
# ----------------------------------
filtered_df = df.copy()

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

    filtered_df = filtered_df[
        filtered_df["TransactionID"].astype(str).str.lower().str.contains(
            search, na=False
        )
        | filtered_df["Account"].str.lower().str.contains(
            search, na=False
        )
    ]

# ----------------------------------
# 5. Calculate KPIs
# ----------------------------------
deposits = filtered_df.loc[
    filtered_df["Type"] == "Deposit", "Amount"
].sum()

withdrawals = filtered_df.loc[
    filtered_df["Type"] == "Withdrawal", "Amount"
].sum()

net_movement = deposits - withdrawals
transaction_count = len(filtered_df)

st.subheader("Transaction Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Deposits",
    f"TZS {deposits:,.0f}"
)

col2.metric(
    "Total Withdrawals",
    f"TZS {withdrawals:,.0f}"
)

col3.metric(
    "Net Movement",
    f"TZS {net_movement:,.0f}"
)

col4.metric(
    "Transactions",
    f"{transaction_count:,}"
)

# ----------------------------------
# 6. Charts
# ----------------------------------
st.subheader("Transaction Analysis")

if filtered_df.empty:
    st.warning("No transactions match your selected filters.")
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
# 7. Transaction records
# ----------------------------------
st.subheader("Transaction Records")

st.write(f"Showing {len(filtered_df)} matching transaction(s).")

display_df = filtered_df.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# ----------------------------------
# 8. Download filtered records
# ----------------------------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered transactions (CSV)",
    data=csv_data,
    file_name="banking_transactions_report.csv",
    mime="text/csv"
)

# ----------------------------------
# 9. Review notice
# ----------------------------------
st.info(
    "Educational demonstration only. Large transactions may warrant "
    "review, but transaction amount alone does not establish fraud. "
    "All data in this dashboard is fictional."
)
