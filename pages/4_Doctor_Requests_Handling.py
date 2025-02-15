import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
from streamlit.components.v1 import html

# Sample clinician and patient data
clinicians = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Dr. Smith", "Dr. Johnson", "Dr. Brown"],
    "registered": [True, False, True],  # Indicates if the clinician has an account
    "availability": [
        ["Monday", "Wednesday", "Friday"],
        ["Tuesday", "Thursday"],
        ["Monday", "Thursday", "Saturday"]
    ]  # Sample clinician availability
})

current_patients = pd.DataFrame({
    "patient_name": ["Alice", "Bob", "Charlie", "Daniel", "Eva"],
    "appointment_date": [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(1, 6)],
    "clinician_name": ["Dr. Smith", "Dr. Smith", "Dr. Brown", "Dr. Smith", "Dr. Brown"]
})

# Sample new patient requests
new_requests = pd.DataFrame({
    "request_id": range(6, 11),
    "patient_name": ["Frank", "Grace", "Helen", "Ivy", "Jack"],
    "age": [45, 34, 29, 50, 41],
    "gender": ["Male", "Female", "Female", "Female", "Male"],
    "symptom_severity": np.random.randint(1, 10, 5),
    "summary": [
        "Fever and cough for 3 days",
        "Headache and dizziness",
        "Chest pain and shortness of breath",
        "Fatigue and muscle weakness",
        "Abdominal pain and nausea"
    ],
    "temperature": np.random.uniform(36.0, 39.0, 5),
    "heart_rate": np.random.randint(60, 120, 5),
    "blood_pressure": ["120/80", "140/90", "110/70", "130/85", "125/78"],
    "oxygen_saturation": np.random.uniform(90, 100, 5),
    "patient_consent": [True, False, True, True, False],
    "request_date": [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(5)],
})

# Initialize session state
if "accepted_requests" not in st.session_state:
    st.session_state["accepted_requests"] = []
if "declined_requests" not in st.session_state:
    st.session_state["declined_requests"] = []

st.title("🏥 Clinician Dashboard")

# Select clinician
clinician_name = st.selectbox("Select Your Name", clinicians["name"].tolist())

# General View: Calendar and Upcoming Appointments
st.header("📆 General Overview")

# Convert patient appointments to calendar format
events = [
    {"title": row["patient_name"], "start": row["appointment_date"].strftime("%Y-%m-%dT%H:%M:%S")}
    for _, row in current_patients[current_patients["clinician_name"] == clinician_name].iterrows()
]

calendar_html = f'''
<!DOCTYPE html>
<html>
<head>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.10.2/fullcalendar.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.10.2/fullcalendar.min.js"></script>
</head>
<body>
    <div id="calendar"></div>
    <script>
        $(document).ready(function() {{
            $('#calendar').fullCalendar({{
                defaultView: 'month',
                events: {json.dumps(events)}
            }});
        }});
    </script>
</body>
</html>
'''

html(calendar_html, height=600)

# Current Patients Section
st.header("📅 Current Patients")
clinician_patients = current_patients[current_patients["clinician_name"] == clinician_name]

if clinician_patients.empty:
    st.info("No upcoming appointments.")
else:
    for _, row in clinician_patients.iterrows():
        st.write(f"**Patient:** {row['patient_name']}")
        st.write(f"**Appointment Date:** {row['appointment_date'].strftime('%Y-%m-%d %H:%M')}")
        st.divider()

# New Requested Patients Section
st.header("🆕 New Requested Patients")

pending_requests = new_requests[~new_requests["request_id"].isin(st.session_state["accepted_requests"] + st.session_state["declined_requests"])]

if pending_requests.empty:
    st.success("No pending requests at the moment.")
else:
    for _, row in pending_requests.iterrows():
        st.markdown(f"### Patient: {row['patient_name']} <span style='color:gray;'>(Requested since {row['request_date'].strftime('%Y-%m-%d %H:%M:%S')})</span>", unsafe_allow_html=True)
        st.write(f"**Age:** {row['age']} | **Gender:** {row['gender']}")
        st.write(f"**Symptom Severity:** {row['symptom_severity']} / 10")
        if row["patient_consent"]:
            with st.expander("View Full Patient Summary"):
                st.write(f"**Summary:** {row['summary']}")
                st.write(f"**Temperature:** {row['temperature']:.1f}°C")
                st.write(f"**Heart Rate:** {row['heart_rate']} BPM")
                st.write(f"**Blood Pressure:** {row['blood_pressure']}")
                st.write(f"**Oxygen Saturation:** {row['oxygen_saturation']:.1f}%")
        else:
            st.write("🔒 Patient has not consented to share full medical data. Only symptom severity is available.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✅ Accept Request - {row['patient_name']}", key=f"accept_{row['patient_name']}"):
                st.session_state["accepted_requests"].append(row['patient_name'])
                st.success(f"You have accepted {row['patient_name']}'s request.")
                st.experimental_rerun()
        with col2:
            if st.button(f"❌ Decline Request - {row['patient_name']}", key=f"decline_{row['patient_name']}"):
                st.session_state["declined_requests"].append(row['patient_name'])
                st.warning(f"You have declined {row['patient_name']}'s request.")
                st.experimental_rerun()
