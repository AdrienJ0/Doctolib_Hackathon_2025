import streamlit as st
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import datetime


## TODO: Make Google Maps API work
# import googlemaps

# Initialize Google Maps client with your API key (Commented out for security reasons)
# gmaps = googlemaps.Client(key="YOUR_GOOGLE_MAPS_API_KEY")

# Sample doctor data (id, name, location, specialty, availability)
# Creating a DataFrame for doctor information, including names, geographic locations, specialties, and availability
doctors = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "name": ["Dr. Smith", "Dr. Johnson", "Dr. Brown", "Dr. Taylor", "Dr. Anderson", "Dr. Thomas", "Dr. Jackson", "Dr. White", "Dr. Harris", "Dr. Martin"],
    "latitude": np.random.uniform(40.0, 41.0, 10),  # Random latitude values for doctors
    "longitude": np.random.uniform(-74.0, -73.0, 10),  # Random longitude values for doctors
    "specialty": ["General Medicine"] * 10,  # All doctors are generalists in this example
    "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
})

# Streamlit App Title
st.title("🏥 Medical Matchmaking System")

# Availability Selection: Allows the user to select available dates for a consultation
st.header("Select Your Availability")
selected_dates = st.date_input("Choose your available dates", [], min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=30))

# Sidebar for Additional Patient Information
# st.sidebar.header("Additional Patient Information (To Hide)")

# Consent for location access in sidebar
st.subheader("Location Access Consent")
# Checkbox to ask user for location sharing consent
share_location = st.checkbox("Allow access to your current location?")
latitude, longitude = None, None  # Initialize latitude and longitude variables

# If the user allows location access, show input fields for latitude and longitude
if share_location:
    latitude = st.sidebar.number_input("Your Latitude (To Hide)", value=40.5, format="%.6f")  # Get the patient's latitude
    longitude = st.sidebar.number_input("Your Longitude (To Hide)", value=-73.5, format="%.6f")  # Get the patient's longitude

    ## TODO: Make GoogleMaps API work to retrieve the address based on coordinates
    # Get the address using Google Maps Geocoding API (commented out for API integration)
    # geocode_result = gmaps.reverse_geocode((latitude, longitude))
    # if geocode_result:
    #     address = geocode_result[0]['formatted_address']
    #     st.sidebar.write(f"Your current address: {address}")
    # else:
    #     st.sidebar.write("Unable to retrieve address. Please check your location.")

# Number of doctors the patient can select
# Set a fixed number for doctor selection (this can be made dynamic with an input widget)
x = 3

# Initialize session state for doctor selection tracking
if "selected_doctors" not in st.session_state:
    st.session_state["selected_doctors"] = {}

# Calculate distance between patient and doctor if location is provided
if latitude and longitude:
    patient_location = (latitude, longitude)
    # Calculate the distance from patient to each doctor using geodesic
    doctors["distance_km"] = doctors.apply(lambda row: geodesic(patient_location, (row["latitude"], row["longitude"])).km, axis=1)
    # Rank doctors by proximity (distance)
    ranked_doctors = doctors.sort_values(by=["distance_km"], ascending=[True]).head(10)
    # Filter doctors by availability based on selected dates
    available_doctors = ranked_doctors[ranked_doctors["availability"].isin([date.strftime('%A') for date in selected_dates])]
else:
    available_doctors = pd.DataFrame()  # If no location is provided, display no available doctors

# Display top 10 recommended doctors based on location and availability
st.subheader("🔍 Top 10 Recommended Generalist Doctors")

# Count the number of selected doctors to manage the selection button state
selected_count = sum(st.session_state["selected_doctors"].values())

# Iterate through the list of available doctors and display them in the app
for _, row in available_doctors.iterrows():
    col1, col2 = st.columns([3, 1])  # Split layout into two columns (doctor info and select/unselect button)
    with col1:
        is_selected = st.session_state["selected_doctors"].get(row["id"], False)  # Check if this doctor is selected
        color = "#4A90E2" if is_selected else "black"  # Highlight selected doctor
        st.markdown(
            f"<span style='color:{color}; font-weight:bold;'>{row['name']}</span> - {row['availability']} - {row['distance_km']:.2f} km away",
            unsafe_allow_html=True,
        )
    with col2:
        # Disable the button if the max selection count is reached
        disabled = selected_count >= x and not is_selected
        # Button to select or unselect a doctor
        new_state = st.button(
            "Unselect" if is_selected else "Select",
            key=f"select_{row['id']}",
            disabled=disabled
        )
        
        # Update session state when doctor is selected or unselected
        if new_state:
            st.session_state["selected_doctors"][row["id"]] = not is_selected
            st.rerun()  # Force rerun to sync the selection state properly

# Display the names of the selected doctors
selected_names = [row.name for row in available_doctors.itertuples() if st.session_state["selected_doctors"].get(row.id, False)]

# Consent Pop-up before sending requests
st.header("Data Sharing Consent")
# Radio button to get patient consent for sharing their data with doctors
consent = st.radio("Do you allow doctors to access your personal data for better diagnosis?", ["Yes", "No"], index=None)

# Button to send consultation requests
if st.button("Send Consultation Requests"):
    if selected_names:  # Ensure at least one doctor is selected
        if consent == "Yes":
            # If consent is given, display a success message
            st.success(f"Request sent to: {', '.join(selected_names)}. Awaiting doctor responses.")
        elif consent == "No":
            # If consent is denied, show a message without sharing personal data
            st.info("Your request has been sent. Doctors will only see your severity score but not your medical history or personal symptoms.")
        else:
            # If no consent option is selected, show a warning
            st.warning("Please choose an option for data sharing before proceeding.")
    else:
        # Show a warning if no doctor is selected
        st.warning("Please select at least one doctor to proceed.")
