import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os

pd.set_option('display.width', 120)
pd.set_option('display.max_columns', None)

print("Loading dataset...")
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"

columns = [
    'checking_account_status', 'duration_months', 'credit_history', 'purpose',
    'credit_amount', 'savings_account', 'present_employment_since',
    'installment_rate_pct', 'personal_status_sex', 'other_debtors',
    'present_residence_since', 'property', 'age', 'other_installment_plans',
    'housing', 'existing_credits_count', 'job', 'num_dependents',
    'telephone', 'foreign_worker', 'target'
]

df = pd.read_csv(url, sep=' ', header=None, names=columns)
df['target'] = df['target'].map({1: 0, 2: 1})  # 0 = Good, 1 = Bad

categorical_cols = df.select_dtypes(include='object').columns.tolist()
numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
numerical_cols.remove('target')

# --- Outlier capping ---
for col in ['duration_months', 'credit_amount', 'age']:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    df[col] = df[col].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)

# --- Encoding ---
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

X = df_encoded.drop('target', axis=1)
y = df_encoded['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Scaling ---
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

X_train = X_train.astype(float)
X_test = X_test.astype(float)

print("Training Logistic Regression...")
lr_grid = GridSearchCV(
    LogisticRegression(max_iter=2000, random_state=42),
    {'C': [0.01, 0.1, 1, 10, 100], 'penalty': ['l2'], 'solver': ['liblinear']},
    cv=5, scoring='roc_auc', n_jobs=-1
)
lr_grid.fit(X_train, y_train)

print("Training Random Forest...")
rf_grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    {'n_estimators': [100, 200], 'max_depth': [5, 10, None], 'min_samples_split': [2, 5]},
    cv=5, scoring='roc_auc', n_jobs=-1
)
rf_grid.fit(X_train, y_train)

# --- Evaluate both, pick the best ---
candidates = {'Logistic Regression': lr_grid.best_estimator_, 'Random Forest': rf_grid.best_estimator_}

results = []
for name, model in candidates.items():
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    results.append({
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1-Score': f1_score(y_test, y_pred),
        'ROC AUC': roc_auc_score(y_test, y_proba)
    })

results_df = pd.DataFrame(results).set_index('Model').round(4)
print("\nModel comparison:")
print(results_df)

best_model_name = results_df['ROC AUC'].idxmax()
best_model = candidates[best_model_name]
print(f"\nBest model: {best_model_name}")

os.makedirs('models', exist_ok=True)
joblib.dump(best_model, 'models/credit_risk_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(list(X_train.columns), 'models/feature_columns.pkl')
joblib.dump(numerical_cols, 'models/numerical_cols.pkl')

print("\nSaved to models/: credit_risk_model.pkl, scaler.pkl, feature_columns.pkl, numerical_cols.pkl")
print("Done.")