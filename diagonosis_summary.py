# """✅ Extracts Key Findings – DeepSeek analyzes the blood report and extracts the most relevant lab values
# ✅ Summarizes the Condition – Generates a clear, structured medical summary
# ✅ Severity Analysis – Determines the case's severity (Mild 🟢, Moderate 🟡, Severe 🔴) based on extreme lab values
# ✅ Highlights Critical Lab Values – Displays which blood test values are too high or too low
# ✅ Specialist Recommendation – Suggests the best doctor based on the patient’s condition"""



# import streamlit as st
# import pandas as pd
# import fitz  # PyMuPDF
# from openai import OpenAI

# # Initialize OpenAI Client (Replace with your API Key)
# client = OpenAI(
#     base_url = "https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1",
#     api_key = "35465751-64a0-4d1e-87aa-fd326c191da1" # Replace SCW_SECRET_KEY with your IAM API key
# )

# # Function to Extract Text from PDF
# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF medical report."""
#     doc = fitz.open(pdf_path)
#     return "\n".join([page.get_text("text") for page in doc])

# # Function to Extract Key Findings
# def extract_key_findings(pdf_text):
#     """Uses DeepSeek to extract key findings from the report."""
#     prompt = f"""
#     You are an AI medical assistant. Extract the **key medical findings** from the following **blood report**:

#     **Patient's Medical Report:**
#     {pdf_text[:2000]}

#     Provide only the **most important lab values** that may indicate health risks.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical analysis AI."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=400,
#         temperature=0.3,
#         top_p=0.9
#     )

#     return response.choices[0].message.content.strip()

# # Function to Summarize the Report
# def summarize_disease_with_deepseek(key_findings, symptoms):
#     """Summarizes the patient's condition based on medical report findings and symptoms."""
#     prompt = f"""
#     You are an AI medical expert. Summarize the patient's condition based on the **lab report findings** and **symptoms**.

#     **Key Medical Findings:**
#     {key_findings}

#     **Patient's Symptoms:**
#     {symptoms}

#     Provide a **clear, structured, and medically accurate summary** in a professional manner.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a concise medical AI."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=350,
#         temperature=0.3,
#         top_p=0.85
#     )
    
#     return response.choices[0].message.content.strip()

# # Function to Analyze Lab Severity
# def analyze_lab_severity(key_findings):
#     """Uses DeepSeek to determine severity based on lab findings."""
#     prompt = f"""
#     You are an AI medical assistant. Analyze the **severity of the patient's case** based on the following lab report findings:

#     **Key Medical Findings:**
#     {key_findings}

#     Classify the severity as:
#     - **Mild 🟢**
#     - **Moderate 🟡**
#     - **Severe 🔴**

#     Also, list **specific lab values that are extremely high or low** and may indicate health risks.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical severity analysis AI."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=400,
#         temperature=0.3,
#         top_p=0.9
#     )

#     return response.choices[0].message.content.strip()

# # Function to Recommend a Specialist
# def recommend_specialist(summary):
#     """Uses DeepSeek to determine the best specialist based on medical findings."""
#     prompt = f"""
#     Based on the following **medical summary**, suggest the **best specialist** for the patient:

#     **Medical Summary:**
#     {summary}

#     Choose from:
#     - **General Physician**
#     - **Diabetologist**
#     - **Cardiologist**
#     - **Neurologist**

#     Return only the **most relevant specialist**.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a specialist recommendation AI."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=50
#     )

#     return response.choices[0].message.content.strip()

# # Streamlit UI
# st.title("🏥 AI-Powered Patient Health Dashboard")
# st.write("Upload a medical report and enter your symptoms for analysis.")

# # File Upload for Medical Report
# uploaded_file = st.file_uploader("Upload PDF Report", type="pdf")

# # User Inputs Symptoms
# user_symptoms = st.text_area("Enter your symptoms", placeholder="E.g., I feel fatigued, have frequent urination, and my sugar level is high.")

# if uploaded_file and user_symptoms:
#     with open("temp_report.pdf", "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Extract text from PDF
#     pdf_text = extract_text_from_pdf("temp_report.pdf")

#     # Extract Key Findings from Report
#     st.subheader("🔍 Extracting Key Medical Findings...")
#     key_findings = extract_key_findings(pdf_text)
#     st.success("✅ Key findings extracted successfully!")

#     # Get AI Summary
#     st.subheader("📝 AI-Generated Medical Summary")
#     summary = summarize_disease_with_deepseek(key_findings, user_symptoms)
#     st.write(summary)

#     # Get AI-Based Severity Analysis
#     st.subheader("🚨 Severity Analysis")
#     severity_analysis = analyze_lab_severity(key_findings)
#     st.write(severity_analysis)

#     # Get Specialist Recommendation
#     st.subheader("👨‍⚕️ Recommended Specialist")
#     recommended_specialist = recommend_specialist(summary)
#     st.write(f"**{recommended_specialist}**")

#----------------------------------------------------------

import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for PDF processing
from openai import OpenAI
import re  # To clean AI output

# Initialize OpenAI Client (Using Scaleway AI)
client = OpenAI(
    base_url="https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1",
    api_key="35465751-64a0-4d1e-87aa-fd326c191da1"  # Replace SCW_SECRET_KEY with your IAM API key
)

# Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_bytes = uploaded_file.getbuffer().tobytes()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        return "\n".join([page.get_text("text") for page in doc])
    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
        return "ERROR: Could not process the PDF."

# Function to Clean AI Output (Remove "Think" Sections)
def clean_ai_response(text):
    """Removes unnecessary explanations from the AI output."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)  # Remove AI thinking
    return text.strip()

# Function to Extract Key Findings
def extract_key_findings(pdf_text):
    """Extracts key lab values and abnormalities from the medical report using Mistral."""
    prompt = f"""
    You are an AI medical assistant. Extract **key medical findings** from the following **blood report**:

    **Medical Report:**
    {pdf_text[:2000]}

    Format output as:
    - 🔴 **Critical Findings:** [Lab Test]: [Value] (Normal Range: [Range])
    - 🟡 **Moderate Findings:** [Lab Test]: [Value] (Normal Range: [Range])
    - 🟢 **Normal Findings:** [Lab Test]: [Value] (Normal Range: [Range])

    No explanations, only findings.
    """

    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages=[{"role": "system", "content": "You are a structured medical AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )

    return clean_ai_response(response.choices[0].message.content.strip())

# Function to Summarize the Condition
def summarize_disease(key_findings, symptoms):
    """Summarizes the patient’s condition based on lab findings and symptoms using Mistral."""
    prompt = f"""
    Summarize the patient’s condition based on **lab report findings** and **symptoms**.

    **Key Findings:**
    {key_findings}

    **Symptoms:**
    {symptoms}

    Provide a **brief, structured medical summary** in bullet points.
    """

    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages=[{"role": "system", "content": "You are a concise medical AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )

    return clean_ai_response(response.choices[0].message.content.strip())

# Function to Analyze Severity
def analyze_lab_severity(key_findings):
    """Determines case severity and highlights critical values using Mistral."""
    prompt = f"""
    Analyze the severity of the case based on the following lab findings:

    **Findings:**
    {key_findings}

    Classify severity:
    - 🟢 **Mild**
    - 🟡 **Moderate**
    - 🔴 **Severe**

    Also, list **specific lab values that are extremely high or low**.
    """

    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages=[{"role": "system", "content": "You are a severity analysis AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )

    return clean_ai_response(response.choices[0].message.content.strip())

# Function to Recommend a Specialist
def recommend_specialist(summary):
    """Suggests the most relevant specialist based on the medical summary using Mistral."""
    prompt = f"""
    Based on the following **medical summary**, recommend the best specialist for the patient:

    **Summary:**
    {summary}

    Choose one:
    - **General Physician**
    - **Diabetologist**
    - **Cardiologist**
    - **Neurologist**

    Return only the specialist name, no explanations.
    """

    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages=[{"role": "system", "content": "You are a specialist recommendation AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🏥 AI-Powered Medical Report Analyzer")

# Upload Medical Report
uploaded_file = st.file_uploader("📄 Upload Pathology Report (PDF)", type="pdf")

# User Symptoms Input
user_symptoms = st.text_area("📝 Describe your symptoms:", placeholder="E.g., Fatigue, frequent urination, headache.")

# Process Data if Inputs Provided
if uploaded_file and user_symptoms:
    st.subheader("🔍 Extracting Medical Report...")
    pdf_text = extract_text_from_pdf(uploaded_file)

    if "ERROR" in pdf_text:
        st.error("🚨 Failed to process the PDF. Please upload a valid document.")
    else:
        st.success("✅ PDF processed successfully!")

        # Extract Key Findings
        st.subheader("🔍 Key Medical Findings")
        key_findings = extract_key_findings(pdf_text)
        st.write(key_findings)

        # Generate Summary
        st.subheader("📝 Medical Summary")
        summary = summarize_disease(key_findings, user_symptoms)
        st.write(summary)

        # Analyze Severity
        st.subheader("🚨 Severity Analysis")
        severity_analysis = analyze_lab_severity(key_findings)
        st.write(severity_analysis)

        # Recommend Specialist
        st.subheader("👨‍⚕️ Recommended Specialist")
        recommended_specialist = recommend_specialist(summary)
        st.success(f"**{recommended_specialist}**")

