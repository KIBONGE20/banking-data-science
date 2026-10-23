from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report

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

    # 0 = Normal, 1 = Review
    # These are invented training labels
    "Label": [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)

# Features the model will learn from
X = df[["Amount", "IsWithdrawal", "Hour"]]

# Labels the model will try to predict
y = df["Label"]

# Divide data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create and train the Decision Tree
model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

model.fit(X_train, y_train)

# Test the model on data it did not train on
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\n=== CONFUSION MATRIX ===")
print(confusion_matrix(y_test, y_pred))

print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Normal", "Review"],
    zero_division=0
))

print("=== MACHINE LEARNING RESULTS ===")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Accuracy:", round(accuracy * 100, 2), "%")

# Predict one new fictional transaction
new_transaction = pd.DataFrame({
    "Amount": [800000],
    "IsWithdrawal": [1],
    "Hour": [2]
})

prediction = model.predict(new_transaction)[0]

print("\n=== NEW TRANSACTION PREDICTION ===")

if prediction == 1:
    print("Prediction: REVIEW")
else:
    print("Prediction: Normal")
plt.figure(figsize=(12, 7))

plot_tree(
    model,
    feature_names=["Amount", "IsWithdrawal", "Hour"],
    class_names=["Normal", "Review"],
    filled=True
)

plt.title("Transaction Review Decision Tree")
plt.show()