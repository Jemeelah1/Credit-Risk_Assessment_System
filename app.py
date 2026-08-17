# import streamlit as st
# import pandas as pd
# import joblib
# from database import init_db, save_prediction, get_all_predictions

# # --- Load trained model artifacts ---
# model = joblib.load('models/credit_risk_model.pkl')
# scaler = joblib.load('models/scaler.pkl')
# feature_columns = joblib.load('models/feature_columns.pkl')
# numerical_cols = joblib.load('models/numerical_cols.pkl')
# col_icon, col_title = st.columns([0.10, 0.92], vertical_alignment="top")

# init_db()

# st.set_page_config(page_title="AI Credit Risk Assessment", layout="centered")
# with col_icon:
#     st.image("assets/shield.png", width=75)

# with col_title:
#     st.markdown(
#         "<h2 style='margin:0; padding:0; font-weight:700; white-space:nowrap;'>Credit Risk Assessment System</h2>", 
#         unsafe_allow_html=True
#     )
#     st.caption("AI-Based Decision Support Tool for Digital Banking")

# # --- UCI dataset code mappings ---
# CHECKING_ACCOUNT = {
#     "Negative balance / overdrawn": "A11",
#     "₦0 - ₦50,000": "A12",
#     "₦50,001 or more / salary assigned": "A13",
#     "No checking account": "A14"
# }

# CREDIT_HISTORY = {
#     "No credits taken / all paid duly": "A30",
#     "All credits at this bank paid duly": "A31",
#     "Existing credits paid till now": "A32",
#     "Delay in paying in the past": "A33",
#     "Critical account / other credits elsewhere": "A34"
# }

# PURPOSE = {
#     "New car": "A40", "Used car": "A41", "Furniture/equipment": "A42",
#     "Radio/TV": "A43", "Domestic appliances": "A44", "Repairs": "A45",
#     "Education": "A46", "Retraining": "A48", "Business": "A49", "Other": "A410"
# }

# SAVINGS = {
#     "₦0 - ₦25,000": "A61",
#     "₦25,001 - ₦125,000": "A62",
#     "₦125,001 - ₦250,000": "A63",
#     "₦250,001 or more": "A64",
#     "Unknown / no savings account": "A65"
# }

# EMPLOYMENT_SINCE = {
#     "Unemployed": "A71", "Less than 1 year": "A72", "1 to 4 years": "A73",
#     "4 to 7 years": "A74", "7 years or more": "A75"
# }

# GENDER_STATUS_MAP = {
#     ("Male", "Single"): "A93",
#     ("Male", "Married"): "A94",
#     ("Male", "Widowed"): "A94",
#     ("Male", "Divorced/Separated"): "A91",
#     ("Female", "Single"): "A95",
#     ("Female", "Married"): "A92",   
#     ("Female", "Divorced/Separated"): "A92",
#     ("Female", "Widowed"): "A92", 
# }

# OTHER_DEBTORS = {"None": "A101", "Co-applicant": "A102", "Guarantor": "A103"}

# PROPERTY = {
#     "Real estate": "A121", "Building society savings / life insurance": "A122",
#     "Car or other property": "A123", "No property / unknown": "A124"
# }

# OTHER_INSTALLMENT_PLANS = {"Bank": "A141", "Stores": "A142", "None": "A143"}

# HOUSING = {"Rent": "A151", "Own": "A152", "Provided for free": "A153"}

# # --- Realistic Nigerian job titles, mapped to the 4 skill-level buckets
# # the model actually understands (that's all the UCI dataset has). ---
# JOB = {
#     # A171: Unemployed / unskilled - non-resident
#     "Unemployed": "A171",

#     # A172: Unskilled - resident
#     "Petty trader / Hawker": "A172",
#     "Okada/Bike or Taxi Rider": "A172",
#     "Domestic Staff / Cleaner": "A172",
#     "Security Guard": "A172",
#     "Student": "A172",
#     "Apprentice": "A172",

#     # A173: Skilled employee / official
#     "Artisan (Tailor, Electrician, Plumber, etc.)": "A173",
#     "Civil Servant (Junior/Mid-level)": "A173",
#     "Teacher": "A173",
#     "Nurse": "A173",
#     "Bank/Office Staff": "A173",
#     "Police / Military (Junior ranks)": "A173",

#     # A174: Management / self-employed / highly qualified
#     "Business Owner / Entrepreneur": "A174",
#     "Doctor": "A174",
#     "Engineer": "A174",
#     "Lawyer": "A174",
#     "Accountant": "A174",
#     "Senior Civil Servant / Government Official": "A174",
#     "Company Executive / Manager": "A174",
# }

# TELEPHONE = {"No": "A191", "Yes": "A192"}
# FOREIGN_WORKER = {"Yes": "A201", "No": "A202"}

# st.header("Borrower Information")

# col1, col2 = st.columns(2)

# with col1:
#     age = st.number_input("Age", min_value=18, max_value=100, value=30)

#     gender = st.selectbox("Gender", ["Male", "Female"])
#     marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced/Separated", "Widowed"])

#     employment_status = st.selectbox("Employment Status (years employed)", list(EMPLOYMENT_SINCE.keys()))
#     job = st.selectbox("Job / Occupation", list(JOB.keys()))
#     credit_history = st.selectbox("Credit History", list(CREDIT_HISTORY.keys()))

#     NAIRA_SCALE_FACTOR = 250

#     loan_amount_naira = st.number_input(
#         "Loan Amount (₦)", min_value=50000, max_value=2000000, value=500000, step=10000
#     )
#     loan_amount = loan_amount_naira / NAIRA_SCALE_FACTOR

#     loan_duration = st.number_input("Loan Duration (months)", min_value=4, max_value=72, value=12)

# with col2:
#     savings_status = st.selectbox("Savings Account Status", list(SAVINGS.keys()))
#     housing_status = st.selectbox("Housing Status", list(HOUSING.keys()))

#     existing_debts_selected = st.selectbox("Existing Credits at This Bank", [0, 1, 2, 3, 4], index=1)
#     existing_debts = max(1, existing_debts_selected)

#     checking_status = st.selectbox("Checking Account Status", list(CHECKING_ACCOUNT.keys()))
#     purpose = st.selectbox("Loan Purpose", list(PURPOSE.keys()))
#     other_debtors = st.selectbox("Other Debtors / Guarantors", list(OTHER_DEBTORS.keys()))
#     property_status = st.selectbox("Property", list(PROPERTY.keys()))
#     other_installment = st.selectbox("Other Installment Plans", list(OTHER_INSTALLMENT_PLANS.keys()))
    
# telephone = st.selectbox("Has Telephone", list(TELEPHONE.keys()))
# foreign_worker = st.selectbox("Foreign Worker", list(FOREIGN_WORKER.keys()))
# installment_rate = st.slider("Installment Rate (% of disposable income)", 1, 4, 2)
# present_residence = st.slider("Years at Present Residence", 1, 4, 2)
# num_dependents = st.selectbox("Number of Dependents", [1, 2])

# if st.button("Assess Credit Risk", type="primary"):

#     personal_status_sex_code = GENDER_STATUS_MAP[(gender, marital_status)]

#     raw_input = pd.DataFrame([{
#         'checking_account_status': CHECKING_ACCOUNT[checking_status],
#         'duration_months': loan_duration,
#         'credit_history': CREDIT_HISTORY[credit_history],
#         'purpose': PURPOSE[purpose],
#         'credit_amount': loan_amount,
#         'savings_account': SAVINGS[savings_status],
#         'present_employment_since': EMPLOYMENT_SINCE[employment_status],
#         'installment_rate_pct': installment_rate,
#         'personal_status_sex': personal_status_sex_code,
#         'other_debtors': OTHER_DEBTORS[other_debtors],
#         'present_residence_since': present_residence,
#         'property': PROPERTY[property_status],
#         'age': age,
#         'other_installment_plans': OTHER_INSTALLMENT_PLANS[other_installment],
#         'housing': HOUSING[housing_status],
#         'existing_credits_count': existing_debts,
#         'job': JOB[job],
#         'num_dependents': num_dependents,
#         'telephone': TELEPHONE[telephone],
#         'foreign_worker': FOREIGN_WORKER[foreign_worker],
#     }])

#     # One-hot encode
#     encoded = pd.get_dummies(raw_input)
#     encoded = encoded.reindex(columns=feature_columns, fill_value=0)

#     # Scale numeric columns
#     encoded[numerical_cols] = scaler.transform(encoded[numerical_cols])
#     encoded = encoded.astype(float)

#     # Predict
#     risk_proba = model.predict_proba(encoded)[0][1]
#     prediction = model.predict(encoded)[0]

#     risk_category = "Bad Risk" if prediction == 1 else "Good Risk"
#     recommendation = "Reject Loan" if prediction == 1 else "Approve Loan"

#     st.divider()
#     st.header("Assessment Result")

#     if prediction == 1:
#         st.error(f"⚠️ Risk Category: **{risk_category}**")
#     else:
#         st.success(f"✅ Risk Category: **{risk_category}**")

#     st.metric("Risk Score (probability of default)", f"{risk_proba:.1%}")
#     st.write(f"**Loan Amount Requested:** ₦{loan_amount_naira:,.0f}")
#     st.write(f"**Recommendation:** {recommendation}")

#     # Save to database
#     save_prediction({
#         'age': age,
#         'employment_status': employment_status,
#         'loan_amount': loan_amount_naira,
#         'loan_duration': loan_duration,
#         'credit_history': credit_history,
#         'savings_status': savings_status,
#         'housing_status': housing_status,
#         'existing_debts': existing_debts_selected,
#         'risk_category': risk_category,
#         'risk_score': round(risk_proba, 4),
#         'recommendation': recommendation
#     })
#     st.info("This assessment has been saved to the database.")

# # --- View past assessments ---
# st.divider()
# if st.checkbox("View Past Assessments"):
#     columns, rows = get_all_predictions()
#     if rows:
#         history_df = pd.DataFrame(rows, columns=columns)
#         st.dataframe(history_df, use_container_width=True)
#     else:
#         st.write("No assessments recorded yet.")

import streamlit as st
import pandas as pd
import joblib
import base64
from database import init_db, save_prediction, get_all_predictions

# --- Load trained model artifacts ---
model = joblib.load('models/credit_risk_model.pkl')
scaler = joblib.load('models/scaler.pkl')
feature_columns = joblib.load('models/feature_columns.pkl')
numerical_cols = joblib.load('models/numerical_cols.pkl')

init_db()

st.set_page_config(page_title="AI Credit Risk Assessment", layout="centered")

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

shield_base64 = get_base64_image("assets/shield.png")

col_icon, col_title = st.columns([0.10, 0.92], vertical_alignment="top")

with col_icon:
    st.markdown(f"""
    <style>
    @keyframes breatheGlow {{
        0%   {{ transform: scale(1) rotate(0deg);    filter: drop-shadow(0 0 0px rgba(34,197,94,0)); }}
        20%  {{ transform: scale(1.08) rotate(0deg);  filter: drop-shadow(0 0 10px rgba(34,197,94,0.6)); }}
        40%  {{ transform: scale(1) rotate(0deg);    filter: drop-shadow(0 0 0px rgba(34,197,94,0)); }}
        60%  {{ transform: scale(1.08) rotate(0deg);  filter: drop-shadow(0 0 10px rgba(34,197,94,0.6)); }}
        80%  {{ transform: scale(1) rotate(0deg);    filter: drop-shadow(0 0 0px rgba(34,197,94,0)); }}
        100% {{ transform: scale(1) rotate(360deg);  filter: drop-shadow(0 0 8px rgba(34,197,94,0.5)); }}
    }}
    @keyframes glowPulse {{
        0%, 100% {{ filter: drop-shadow(0 0 4px rgba(34,197,94,0.3)); }}
        50%      {{ filter: drop-shadow(0 0 12px rgba(34,197,94,0.7)); }}
    }}
    .spinning-icon {{
        width: 75px;
        animation: breatheGlow 10s ease-in-out 1 forwards,
                   glowPulse 2.5s ease-in-out infinite 10s;
    }}
    </style>
    <img src="data:image/png;base64,{shield_base64}" class="spinning-icon">
    """, unsafe_allow_html=True)

with col_title:
    st.markdown(
        "<h2 style='margin:0; padding:0; font-weight:700; white-space:nowrap;'>Credit Risk Assessment System</h2>", 
        unsafe_allow_html=True
    )
    st.caption("AI-Based Decision Support Tool for Digital Banking")

# --- UCI dataset code mappings ---
CHECKING_ACCOUNT = {
    "Negative balance / overdrawn": "A11",
    "₦0 - ₦50,000": "A12",
    "₦50,001 or more / salary assigned": "A13",
    "No checking account": "A14"
}

CREDIT_HISTORY = {
    "No credits taken / all paid duly": "A30",
    "All credits at this bank paid duly": "A31",
    "Existing credits paid till now": "A32",
    "Delay in paying in the past": "A33",
    "Critical account / other credits elsewhere": "A34"
}

PURPOSE = {
    "New car": "A40", "Used car": "A41", "Furniture/equipment": "A42",
    "Radio/TV": "A43", "Domestic appliances": "A44", "Repairs": "A45",
    "Education": "A46", "Retraining": "A48", "Business": "A49", "Other": "A410"
}

SAVINGS = {
    "₦0 - ₦25,000": "A61",
    "₦25,001 - ₦125,000": "A62",
    "₦125,001 - ₦250,000": "A63",
    "₦250,001 or more": "A64",
    "Unknown / no savings account": "A65"
}

EMPLOYMENT_SINCE = {
    "Unemployed": "A71", "Less than 1 year": "A72", "1 to 4 years": "A73",
    "4 to 7 years": "A74", "7 years or more": "A75"
}

GENDER_STATUS_MAP = {
    ("Male", "Single"): "A93",
    ("Male", "Married"): "A94",
    ("Male", "Widowed"): "A94",
    ("Male", "Divorced/Separated"): "A91",
    ("Female", "Single"): "A95",
    ("Female", "Married"): "A92",   
    ("Female", "Divorced/Separated"): "A92",
    ("Female", "Widowed"): "A92", 
}

OTHER_DEBTORS = {"None": "A101", "Co-applicant": "A102", "Guarantor": "A103"}

PROPERTY = {
    "Real estate": "A121", "Building society savings / life insurance": "A122",
    "Car or other property": "A123", "No property / unknown": "A124"
}

OTHER_INSTALLMENT_PLANS = {"Bank": "A141", "Stores": "A142", "None": "A143"}

HOUSING = {"Rent": "A151", "Own": "A152", "Provided for free": "A153"}

# --- Realistic Nigerian job titles, mapped to the 4 skill-level buckets
# the model actually understands (that's all the UCI dataset has). ---
JOB = {
    # A171: Unemployed / unskilled - non-resident
    "Unemployed": "A171",

    # A172: Unskilled - resident
    "Petty trader / Hawker": "A172",
    "Okada/Bike or Taxi Rider": "A172",
    "Domestic Staff / Cleaner": "A172",
    "Security Guard": "A172",
    "Student": "A172",
    "Apprentice": "A172",

    # A173: Skilled employee / official
    "Artisan (Tailor, Electrician, Plumber, etc.)": "A173",
    "Civil Servant (Junior/Mid-level)": "A173",
    "Teacher": "A173",
    "Nurse": "A173",
    "Bank/Office Staff": "A173",
    "Police / Military (Junior ranks)": "A173",

    # A174: Management / self-employed / highly qualified
    "Business Owner / Entrepreneur": "A174",
    "Doctor": "A174",
    "Engineer": "A174",
    "Lawyer": "A174",
    "Accountant": "A174",
    "Senior Civil Servant / Government Official": "A174",
    "Company Executive / Manager": "A174",
}

TELEPHONE = {"No": "A191", "Yes": "A192"}
FOREIGN_WORKER = {"Yes": "A201", "No": "A202"}

st.markdown("""
<style>
div.stButton > button[kind="primary"] {
    background-color: #4A9B6E;
    border-color: #4A9B6E;
    color: white;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #3E8259;
    border-color: #3E8259;
    color: white;
}
div.stButton > button[kind="primary"]:active {
    background-color: #336B49;
    border-color: #336B49;
    color: white;
}

/* Focus outline on inputs, selects, number inputs */
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stNumberInput"] > div:focus-within,
div[data-testid="stNumberInput"] [data-baseweb="base-input"]:focus-within {
    border-color: #4A9B6E !important;
    box-shadow: 0 0 0 1px #4A9B6E !important;
}

div[data-testid="stNumberInput"] input:focus {
    outline: none !important;
}

/* --- Number Input (+ and -) Buttons --- */
/* Default state: keep buttons and icons white */
div[data-testid="stNumberInput"] button,
div[data-testid="stNumberInput"] button * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    border-color: transparent !important;
}

div[data-testid="stNumberInput"] button:hover,
div[data-testid="stNumberInput"] button:focus,
div[data-testid="stNumberInput"] button:active,
div[data-testid="stNumberInput"] button:focus-visible {
    background-color: rgba(255, 255, 255, 0.1) !important;
    box-shadow: none !important;
    outline: none !important;
    border-color: transparent !important;
}

div[data-testid="stNumberInput"] button:hover svg,
div[data-testid="stNumberInput"] button:focus svg,
div[data-testid="stNumberInput"] button:active svg {
    fill: #FFFFFF !important;
}

/* Checkbox accent color */
input[type="checkbox"] {
    accent-color: #4A9B6E;
}

/* Slider track/thumb */
# div[data-baseweb="slider"] div[role="slider"] {
#     background-color: #4A9B6E !important;
#     border-color: #4A9B6E !important;
# }
</style>
""", unsafe_allow_html=True)

st.header("Borrower Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=30)

    gender = st.selectbox("Gender", ["Male", "Female"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced/Separated", "Widowed"])

    employment_status = st.selectbox("Employment Status (years employed)", list(EMPLOYMENT_SINCE.keys()))
    job = st.selectbox("Job / Occupation", list(JOB.keys()))
    credit_history = st.selectbox("Credit History", list(CREDIT_HISTORY.keys()))

    NAIRA_SCALE_FACTOR = 250

    loan_amount_naira = st.number_input(
        "Loan Amount (₦)", min_value=50000, max_value=2000000, value=500000, step=10000
    )
    loan_amount = loan_amount_naira / NAIRA_SCALE_FACTOR

    loan_duration = st.number_input("Loan Duration (months)", min_value=4, max_value=72, value=12)

with col2:
    savings_status = st.selectbox("Savings Account Status", list(SAVINGS.keys()))
    housing_status = st.selectbox("Housing Status", list(HOUSING.keys()))

    existing_debts_selected = st.selectbox("Existing Credits at This Bank", [0, 1, 2, 3, 4], index=1)
    existing_debts = max(1, existing_debts_selected)

    checking_status = st.selectbox("Checking Account Status", list(CHECKING_ACCOUNT.keys()))
    purpose = st.selectbox("Loan Purpose", list(PURPOSE.keys()))
    other_debtors = st.selectbox("Other Debtors / Guarantors", list(OTHER_DEBTORS.keys()))
    property_status = st.selectbox("Property", list(PROPERTY.keys()))
    other_installment = st.selectbox("Other Installment Plans", list(OTHER_INSTALLMENT_PLANS.keys()))
    
telephone = st.selectbox("Has Telephone", list(TELEPHONE.keys()))
foreign_worker = st.selectbox("Foreign Worker", list(FOREIGN_WORKER.keys()))
installment_rate = st.slider("Installment Rate (% of disposable income)", 1, 4, 2)
present_residence = st.slider("Years at Present Residence", 1, 4, 2)
num_dependents = st.selectbox("Number of Dependents", [1, 2])

if st.button("Assess Credit Risk", type="primary"):

    personal_status_sex_code = GENDER_STATUS_MAP[(gender, marital_status)]

    raw_input = pd.DataFrame([{
        'checking_account_status': CHECKING_ACCOUNT[checking_status],
        'duration_months': loan_duration,
        'credit_history': CREDIT_HISTORY[credit_history],
        'purpose': PURPOSE[purpose],
        'credit_amount': loan_amount,
        'savings_account': SAVINGS[savings_status],
        'present_employment_since': EMPLOYMENT_SINCE[employment_status],
        'installment_rate_pct': installment_rate,
        'personal_status_sex': personal_status_sex_code,
        'other_debtors': OTHER_DEBTORS[other_debtors],
        'present_residence_since': present_residence,
        'property': PROPERTY[property_status],
        'age': age,
        'other_installment_plans': OTHER_INSTALLMENT_PLANS[other_installment],
        'housing': HOUSING[housing_status],
        'existing_credits_count': existing_debts,
        'job': JOB[job],
        'num_dependents': num_dependents,
        'telephone': TELEPHONE[telephone],
        'foreign_worker': FOREIGN_WORKER[foreign_worker],
    }])

    # One-hot encode
    encoded = pd.get_dummies(raw_input)
    encoded = encoded.reindex(columns=feature_columns, fill_value=0)

    # Scale numeric columns
    encoded[numerical_cols] = scaler.transform(encoded[numerical_cols])
    encoded = encoded.astype(float)

    # Predict
    risk_proba = model.predict_proba(encoded)[0][1]
    prediction = model.predict(encoded)[0]

    risk_category = "Bad Risk" if prediction == 1 else "Good Risk"
    recommendation = "Reject Loan" if prediction == 1 else "Approve Loan"

    st.divider()
    st.header("Assessment Result")

    if prediction == 1:
        st.error(f"⚠️ Risk Category: **{risk_category}**")
    else:
        st.success(f"✅ Risk Category: **{risk_category}**")

    st.metric("Risk Score (probability of default)", f"{risk_proba:.1%}")
    st.write(f"**Loan Amount Requested:** ₦{loan_amount_naira:,.0f}")
    st.write(f"**Recommendation:** {recommendation}")

    # Save to database
    save_prediction({
        'age': age,
        'employment_status': employment_status,
        'loan_amount': loan_amount_naira,
        'loan_duration': loan_duration,
        'credit_history': credit_history,
        'savings_status': savings_status,
        'housing_status': housing_status,
        'existing_debts': existing_debts_selected,
        'risk_category': risk_category,
        'risk_score': round(risk_proba, 4),
        'recommendation': recommendation
    })
    st.info("This assessment has been saved to the database.")

# --- View past assessments ---
st.divider()
if st.checkbox("View Past Assessments"):
    columns, rows = get_all_predictions()
    if rows:
        history_df = pd.DataFrame(rows, columns=columns)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.write("No assessments recorded yet.")