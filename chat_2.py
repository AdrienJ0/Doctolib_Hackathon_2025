
# This works good but don't ask the right questions and don't show chat history

# import streamlit as st
# import fitz  # PyMuPDF for PDF processing
# from openai import OpenAI
# import json

# # Initialize OpenAI Client
# client = OpenAI(
#     base_url="https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1",
#     api_key="35465751-64a0-4d1e-87aa-fd326c191da1"
# )

# # Medical prompts for chatbot flow
# MEDICAL_PROMPTS = {
#     "chief_complaint": "What is the main reason for your visit today?",
#     "history_of_present_illness": "Describe how your symptoms started and evolved over time.",
#     "past_medical_history": "Do you have any known medical conditions?",
#     "drug_history": "List any medications you are currently taking.",
#     "family_history": "Is there a history of genetic diseases in your family?",
#     "social_history": "Do you smoke or consume alcohol regularly?",
#     "recent_tests": "Have you undergone any medical tests? Upload the report if available."
# }

# # Function to Extract Text from PDF
# def extract_text_from_pdf(uploaded_file) -> str:
#     """Extract text from uploaded PDF file."""
#     try:
#         doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#         return "\n".join([page.get_text() for page in doc])
#     except Exception as e:
#         st.error(f"❌ Error processing PDF: {str(e)}")
#         return ""

# # Function to Extract Patient Details
# def extract_patient_details(pdf_text):
#     """Extracts Name & Age from medical report using DeepSeek R1."""
#     prompt = f"""
#     Extract the **patient's name and age** from this medical report:

#     **Report:**
#     {pdf_text[:2000]}

#     Return in this format:
#     - **Name:** [Patient Name]
#     - **Age:** [Patient Age]
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are an AI medical assistant. Keep the response direct."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=150
#     )

#     return response.choices[0].message.content.strip()

# # Function to Analyze Key Findings
# def analyze_key_findings(pdf_text):
#     """Extracts key medical findings from pathology report."""
#     prompt = f"""
#     Extract **key medical findings** from this pathology report:

#     **Report:**
#     {pdf_text[:2000]}

#     Provide findings in a structured format:
#     - **Abnormal Lab Values:** [List with Normal Ranges]
#     - **Key Findings:** [Summarized medical condition]
#     - **Critical Alerts:** [Any urgent issues]
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical expert AI. Keep the response structured."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=500
#     )

#     return response.choices[0].message.content.strip()

# # Function to Summarize Medical Condition
# def summarize_condition(key_findings, symptoms):
#     """Summarizes patient’s condition based on lab findings & symptoms."""
#     prompt = f"""
#     Summarize the patient's medical condition based on **lab findings and symptoms**.

#     **Findings:**
#     {key_findings}

#     **Symptoms:**
#     {symptoms}

#     Provide a structured medical summary in simple terms.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical diagnosis AI. Respond concisely."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=350
#     )
    
#     return response.choices[0].message.content.strip()

# # Function to Recommend a Specialist
# def recommend_specialist(summary):
#     """Recommends the best specialist for the patient."""
#     prompt = f"""
#     Based on the following **medical summary**, suggest the best specialist.

#     **Summary:**
#     {summary}

#     Choose from:
#     - **General Physician**
#     - **Diabetologist**
#     - **Cardiologist**
#     - **Neurologist**

#     Return only the specialist name.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a specialist recommendation AI. Be concise."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=50
#     )

#     return response.choices[0].message.content.strip()

# # Streamlit Chatbot UI
# st.title("💬 AI Medical Chatbot")

# # **Initialize session state**
# if "step" not in st.session_state:
#     st.session_state.step = "ask_name"
#     st.session_state.name = ""
#     st.session_state.age = ""
#     st.session_state.symptoms = ""
#     st.session_state.pdf_text = ""
#     st.session_state.key_findings = ""
#     st.session_state.summary = ""
#     st.session_state.specialist = ""
#     st.session_state.chat_history = []

# # **Chat Input**
# user_input = st.chat_input("Ask the AI medical chatbot...")

# if user_input:
#     st.session_state.chat_history.append({"role": "user", "content": user_input})

#     if st.session_state.step == "ask_name":
#         st.session_state.name = user_input
#         st.session_state.step = "ask_age"
#         st.chat_message("assistant").write("How old are you?")

#     elif st.session_state.step == "ask_age":
#         st.session_state.age = user_input
#         st.session_state.step = "ask_symptoms"
#         st.chat_message("assistant").write("What symptoms are you experiencing?")

#     elif st.session_state.step == "ask_symptoms":
#         st.session_state.symptoms = user_input
#         st.session_state.step = "ask_report"
#         st.chat_message("assistant").write("Please upload your pathology report (PDF) for analysis.")

# # **File Upload for Medical Report**
# uploaded_file = st.file_uploader("Upload your pathology report (PDF)", type="pdf")

# if uploaded_file and st.session_state.step == "ask_report":
#     st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)

#     # Extract Patient Details
#     patient_details = extract_patient_details(st.session_state.pdf_text)

#     # Extract Key Findings
#     st.session_state.key_findings = analyze_key_findings(st.session_state.pdf_text)

#     # Summarize the Condition
#     st.session_state.summary = summarize_condition(st.session_state.key_findings, st.session_state.symptoms)

#     # Recommend a Specialist
#     st.session_state.specialist = recommend_specialist(st.session_state.summary)

#     # **Store AI Responses in Chat History**
#     ai_response = f"""
#     **👤 Patient Details:**  
#     {patient_details}  

#     **📊 Key Medical Findings:**  
#     {st.session_state.key_findings}  

#     **📝 Medical Summary:**  
#     {st.session_state.summary}  

#     **👨‍⚕️ Recommended Specialist:**  
#     **{st.session_state.specialist}**  
#     """

#     st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
#     st.session_state.step = "continue_chat"

# # **Display Chat History**
# for message in st.session_state.chat_history:
#     st.chat_message(message["role"]).write(message["content"])

# # **Continue Chat After Report Analysis**
# if st.session_state.step == "continue_chat":
#     follow_up_input = st.chat_input("Do you need further assistance?")
#     if follow_up_input:
#         st.session_state.chat_history.append({"role": "user", "content": follow_up_input})
#         st.chat_message("assistant").write("How else can I assist you?")

#---------------------------------------------------------------------------------------------------------------------------------------


#This work fine just don't show chat history and thinks out loud

# import streamlit as st
# import fitz  # PyMuPDF for PDF processing
# from openai import OpenAI
# import json

# # Initialize OpenAI Client
# client = OpenAI(
#     base_url="https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1",
#     api_key="35465751-64a0-4d1e-87aa-fd326c191da1"
# )

# # Medical prompts for chatbot flow
# MEDICAL_PROMPTS = {
#     "chief_complaint": "What is the main reason for your visit today?",
#     "history_of_present_illness": "Describe how your symptoms started and evolved over time.",
#     "past_medical_history": "Do you have any known medical conditions?",
#     "drug_history": "List any medications you are currently taking.",
#     "family_history": "Is there a history of genetic diseases in your family?",
#     "social_history": "Do you smoke or consume alcohol regularly?",
#     "recent_tests": "Have you undergone any medical tests? Upload the report if available."
# }

# # Function to Extract Text from PDF
# def extract_text_from_pdf(uploaded_file) -> str:
#     """Extract text from uploaded PDF file."""
#     try:
#         doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#         return "\n".join([page.get_text() for page in doc])
#     except Exception as e:
#         st.error(f"❌ Error processing PDF: {str(e)}")
#         return ""

# # Function to Analyze Key Findings
# def analyze_key_findings(pdf_text):
#     """Extracts key medical findings from pathology report."""
#     prompt = f"""
#     Extract **key medical findings** from this pathology report.

#     **Report:**
#     {pdf_text[:2000]}

#     Provide findings in a **structured format** with severity:
#     - **🔴 Critical:** [Lab Test]: [Value] (Normal Range: [Range])
#     - **🟡 Moderate:** [Lab Test]: [Value] (Normal Range: [Range])
#     - **🟢 Normal:** [Lab Test]: [Value] (Normal Range: [Range])

#     Only return the structured findings, no explanations.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical AI. Provide structured bullet points without explanations."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=500
#     )

#     return response.choices[0].message.content.strip()

# # Function to Summarize Medical Condition
# def summarize_condition(user_responses, key_findings):
#     """Summarizes patient’s condition based on responses & pathology findings."""
#     prompt = f"""
#     Summarize the patient's medical condition based on their responses and **lab findings**.

#     **User Responses:**
#     - **Chief Complaint:** {user_responses.get("chief_complaint", "Not provided")}
#     - **History of Present Illness:** {user_responses.get("history_of_present_illness", "Not provided")}
#     - **Past Medical History:** {user_responses.get("past_medical_history", "Not provided")}
#     - **Medications:** {user_responses.get("drug_history", "Not provided")}
#     - **Family History:** {user_responses.get("family_history", "Not provided")}
#     - **Social History:** {user_responses.get("social_history", "Not provided")}

#     **Lab Findings:**
#     {key_findings}

#     Provide a short **structured medical summary**, avoiding explanations.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical AI. Provide a structured summary only."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=400
#     )
    
#     return response.choices[0].message.content.strip()

# # Function to Recommend a Specialist
# def recommend_specialist(medical_summary):
#     """Recommends the best specialist for the patient."""
#     prompt = f"""
#     Based on the following **medical summary**, suggest the best specialist.

#     **Summary:**
#     {medical_summary}

#     Choose from:
#     - **General Physician**
#     - **Diabetologist**
#     - **Cardiologist**
#     - **Neurologist**

#     Return only the specialist name, nothing else.
#     """

#     response = client.chat.completions.create(
#         model="deepseek-r1",
#         messages=[{"role": "system", "content": "You are a medical AI. Provide only the specialist name, no explanation."},
#                   {"role": "user", "content": prompt}],
#         max_tokens=50
#     )

#     return response.choices[0].message.content.strip()

# # Streamlit Chatbot UI
# st.title("💬 AI Medical Chatbot")

# # **Initialize session state**
# if "step" not in st.session_state:
#     st.session_state.step = 0
#     st.session_state.responses = {}
#     st.session_state.key_findings = ""
#     st.session_state.medical_summary = ""
#     st.session_state.specialist = ""
#     st.session_state.chat_history = []

# # **Ask Medical Questions Step-by-Step**
# if st.session_state.step < len(MEDICAL_PROMPTS):
#     question_key = list(MEDICAL_PROMPTS.keys())[st.session_state.step]
#     user_input = st.text_input(MEDICAL_PROMPTS[question_key])

#     if user_input:
#         st.session_state.responses[question_key] = user_input
#         st.session_state.step += 1
#         st.rerun()

# # **Ask for PDF Upload After Questions Are Answered**
# elif st.session_state.step == len(MEDICAL_PROMPTS):
#     uploaded_file = st.file_uploader("📄 Upload your pathology report (PDF)", type="pdf")

#     if uploaded_file:
#         st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
#         st.session_state.key_findings = analyze_key_findings(st.session_state.pdf_text)
#         st.session_state.medical_summary = summarize_condition(st.session_state.responses, st.session_state.key_findings)
#         st.session_state.specialist = recommend_specialist(st.session_state.medical_summary)
#         st.session_state.step += 1
#         st.rerun()

# # **Display AI Analysis Once Everything Is Collected**
# elif st.session_state.step > len(MEDICAL_PROMPTS):
#     ai_response = f"""
#     🏥 **Patient Responses:**  
#     {st.session_state.responses}  

#     📊 **Key Medical Findings:**  
#     {st.session_state.key_findings}  

#     📝 **Medical Summary:**  
#     {st.session_state.medical_summary}  

#     👨‍⚕️ **Recommended Specialist:**  
#     **{st.session_state.specialist}**  
#     """

#     st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# # **Display Chat History**
# for message in st.session_state.chat_history:
#     st.chat_message(message["role"]).write(message["content"])

# # **User Chat Input for Follow-Up**
# follow_up_input = st.chat_input("Ask the AI medical chatbot...")

# if follow_up_input:
#     st.session_state.chat_history.append({"role": "user", "content": follow_up_input})

#     # **AI Response to User**
#     follow_up_response = "🔍 How else can I assist you regarding your health?"
#     st.session_state.chat_history.append({"role": "assistant", "content": follow_up_response})
#     st.rerun()

##----------------------------------------------------------------------------------------------------------

import streamlit as st
import fitz  # PyMuPDF for PDF processing
from openai import OpenAI
import json
import re  # To clean AI output

# Initialize OpenAI Client
client = OpenAI(
    base_url="https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1",
    api_key="35465751-64a0-4d1e-87aa-fd326c191da1"
)

# Medical prompts for chatbot flow
MEDICAL_PROMPTS = [
    "What is the main reason for your visit today?",
    "Describe how your symptoms started and evolved over time.",
    "Do you have any known medical conditions?",
    "List any medications you are currently taking.",
    "Is there a history of genetic diseases in your family?",
    "Do you smoke or consume alcohol regularly?",
    "Have you undergone any medical tests? Upload the report if available."
]

# Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from uploaded PDF file."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
        return ""

# Function to Clean AI Output (Remove "Think" Sections)
def clean_ai_response(text):
    """Removes unnecessary explanations from DeepSeek output."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)  # Remove think sections
    return text.strip()

# Function to Analyze Key Findings
def analyze_key_findings(pdf_text):
    """Extracts key medical findings from pathology report."""
    prompt = f"""
    Extract **key medical findings** from this pathology report.

    **Report:**
    {pdf_text[:2000]}

    Provide findings in a **structured format** with severity:
    - **🔴 Critical:** [Lab Test]: [Value] (Normal Range: [Range])
    - **🟡 Moderate:** [Lab Test]: [Value] (Normal Range: [Range])
    - **🟢 Normal:** [Lab Test]: [Value] (Normal Range: [Range])

    Only return the structured findings, no explanations.
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are a medical AI. Provide structured bullet points without explanations."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )

    return clean_ai_response(response.choices[0].message.content.strip())

# Function to Summarize Medical Condition
def summarize_condition(user_responses, key_findings):
    """Summarizes patient’s condition based on responses & pathology findings."""
    prompt = f"""
    Summarize the patient's medical condition based on their responses and **lab findings**.

    **User Responses:**
    {user_responses}

    **Lab Findings:**
    {key_findings}

    Provide a short **structured medical summary**, avoiding explanations.
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are a medical AI. Provide a structured summary only."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )
    
    return clean_ai_response(response.choices[0].message.content.strip())

# Function to Recommend a Specialist
def recommend_specialist(medical_summary):
    """Recommends the best specialist for the patient."""
    prompt = f"""
    Based on the following **medical summary**, suggest the best specialist.

    **Summary:**
    {medical_summary}

    Choose from:
    - **General Physician**
    - **Diabetologist**
    - **Cardiologist**
    - **Neurologist**

    Return only the specialist name, nothing else.
    """

    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[{"role": "system", "content": "You are a medical AI. Provide only the specialist name, no explanation."},
                  {"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content.strip()

# Streamlit Chatbot UI
st.title("💬 AI Medical Chatbot")

# **Initialize session state**
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.responses = []
    st.session_state.key_findings = ""
    st.session_state.medical_summary = ""
    st.session_state.specialist = ""
    st.session_state.chat_history = []

# **Display Chat History**
for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

# **Show First Question Immediately**
if st.session_state.step < len(MEDICAL_PROMPTS):
    question = MEDICAL_PROMPTS[st.session_state.step]

    # Ensure first question is shown automatically
    if len(st.session_state.chat_history) == 0 or st.session_state.chat_history[-1]["role"] != "assistant":
        st.session_state.chat_history.append({"role": "assistant", "content": question})
        st.rerun()

    # **Place answer input box at the TOP**
    user_input = st.text_input("Your Answer:", key="medical_input")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.responses.append(user_input)
        st.session_state.step += 1
        st.rerun()

# **Ask for PDF Upload After Questions Are Answered**
elif st.session_state.step == len(MEDICAL_PROMPTS):
    bot_message = "📄 Please upload your pathology report (PDF)."

    if len(st.session_state.chat_history) == 0 or st.session_state.chat_history[-1]["role"] != "assistant":
        st.session_state.chat_history.append({"role": "assistant", "content": bot_message})

    uploaded_file = st.file_uploader("Upload your pathology report:", type="pdf")

    if uploaded_file:
        st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
        st.session_state.key_findings = analyze_key_findings(st.session_state.pdf_text)
        st.session_state.medical_summary = summarize_condition(st.session_state.responses, st.session_state.key_findings)
        st.session_state.specialist = recommend_specialist(st.session_state.medical_summary)
        st.session_state.step += 1
        st.rerun()

# **Display AI Analysis**
elif st.session_state.step > len(MEDICAL_PROMPTS):
    ai_response = f"""
    📊 **Key Medical Findings:**  
    {st.session_state.key_findings}  

    📝 **Medical Summary:**  
    {st.session_state.medical_summary}  

    👨‍⚕️ **Recommended Specialist:**  
    **{st.session_state.specialist}**  
    """

    if len(st.session_state.chat_history) == 0 or st.session_state.chat_history[-1]["role"] != "assistant":
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# **General Chat Input Box (At Bottom)**
follow_up_input = st.chat_input("Ask the AI medical chatbot...")

if follow_up_input:
    st.session_state.chat_history.append({"role": "user", "content": follow_up_input})
    st.session_state.chat_history.append({"role": "assistant", "content": "🔍 How else can I assist you?"})
    st.rerun()
