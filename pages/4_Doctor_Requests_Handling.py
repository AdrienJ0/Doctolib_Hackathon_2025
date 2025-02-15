import streamlit as st
import pandas as pd
import numpy as np
import random

# Sample incoming patient requests
requests = pd.DataFrame({
    "request_id": range(1, 6),
    "patient_name": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "symptom_severity": np.random.randint(1, 10, 5),
    "summary": [
        "Fever and cough for 3 days",
        "Headache and dizziness",
        "Chest pain and shortness of breath",
        "Fatigue and muscle weakness",
        "Abdominal pain and nausea"
    ],
    "temperature": np.random.uniform(36, 39, 5),
    "heart_rate": np.random.randint(60, 120, 5),
    "blood_pressure": ["120/80", "140/90", "110/70", "130/85", "125/78"],
    "oxygen_saturation": np.random.uniform(90, 100, 5),
    "patient_consent": [True, False, True, True, False]
})

st.title("🏥 Clinician Request Dashboard")
st.write("Review incoming patient requests and choose whether to accept or decline.")

for _, row in requests.iterrows():
    st.subheader(f"Patient: {row['patient_name']}")
    st.write(f"**Symptom Severity:** {row['symptom_severity']} / 10")
    
    if row["patient_consent"]:
        with st.expander("View Patient Summary & Vital Signs"):
            st.write(f"**Summary:** {row['summary']}")
            st.write(f"**Temperature:** {row['temperature']:.1f}°C")
            st.write(f"**Heart Rate:** {row['heart_rate']} BPM")
            st.write(f"**Blood Pressure:** {row['blood_pressure']}")
            st.write(f"**Oxygen Saturation:** {row['oxygen_saturation']:.1f}%")
            st.progress(row['symptom_severity'] / 10)
    else:
        st.write("🔒 Patient did not consent to share detailed medical data.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"✅ Accept Request - {row['patient_name']}", key=f"accept_{row['request_id']}"):
            st.success(f"You have accepted {row['patient_name']}'s request.")
    with col2:
        if st.button(f"❌ Decline Request - {row['patient_name']}", key=f"decline_{row['request_id']}"):
            st.warning(f"You have declined {row['patient_name']}'s request.")
