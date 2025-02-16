import streamlit as st
import pandas as pd
import datetime

# Sample data of clinicians registered on the platform with their availability
# 'clinicians' DataFrame contains clinician information such as their name, registration status, and availability
clinicians = pd.DataFrame({
    "id": [1, 2, 3],  # Clinician IDs
    "name": ["Dr. Smith", "Dr. Johnson", "Dr. Brown"],  # Clinician names
    "registered": [True, False, True],  # Indicates if the clinician has an account (True/False)
    "availability": [
        ["Monday", "Wednesday", "Friday"],  # Available days for Dr. Smith
        ["Tuesday", "Thursday"],  # Available days for Dr. Johnson
        ["Monday", "Thursday", "Saturday"]  # Available days for Dr. Brown
    ]  # Clinician availability (days of the week)
})

# Streamlit App Title
st.title("📩 Send Availability & Symptoms to Your Clinician")

# Dedicate Clinician Input Section
st.header("Your Dedicated Clinician")
dedicated_clinician = st.text_input("Enter Your Clinician's Name", "Dr. Smith")  # Input for clinician's name

# Initialize session state to track clinician verification status and available days
if 'clinician_status' not in st.session_state:
    st.session_state['clinician_status'] = None
available_days = []  # List to store the available days for the selected clinician
selected_dates = []  # List to store selected availability days by the patient

# Verify clinician's registration status and availability
if st.button("Verify Clinician"):
    st.session_state['clinician_status'] = None
    st.session_state['available_days'] = []  # Reset available days on verification
    if dedicated_clinician in clinicians["name"].values:  # Check if the clinician exists in the database
        clinician_row = clinicians[clinicians["name"] == dedicated_clinician]  # Get the clinician's data
        st.session_state['clinician_status'] = clinician_row["registered"].values[0]  # Check if the clinician is registered
        st.session_state['available_days'] = clinician_row["availability"].values[0]  # Get the clinician's availability
        if st.session_state['clinician_status']:
            # If clinician is registered
            st.success(f"✅ {dedicated_clinician} is registered on the platform.")
            st.write(f"📅 **Available Days:** {', '.join(st.session_state['available_days'])}")
        else:
            # If clinician is not registered
            st.warning(f"⚠️ {dedicated_clinician} is not registered on the platform. They will not receive your request.")
    else:
        # If clinician name doesn't exist in the database
        st.error("❌ No record found for this clinician. Please check the name and try again.")

# Availability Selection Section
st.header("Select Your Availability (Based on Clinician's Availability)")
# Show availability days only after clinician is verified
if 'available_days' in st.session_state and st.session_state['available_days']:
    selected_dates = st.multiselect("Choose your available days", st.session_state['available_days'])  # Select available days
else:
    selected_dates = []
    st.warning("Please verify your clinician to see available days.")  # Warn if clinician is not verified yet

# Consent for Data Sharing Section
st.header("Data Sharing Consent")
# Radio button for consent to share symptom data with clinician
consent = st.radio("Do you allow your clinician to access your symptom details for better diagnosis?", ["Yes", "No"], index=None)

# Button to send request to clinician
if st.button("Send Request to Clinician"):
    # Validation checks before sending the request
    if st.session_state['clinician_status'] is None:
        st.error("Please verify your clinician before sending the request.")  # Check if clinician is verified
    elif not st.session_state['clinician_status']:
        st.error("Your selected clinician does not have an account and cannot receive your request.")  # Check if clinician is registered
    elif not selected_dates:
        st.warning("Please select at least one available day before proceeding.")  # Ensure at least one day is selected
    elif consent is None:
        st.warning("Please choose an option for data sharing before proceeding.")  # Ensure consent is selected
    else:
        # If consent is given, send request with symptom details
        if consent == "Yes":
            st.success(f"Request sent to {dedicated_clinician}. They will receive your availability and symptom details.")
        else:
            # If consent is not given, send request without symptom details
            st.info(f"Request sent to {dedicated_clinician}. They will only see your availability and symptom severity, but not your symptom details.")
