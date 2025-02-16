"""🚀 Building an AI-Powered Medical Chatbot for Patients
You want to build a smart chatbot that:
✅ Extracts patient details (Name, Age) from a PDF or asks the user if missing
✅ Asks the patient to upload pathology reports and symptoms
✅ Generates a summary of the report, severity level, and specialist recommendation
✅ Continues chatting with the patient to assist with scheduling an appointment
✅ Handles complex medical cases & guides the patient effectively"""

import streamlit as st
import fitz  # PyMuPDF for PDF processing
from openai import OpenAI

# Initialize OpenAI Client (Replace with your API Key)
client = OpenAI(
    base_url = "https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1",
    api_key = "35465751-64a0-4d1e-87aa-fd326c191da1" # Replace SCW_SECRET_KEY with your IAM API key
)

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])

# Function to Extract Patient Details
def extract_patient_details(pdf_text):
    prompt = f"""
    Extract the **patient's name and age** from this medical report:

    **Report:**
    {pdf_text[:2000]}

    Return in this format:
    - **Name:** [Patient Name]
    - **Age:** [Patient Age]
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are an AI medical assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

# Function to Process Key Findings
def analyze_key_findings(pdf_text):
    prompt = f"""
    Extract **key medical findings** from this report:

    **Report:**
    {pdf_text[:2000]}

    Return only **important lab values** that indicate risks.
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are an AI medical expert."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )

    return response.choices[0].message.content.strip()

# Function to Summarize Condition
def summarize_condition(key_findings, symptoms):
    prompt = f"""
    Summarize the patient's condition based on **lab findings and symptoms**.

    **Findings:**
    {key_findings}

    **Symptoms:**
    {symptoms}

    Provide a **clear, structured medical summary**.
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are a medical diagnosis AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=350
    )
    
    return response.choices[0].message.content.strip()

# Function to Recommend Specialist
def recommend_specialist(summary):
    prompt = f"""
    Suggest the **best specialist** based on this **medical summary**:

    **Summary:**
    {summary}

    Choose from:
    - **General Physician**
    - **Diabetologist**
    - **Cardiologist**
    - **Neurologist**

    Return **only the best specialist**.
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are a specialist recommendation AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content.strip()

# Streamlit Chatbot UI
st.title("💬 AI Medical Chatbot")

# **Initialize session state**
if "step" not in st.session_state:
    st.session_state.step = "ask_name"
    st.session_state.name = ""
    st.session_state.age = ""
    st.session_state.symptoms = ""
    st.session_state.pdf_text = ""
    st.session_state.key_findings = ""
    st.session_state.summary = ""

# **Chat Input**
user_input = st.chat_input("Ask the AI medical chatbot...")

if user_input:
    if st.session_state.step == "ask_name":
        st.session_state.name = user_input
        st.session_state.step = "ask_age"
        st.write(f"👤 Patient Name: {st.session_state.name}")
        st.chat_message("assistant").write("How old are you?")

    elif st.session_state.step == "ask_age":
        st.session_state.age = user_input
        st.session_state.step = "ask_symptoms"
        st.write(f"🎂 Age: {st.session_state.age}")
        st.chat_message("assistant").write("What symptoms are you experiencing?")

    elif st.session_state.step == "ask_symptoms":
        st.session_state.symptoms = user_input
        st.session_state.step = "ask_report"
        st.write(f"🤒 Symptoms: {st.session_state.symptoms}")
        st.chat_message("assistant").write("Please upload your pathology report (PDF) for analysis.")

# **File Upload for Medical Report**
uploaded_file = st.file_uploader("Upload your pathology report (PDF)", type="pdf")

if uploaded_file and st.session_state.step == "ask_report":
    with open("temp_report.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.pdf_text = extract_text_from_pdf("temp_report.pdf")

    # Extract Patient Details from PDF
    patient_details = extract_patient_details(st.session_state.pdf_text)

    # Extract Key Findings from Report
    st.session_state.key_findings = analyze_key_findings(st.session_state.pdf_text)

    # Summarize the Condition
    st.session_state.summary = summarize_condition(st.session_state.key_findings, st.session_state.symptoms)

    # Recommend a Specialist
    recommended_specialist = recommend_specialist(st.session_state.summary)

    # **Display AI Results**
    ai_response = f"""
    **🔹 Patient Details:**  
    {patient_details}  

    **📊 Key Medical Findings:**  
    {st.session_state.key_findings}  

    **📝 Medical Summary:**  
    {st.session_state.summary}  

    **👨‍⚕️ Recommended Specialist:**  
    **{recommended_specialist}**  
    """

    st.session_state.step = "continue_chat"
    st.session_state.messages = [{"role": "assistant", "content": ai_response}]
    st.chat_message("assistant").write(ai_response)

# **Continue Chat After Report Analysis**
if st.session_state.step == "continue_chat":
    follow_up_input = st.chat_input("Do you need further assistance?")

    if follow_up_input:
        if "appointment" in follow_up_input.lower():
            st.chat_message("assistant").write("📅 I can help schedule an appointment with your specialist. Would you like to proceed?")
        elif "more details" in follow_up_input.lower():
            st.chat_message("assistant").write("🔍 Would you like a deeper analysis of your report?")
        else:
            st.chat_message("assistant").write("How else can I assist you?")
