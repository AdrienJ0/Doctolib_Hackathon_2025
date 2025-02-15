# Function to generate a synthetic medical record (PDF)
def generate_synthetic_medical_record(patient_name: str) -> str:
    """Generates a synthetic medical record in PDF format."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Basic details
    pdf.cell(200, 10, txt="Medical Record", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {time.strftime('%Y-%m-%d')}", ln=True)

    # Simulated medical data
    symptoms = ["headache", "fatigue", "cough", "fever", "chest pain"]
    treatment_plan = ["rest", "medication", "consult specialist"]
    pdf.cell(200, 10, txt=f"Symptoms: {random.choice(symptoms)}", ln=True)
    pdf.cell(200, 10, txt=f"Treatment Plan: {random.choice(treatment_plan)}", ln=True)

    # Save the PDF
    pdf_output = f"{patient_name}_medical_record.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Step 3: Ask for the medical record
if st.button("Generate Synthetic Medical Record"):
    pdf_path = generate_synthetic_medical_record(patient_name)
    st.write(f"Medical record PDF generated for {patient_name}.")
    st.download_button("Download Medical Record", pdf_path)