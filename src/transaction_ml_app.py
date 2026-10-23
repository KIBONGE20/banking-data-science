
import pandas as pd
import streamlit as st

from sklearn.tree import DecisionTreeClassifier

st.set_page_config(
    page_title="Transaction ML Demo",
    layout="centered"
)

st.title("Transaction ML Demo")
st.caption("Training project using fictional data only")

# Fictional training data
data = {
    "Amount": [
        10000, 20000, 30000, 50000, 60000,
        15000, 25000, 40000, 70000, 90000,
        250000, 400000, 600000, 800000, 1000000,
        300000, 500000, 750000, 900000, 1200000
    ],
    "IsWithdrawal": [
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0
    ],
    "Hour": [
        10, 11, 14, 15, 12,
        9, 10, 13, 14, 16,
        2, 3, 1, 2, 4,
        10, 11, 12, 13, 15
    ],
    "Label": [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)

X = df[["Amount", "IsWithdrawal", "Hour"]]
y = df["Label"]

# Train the model using all fictional examples
model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)
model.fit(X, y)

st.subheader("Enter a transaction")

amount = st.number_input(
    "Transaction amount (TZS)",
    min_value=0,
    value=800000,
    step=10000
)

transaction_type = st.selectbox(
    "Transaction type",
    ["Withdrawal", "Deposit"]
)

hour = st.slider(
    "Transaction hour",
    min_value=0,
    max_value=23,
    value=2
)

if st.button("Analyze transaction"):
    is_withdrawal = 1 if transaction_type == "Withdrawal" else 0

    new_transaction = pd.DataFrame({
        "Amount": [amount],
        "IsWithdrawal": [is_withdrawal],
        "Hour": [hour]
    })

    prediction = model.predict(new_transaction)[0]

    st.subheader("Model result")

    if prediction == 1:
        st.warning("Prediction: REVIEW")
    else:
        st.success("Prediction: Normal")

    st.caption(
        "This is an educational prediction using a small "
        "fictional dataset. It does not establish fraud."
    )
