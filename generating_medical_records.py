from faker import Faker
import random
import csv

# Create an instance of Faker
fake = Faker('fr_FR')

# Function to generate long medical record data for CSV (with biomedical data)
def generate_medical_record_data():
    medical_records = []
    
    # Sample records with biomedical data
    for patient_id in range(1, 100):
        patient_name = fake.name()
        age = random.randint(30, 70)
        gender = random.choice(["Male", "Female"])
        address = fake.address().replace("\n", ", ")
        
        # Medical History
        medical_history = "Hypertension, Type 2 diabetes, Asthma"
        
        # Diagnosis
        diagnosis = "Mild tachycardia and elevated blood pressure, suspected early-stage heart disease"
        
        # Biomedical Data (Lab Results, Vital Signs, Imaging)
        lab_results = "Blood Pressure: 145/90 mmHg, Blood Glucose: 150 mg/dL, Lipid Profile: High, HbA1c: 7.5%, ECG: Mild tachycardia"
        vital_signs = "Heart Rate: 92 bpm, Respiratory Rate: 18 breaths/min, Oxygen Saturation: 93%, Temperature: 37.1°C, Weight: 85 kg"
        imaging_results = "Echocardiogram: Mild left ventricular hypertrophy, MRI: Normal cerebral circulation"
        
        # Treatment Plan
        treatment_plan = "1. Continue antihypertensive medication, 2. Start beta-blockers, 3. Recommend heart-healthy diet and exercise"
        
        # Append the data as a row
        medical_records.append([
            patient_id, patient_name, age, gender, address, medical_history, 
            diagnosis, lab_results, vital_signs, imaging_results, treatment_plan
        ])
    
    return medical_records

# Generate the data for 3 medical records
medical_data = generate_medical_record_data()

# Define CSV file path
csv_file_path = 'medical_records_with_biomedical_data.csv'

# Write the data to a CSV file
header = ['patient_id', 'name', 'age', 'gender', 'address', 'medical_history', 
          'diagnosis', 'lab_results', 'vital_signs', 'imaging_results', 'treatment_plan']


with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(medical_data)

