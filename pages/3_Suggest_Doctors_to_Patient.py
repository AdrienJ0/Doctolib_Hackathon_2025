import streamlit as st
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import datetime

# Sample doctor data (id, name, location, specialty, availability)
doctors = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "name": ["Dr. Smith", "Dr. Johnson", "Dr. Brown", "Dr. Taylor", "Dr. Anderson", "Dr. Thomas", "Dr. Jackson", "Dr. White", "Dr. Harris", "Dr. Martin"],
    "latitude": np.random.uniform(40.0, 41.0, 10),
    "longitude": np.random.uniform(-74.0, -73.0, 10),
    "specialty": ["General Medicine"] * 10,
    "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
})

# Streamlit App Title
st.title("🏥 Medical Matchmaking System")

# Patient Name Input
st.header("Patient Information")
patient_name = st.text_input("Your Name", "")

# Availability Selection
st.header("Select Your Availability")
selected_dates = st.date_input("Choose your available dates", [], min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=30))

# Consent for location access
st.header("Location Access Consent")
share_location = st.checkbox("Allow access to your current location?")
latitude, longitude = None, None
if share_location:
    latitude = st.number_input("Your Latitude", value=40.5, format="%.6f")
    longitude = st.number_input("Your Longitude", value=-73.5, format="%.6f")

# Sidebar for Additional Patient Information
st.sidebar.header("Additional Patient Information")

# Symptom Severity
symptom_severity = st.sidebar.slider("Rate Your Symptom Severity (1-10)", 1, 10, 5)

# Number of doctors patient can select
x = st.sidebar.number_input("Number of doctors to select", min_value=1, max_value=10, value=3)

# Initialize session state for selections
if "selected_doctors" not in st.session_state:
    st.session_state["selected_doctors"] = {}

# Calculate distance and rank doctors if location is provided
if latitude and longitude:
    patient_location = (latitude, longitude)
    doctors["distance_km"] = doctors.apply(lambda row: geodesic(patient_location, (row["latitude"], row["longitude"])).km, axis=1)
    ranked_doctors = doctors.sort_values(by=["distance_km"], ascending=[True]).head(10)
    available_doctors = ranked_doctors[ranked_doctors["availability"].isin([date.strftime('%A') for date in selected_dates])]
else:
    available_doctors = pd.DataFrame()

# Display ranked doctors
st.subheader("🔍 Top 10 Recommended Generalist Doctors")

selected_count = sum(st.session_state["selected_doctors"].values())

for _, row in available_doctors.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        is_selected = st.session_state["selected_doctors"].get(row["id"], False)
        color = "#4A90E2" if is_selected else "black"
        st.markdown(
            f"<span style='color:{color}; font-weight:bold;'>{row['name']}</span> - {row['availability']} - {row['distance_km']:.2f} km away",
            unsafe_allow_html=True,
        )
    with col2:
        # Disable selection if max reached and doctor isn't already selected
        disabled = selected_count >= x and not is_selected
        new_state = st.button(
            "Unselect" if is_selected else "Select",
            key=f"select_{row['id']}",
            disabled=disabled
        )
        
        if new_state:
            st.session_state["selected_doctors"][row["id"]] = not is_selected
            st.rerun()  # Force rerun to sync selection state properly

# Display selected doctors
selected_names = [row.name for row in available_doctors.itertuples() if st.session_state["selected_doctors"].get(row.id, False)]

# Consent Pop-up before sending requests
st.header("Data Sharing Consent")
consent = st.radio("Do you allow doctors to access your personal data for better diagnosis?", ["Yes", "No"], index=None)

if st.button("Send Consultation Requests"):
    if selected_names:
        if consent == "Yes":
            st.success(f"Request sent to: {', '.join(selected_names)}. Awaiting doctor responses.")
        elif consent == "No":
            st.info("Your request has been sent. Doctors will only see your severity score but not your medical history or personal symptoms.")
        else:
            st.warning("Please choose an option for data sharing before proceeding.")
    else:
        st.warning("Please select at least one doctor to proceed.")
