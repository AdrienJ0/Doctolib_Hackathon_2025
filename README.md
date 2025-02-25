# 🏥 Medical Platform Dashboard & Appointment System

This is a medical platform dashboard built with **Streamlit**, designed to facilitate the process of doctor-patient matchmaking, appointment management, and consultation requests. The platform includes features for clinicians to manage their appointments, interact with patient requests, and match patients with available doctors based on their location and availability.

## Here is the video demo of our platform

https://drive.google.com/file/d/1jITYZV9DPo5QpHVf4uc4i6nl40kALVSo/view?usp=sharing


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

These questions are designed based on the common questions used in family doctor consultations, as outlined in medical guidelines.

R. Turner, R. Blackwood, R. Jones; Guide to History and Examination for Clinical Students; Oxford University Medical School publication.
Liu, C., Scott, K. M., Lim, R. L., Taylor, S., & Calvo, R. A. (2016). EQClinic: a platform for learning communication skills in clinical consultations. Medical education online, 21(1), 31801.

![Case 1 - 1](imgs_readme/case1%201%20info.png)

Since patients often cannot accurately describe their conditions, our program analyzes the questions generated by users and asks more specific questions to help patients express their symptoms and assist doctors in gaining a preliminary understanding.

![Case 1 - 2](imgs_readme/case1%202.png)

The patient condition summary generated by the large language model is concise and clear, suitable for both patients and doctors to gain a preliminary understanding of the condition.

![Case 1 - 3](imgs_readme/case1%203.png)

![Case 1 - 4](imgs_readme/case1%204%20sum.png)

Sometimes, patients may not understand the severity of their symptoms, like chest pain lasting three days that requires immediate medical attention. Our model alerts them to seek emergency care.

![Case 1 - 5](imgs_readme/case1%205%20sever.png)

Patients can also use our system to make appointments.

![Case 1 - 6](imgs_readme/case1%206%20appoint.png)

# Case 2

Another case, a patient with diabetes:

![Case 2 - 1](imgs_readme/case2%201%20.png)
![Case 2 - 2](imgs_readme/case2%202.png)

We can see parts of the large model analysis report and the results.

![Case 2 - PDF](imgs_readme/case%202%20pdf.png)
![Case 2 - 3](imgs_readme/case2%203.png)
![Case 2 - 4](imgs_readme/case2%204.png)
![Case 2 - 5](imgs_readme/case%202%205.png)


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


