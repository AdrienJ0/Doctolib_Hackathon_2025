# 🏥 Medical Platform Dashboard & Appointment System

This is a medical platform dashboard built with **Streamlit**, designed to facilitate the process of doctor-patient matchmaking, appointment management, and consultation requests. The platform includes features for clinicians to manage their appointments, interact with patient requests, and match patients with available doctors based on their location and availability.

## Here is the demo 

https://drive.google.com/file/d/1jITYZV9DPo5QpHVf4uc4i6nl40kALVSo/view?usp=sharing

## 🎥 Demo Video

[![Watch the Demo](https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)](https://drive.google.com/file/d/1jITYZV9DPo5QpHVf4uc4i6nl40kALVSo/view?usp=sharing)

## Features

- **Clinician Dashboard**: View and manage current appointments, verify new patient requests, and match patients based on location and availability.
- **Patient Dashboard**: Select available dates, share location, and submit consultation requests.
- **Location Integration**: Patients can share their current location, and doctors will be ranked based on proximity using geolocation.
- **Doctor Availability**: Patients can view available doctors who match their symptoms and availability.
- **Data Sharing Consent**: Before sending consultation requests, patients must provide consent regarding the sharing of personal data with doctors.
- **Calendar Integration**: Clinicians can view appointments in a calendar format.

## Setup

### Prerequisites

1. **Python**: Ensure you have Python 3.7 or higher.
2. **Required Libraries**: Install the following Python packages:

    See the file requirements.txt

   You can install them using the following:

    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

You can set your API key by creating a `.env` file and including the following:

```text
API_KEY="your_api_key_here"
```

# Running the App

**NB:** The deployment is under progress. If you want to run it go on the branch **"deploiement"**

To run the Streamlit app, use the following command:

`streamlit run Login.py`

Where Login.py is the Python script containing the Streamlit app.

# Functionality Breakdown
1. Clinician Dashboard

    Appointment Calendar: Displays upcoming appointments for the selected clinician, using fullcalendar.
    Patient Management: Allows clinicians to view, accept, or decline new patient requests based on their medical symptoms and consent.
    Doctor Availability: Clinicians can filter patients based on available dates and times, improving appointment scheduling.

2. Patient Dashboard

    Location Access: Patients can opt-in to share their location, enabling location-based doctor matchmaking.
    Symptom Input: Patients can enter the severity of their symptoms, which is sent to the selected clinician for review.
    Doctor Search: Based on location and availability, the system ranks doctors, showing the closest available doctors based on geolocation.
    Data Sharing Consent: Patients consent to share medical data with the doctor for consultation, ensuring privacy control.

3. Doctor Matching Algorithm

    Location-Based Matching: The system calculates the distance between the patient and available doctors using geopy's geodesic function.
    Availability-Based Matching: Doctors are filtered based on their availability and the patient's selected dates.

4. Data Sharing

    Data Sharing Consent: Before submitting consultation requests, patients are asked to provide consent on whether doctors can access their medical data for diagnosis purposes.

The system ensures that only the necessary information is shared based on the patient's consent.
Code Structure

    Login.py: The main Streamlit application file containing the UI components and logic for clinician and patient management.
    resources: Contains the sample data for doctors, patients, and new patient requests. This data can be replaced with live data sources or a database in production.
    requirements.txt: A text file listing all Python dependencies required for running the app.
    .env: (Optional) Stores environment variables like the Google Maps API key for location services.

# Example Use Cases

    Clinician Interaction:
        Clinicians can select their name from a dropdown and view a calendar of their upcoming appointments.
        They can accept or decline new patient requests based on the symptom severity and available dates.

    Patient Interaction:
        Patients can select their available dates and share their current location for more accurate doctor matching.
        The system ranks available doctors based on proximity and availability, allowing the patient to select their preferred doctors.

# Case 1

![Case 1 - 1](case1%201%20info.png)
![Case 1 - 2](case1%202.png)
![Case 1 - 3](case1%203.png)
![Case 1 - 4](case1%204%20sum.png)
![Case 1 - 5](case1%205%20sever.png)
![Case 1 - 6](case1%206%20appoint.png)

# Case 2

![Case 2 - 1](case2%201%20.png)
![Case 2 - 2](case2%202.png)
![Case 2 - 3](case2%203.png)
![Case 2 - 4](case2%204.png)
![Case 2 - 5](case2%205.png)
![Case 2 - PDF](case2%20pdf.png)

# Future Improvements

    Real-Time Data Sync: Integrate with a database to manage live clinician and patient data.
    Advanced Matching Algorithm: Implement more complex algorithms to match doctors and patients based on additional criteria (e.g., specialty).
    Google Maps Integration: Complete the Google Maps integration for geolocation and address fetching.
    Appointment Booking: Allow patients to book appointments directly with the clinician from the dashboard.
    Patient History: Implement a feature for patients to submit their medical history or reports for review by clinicians.

# Contributing

If you'd like to contribute to the project, feel free to fork the repository, make improvements, and submit a pull request.
License

This project is licensed under the MIT License.


