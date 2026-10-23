\# Banking Data Science and Machine Learning



\## Overview

A Python-based banking analytics project that demonstrates transaction analysis, unusual withdrawal detection, account-level anomaly detection, and basic machine learning using fictional banking data.



\## Features

\- \*\*Transaction Analysis:\*\* Summarizes deposits, withdrawals, and net movement.

\- \*\*Banking Dashboard:\*\* Displays transaction summaries and visualizations using Streamlit.

\- \*\*Unusual Withdrawal Detection:\*\* Flags withdrawals that meet a configurable amount threshold.

\- \*\*Account Anomaly Detection:\*\* Compares withdrawals against an account's previous transaction history.

\- \*\*Machine Learning:\*\* Demonstrates a Decision Tree classifier using an educational synthetic dataset.

\- \*\*Interactive Prediction App:\*\* Allows users to enter transaction details and view a sample model prediction.



\## Technologies

\- Python

\- Pandas

\- Matplotlib

\- Scikit-learn

\- Streamlit



\## Project Structure

```text

banking-data-science/

├── reports/

├── src/

│   ├── account\_anomaly.py

│   ├── bank\_analysis.py

│   ├── bank\_dashboard.py

│   ├── transaction\_ml.py

│   ├── transaction\_ml\_app.py

│   └── unusual\_transactions.py

├── .gitignore

├── README.md

└── requirements.txt

```



\## Installation

Install Python, then install the required libraries:



```bash

pip install -r requirements.txt

```



\## Running the Applications

Run these commands from the project root directory.



Banking dashboard:

```bash

python -m streamlit run src/bank\_dashboard.py

```



Machine learning prediction app:

```bash

python -m streamlit run src/transaction\_ml\_app.py

```



Run transaction analysis:

```bash

python src/bank\_analysis.py

```



Run unusual withdrawal detection:

```bash

python src/unusual\_transactions.py

```



Run account anomaly detection:

```bash

python src/account\_anomaly.py

```



Run the machine learning example:

```bash

python src/transaction\_ml.py

```



\## Important Note

This project uses fictional data for educational purposes. The machine-learning model is a demonstration, not a validated fraud-detection system, and must not be used to make real banking decisions.



\## Author

Dorcas Kivuyo



Computer Science Graduate | Banking ICT | Data Science and Machine Learning



