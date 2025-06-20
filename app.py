# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F-NN3__Q7zVwRDpX8MZ5wLcpOgCZ4fZZ
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from sklearn.preprocessing import LabelEncoder

# STEP 1: Load dataset
df = pd.read_csv("Creditcard.csv")

# STEP 2: Drop unnecessary column
df = df.drop(columns=["Unnamed: 18"], errors='ignore')

# STEP 3: Fill missing values and encode categorical columns
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna(df[col].mode()[0])
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    else:
        df[col] = df[col].fillna(df[col].median())

# STEP 4: Features and target
X = df.drop(columns=["label", "Ind_ID"])  # Exclude label and ID
y = df["label"]

# STEP 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# STEP 6: Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# STEP 7: Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:\n", classification_report(y_test, y_pred))
print("🧾 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# STEP 8: Save the model
joblib.dump(model, "fraud_model.pkl")
print("✅ Model saved as 'fraud_model.pkl'")

# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load("fraud_model.pkl")

# App title
st.title("💳 Credit Card Fraud Detection App")

st.markdown("Enter customer transaction details to detect fraud.")

# Input fields (example based on your dataset)
gender = st.selectbox("Gender", ["Male", "Female"])
car_owner = st.selectbox("Car Owner", ["Yes", "No"])
property_owner = st.selectbox("Property Owner", ["Yes", "No"])
income = st.number_input("Annual Income", min_value=0)
edu = st.selectbox("Education", ["Higher education", "Secondary", "Incomplete", "Academic degree"])
marital = st.selectbox("Marital Status", ["Married", "Single", "Separated", "Widow"])
housing = st.selectbox("Housing Type", ["House", "With parents", "Municipal", "Rented", "Office apartment"])
birthday = st.number_input("Birthday Count (days)", value=-10000)
employed = st.number_input("Employed Days (negative = employed)", value=-1000)
workphone = st.selectbox("Has Work Phone?", ["Yes", "No"])
phone = st.selectbox("Has Phone?", ["Yes", "No"])
email = st.selectbox("Has Email?", ["Yes", "No"])
occupation = st.selectbox("Occupation", ["Laborers", "Managers", "Sales", "Drivers", "Others"])

# Mapping input to numeric as model expects
input_data = {
    "GENDER": 0 if gender == "Male" else 1,
    "Car_Owner": 1 if car_owner == "Yes" else 0,
    "Propert_Owner": 1 if property_owner == "Yes" else 0,
    "Annual_income": income,
    "EDUCATION": {"Higher education": 0, "Secondary": 1, "Incomplete": 2, "Academic degree": 3}[edu],
    "Marital_status": {"Married": 0, "Single": 1, "Separated": 2, "Widow": 3}[marital],
    "Housing_type": {"House": 0, "With parents": 1, "Municipal": 2, "Rented": 3, "Office apartment": 4}[housing],
    "Birthday_count": birthday,
    "Employed_days": employed,
    "Work_Phone": 1 if workphone == "Yes" else 0,
    "Phone": 1 if phone == "Yes" else 0,
    "EMAIL_ID": 1 if email == "Yes" else 0,
    "Type_Occupation": {"Laborers": 0, "Managers": 1, "Sales": 2, "Drivers": 3, "Others": 4}[occupation],
}
type_income = st.selectbox("Type of Income", ["Working", "Commercial associate", "State servant", "Student", "Pensioner"])
mobile = st.selectbox("Has Mobile Phone?", ["Yes", "No"])
children = st.number_input("Number of Children", min_value=0)
family_members = st.number_input("Total Family Members", min_value=1)




# Convert to DataFrame
input_df = pd.DataFrame([input_data])

# Predict button
if st.button("🔍 Predict"):
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.error("❌ This transaction is predicted to be FRAUDULENT!")
    else:
        st.success("✅ This transaction is NOT fraudulent.")

