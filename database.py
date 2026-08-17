import sqlite3
from datetime import datetime

DB_NAME = "credit_risk.db"


def init_db():
    """Create the Borrowers table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Borrowers (
            BorrowerID INTEGER PRIMARY KEY AUTOINCREMENT,
            Age INTEGER,
            EmploymentStatus VARCHAR(100),
            LoanAmount DECIMAL,
            LoanDuration INTEGER,
            CreditHistory VARCHAR(100),
            SavingsStatus VARCHAR(100),
            HousingStatus VARCHAR(100),
            ExistingDebts INTEGER,
            RiskCategory VARCHAR(50),
            RiskScore DECIMAL,
            Recommendation VARCHAR(50),
            DateAssessed TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(record: dict):
    """Insert one borrower assessment record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Borrowers (
            Age, EmploymentStatus, LoanAmount, LoanDuration, CreditHistory,
            SavingsStatus, HousingStatus, ExistingDebts,
            RiskCategory, RiskScore, Recommendation, DateAssessed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record['age'], record['employment_status'], record['loan_amount'],
        record['loan_duration'], record['credit_history'], record['savings_status'],
        record['housing_status'], record['existing_debts'],
        record['risk_category'], record['risk_score'], record['recommendation'],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def get_all_predictions():
    """Retrieve all stored borrower records, most recent first."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Borrowers ORDER BY BorrowerID DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return columns, rows


if __name__ == "__main__":
    init_db()
    print(f"Database '{DB_NAME}' initialized with Borrowers table.")