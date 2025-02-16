import streamlit as st
import pandas as pd
import datetime

# Sample data of clinicians registered on the platform with their availability
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

# Streamlit App Title
st.title("📩 Send Availability & Symptoms to Your Clinician")

# Patient Name Input
# st.header("Patient Information (To Suppress)")
# patient_name = st.text_input("Your Name", "")

# Dedicated Clinician Input
st.header("Your Dedicated Clinician")
dedicated_clinician = st.text_input("Enter Your Clinician's Name", "Dr. Smith")
if 'clinician_status' not in st.session_state:
    st.session_state['clinician_status'] = None
available_days = []
selected_dates = []

if st.button("Verify Clinician"):
    st.session_state['clinician_status'] = None
    st.session_state['available_days'] = []  # Reset available days on verification
    if dedicated_clinician in clinicians["name"].values:
        clinician_row = clinicians[clinicians["name"] == dedicated_clinician]
        st.session_state['clinician_status'] = clinician_row["registered"].values[0]
        st.session_state['available_days'] = clinician_row["availability"].values[0]
        if st.session_state['clinician_status']:
            st.success(f"✅ {dedicated_clinician} is registered on the platform.")
            st.write(f"📅 **Available Days:** {', '.join(st.session_state['available_days'])}")
        else:
            st.warning(f"⚠️ {dedicated_clinician} is not registered on the platform. They will not receive your request.")
    else:
        st.error("❌ No record found for this clinician. Please check the name and try again.")

# Availability Selection
st.header("Select Your Availability (Based on Clinician's Availability)")
if 'available_days' in st.session_state and st.session_state['available_days']:
    selected_dates = st.multiselect("Choose your available days", st.session_state['available_days'])
else:
    selected_dates = []
    st.warning("Please verify your clinician to see available days.")

# Sidebar for Reporting Symptoms
# st.sidebar.header("Report Your Symptoms")
# symptom_severity = st.sidebar.slider("Rate Your Symptom Severity (1-10)", 1, 10, 5)
# symptom_description = st.sidebar.text_area("Describe Your Symptoms")

# Consent Pop-up before sending request
st.header("Data Sharing Consent")
consent = st.radio("Do you allow your clinician to access your symptom details for better diagnosis?", ["Yes", "No"], index=None)

if st.button("Send Request to Clinician"):
    if st.session_state['clinician_status'] is None:
        st.error("Please verify your clinician before sending the request.")
    elif not st.session_state['clinician_status']:
        st.error("Your selected clinician does not have an account and cannot receive your request.")
    elif not selected_dates:
        st.warning("Please select at least one available day before proceeding.")
    elif consent is None:
        st.warning("Please choose an option for data sharing before proceeding.")
    else:
        if consent == "Yes":
            st.success(f"Request sent to {dedicated_clinician}. They will receive your availability and symptom details.")
        else:
            st.info(f"Request sent to {dedicated_clinician}. They will only see your availability and symptom severity, but not your symptom details.")
