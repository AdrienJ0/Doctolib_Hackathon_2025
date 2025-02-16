import streamlit as st
import fitz  # PyMuPDF for PDF processing
from openai import OpenAI
import re
import os
from dotenv import load_dotenv

# Load environment variables (e.g., API keys) from .env file
load_dotenv()

# Define the model for OpenAI API
MODEL_NAME = "mistral-nemo-instruct-2407"

# Initialize the OpenAI client using API key from environment variables
client = OpenAI(
    base_url="https://api.scaleway.ai/74bb05fa-56e4-49d4-949a-fabc5875d712/v1", 
    # base_url = "https://api.mistral.ai/v1",
    api_key=os.getenv("API_KEY")  # Ensure the API key is stored securely in a .env file
)

# ✅ Medical Question Prompts for gathering patient history
prompts = {
    "chief_complaint": "Please describe the main reason for your visit today.",
    "history_of_present_illness": "Detail the timeline of your current symptoms, starting from when they first appeared.",
    "past_medical_history": "Do you have any ongoing medical conditions or a history of any diseases?",
    "drug_history": "What medications are you currently taking, and do you have any known allergies?",
    "family_history": "Is there a history of any genetic diseases in your family?",
    "social_history": "Do you smoke or consume alcohol regularly?",
    "recent_tests": "Do you have any recent medical tests or documents? If so, please upload a pathology report."
}

# ✅ Function to Remove AI "Thinking" Sections
def remove_think_tags(text):
    """Removes <think> tags from AI responses to clean up the output."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# ✅ Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file using PyMuPDF."""
    if type(uploaded_file) == str:
        if uploaded_file == 'no medical report provided':
            return 'no medical report provided'

    try:
        # Open the PDF from the uploaded file
        pdf_bytes = uploaded_file.getbuffer().tobytes()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        # Extract text from each page of the PDF
        return "\n".join([page.get_text("text") for page in doc])
    except Exception as e:
        # Error handling if PDF cannot be processed
        st.error(f"❌ Error processing PDF: {str(e)}")
        return "ERROR: Could not process the PDF."

# ✅ Function to Extract Key Medical Findings from PDF Text
def extract_key_findings(pdf_text):
    """Extracts key lab values and abnormalities using the AI model."""
    prompt = f"""
                Extract **key medical findings** from the following **blood report**. For each lab test result, calculate a normalized score between 0 and 10 based on its value relative to the provided normal range. Use the following rules for normalization:
                
                **Important: Only use the provided information and do not introduce any unverified or fabricated details (avoid hallucinations).** 

                **Medical Report:**
                {pdf_text[:2000]}

                Format output as:
                - 🔴 **Critical Findings:** [Lab Test]: [Normalized Value] (Original Value: [Value], Normal Range: [Range])
                - 🟡 **Moderate Findings:** [Lab Test]: [Normalized Value] (Original Value: [Value], Normal Range: [Range])
                - 🟢 **Normal Findings:** [Lab Test]: [Normalized Value] (Original Value: [Value], Normal Range: [Range])
                """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are a structured medical AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )

    return remove_think_tags(response.choices[0].message.content.strip())

# ✅ Function to Generate a Medical Summary Based on Patient History
def summarize_disease(the_dict_of_q_and_a, key_findings):
    """Generates a structured summary of the patient’s condition."""
    qa_list = [f"[Question]{q}\n[Answer]{a}" for q, a in the_dict_of_q_and_a.items()]
    qa_content = "\n".join(qa_list)  # Join all items in the list into a single string separated by newlines
    prompt = f"""
    Provide a clear and structured summary of the patient's condition that is suitable for both patients and healthcare professionals. Use plain, accessible English while retaining key clinical details. **Important: Only use the provided information and do not introduce any unverified or fabricated details (avoid hallucinations).**

    {qa_content}

    Present your summary in bullet points.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are a concise medical AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )

    return remove_think_tags(response.choices[0].message.content.strip())

# ✅ Function to Analyze Case Severity Based on Medical Summary
def analyze_lab_severity(summary):
    """Determines case severity & highlights critical values using Mistral."""
    prompt = f"""
            Analyze the severity of the patient's case based on the following findings:

            **Findings:**
            {summary}

            For this analysis:
            - Assign a severity score between 0 and 10 (0 = no severity, 10 = most severe).
            - If the patient's symptoms are extremely severe (e.g., chest pain), include a clear warning advising immediate emergency care.
            - Classify severity as:
            - 🟢 Mild
            - 🟡 Moderate
            - 🔴 Severe
            - Identify and list specific lab values that are extremely high or low.
            renmember that Assign a severity score between 0 and 10 (0 = no severity, 10 = most severe).
            Provide your analysis and severity score in English.
            """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are a severity analysis AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )

    return remove_think_tags(response.choices[0].message.content.strip())

# ✅ Function to Recommend a Specialist Based on Medical Summary
def recommend_specialist(summary):
    """Suggests the most relevant specialist based on the medical summary."""
    prompt = f"""
    Based on the **medical summary**, recommend the **best specialist** for the patient:

    **Summary:**
    {summary}

    Choose one:
    - **Gynécologue**
    - **Ophtalmologue**
    - **Psychiatre**
    - **Dentiste**
    - **Pédiatre**
    - **Masseur-kinésithérapeute**
    - **Sage-femme**
    - **médecin traitant**

    Just choose one of the above options. Just give a short answer.

    Only if the situation is urgent, please recommend the patient to go to the emergency room.
    and try to convince the patient to go to the emergency room.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are a specialist recommendation AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=4096
    )

    return response.choices[0].message.content.strip()


# ✅ Streamlit Chatbot UI for collecting user input and displaying medical history
st.title("💬 AI Medical Chatbot")

# Initialize session state if not already initialized
if "qa_history" not in st.session_state:
    st.session_state.qa_history = {}

# Display chat history (previous questions and answers)
for q, a in st.session_state.qa_history.items():
    st.write(f"❓ **{q}:** {a}")

# Display all questions if not all are answered
if len(st.session_state.qa_history) < len(prompts):
    st.subheader("📝 Please fill in the following medical information:")
    
    # Create container for question inputs
    form_container = st.container()
    with form_container:
        all_answered = True
        responses = {}
        
        # Loop through all medical prompts and create input fields
        for i, (q_key, q_text) in enumerate(prompts.items()):
            if q_key not in st.session_state.qa_history:
                all_answered = False
                default_value = ""
            else:
                default_value = st.session_state.qa_history[q_key]
            
            # Create input field for each question
            response = st.text_input(
                label=f"{i+1}. {q_text}",
                value=default_value,
                key=f"input_{q_key}"
            )
            responses[q_key] = response

        # Add submit button to collect all answers
        if st.button("Submit All Answers"):
            processed_responses = {
                k: v if v else "No" 
                for k, v in responses.items()
            }
            # Update session state with responses
            st.session_state.qa_history.update(processed_responses)
            st.rerun()


# ✅ Generate follow-up questions based on medical history
def generate_followup_question(qa_history):
    """Generates a context-aware follow-up question using AI analysis."""
    qa_text = "\n".join([f"Q: {q}\nA: {a}" for q,a in qa_history.items()])
    
    prompt = f"""
    Analyze this patient Q&A history and suggest ONE crucial follow-up question 
    that could reveal missing information important for diagnosis:
    
    {qa_text}

    You need to ask how severe the patient's condition is. (e.g. How severe is the patient's condition? grade the pain from 1 to 10)

    You need to ask the most important question to get the most important information. Do not ask too many.
    
    Output format: <think>analysis</think>\n\nQuestion: [your question]
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    return remove_think_tags(response.choices[0].message.content.strip())

# **Analyze Medical Data if Complete**
if len(st.session_state.qa_history) == len(prompts):
    if "followup_answered" not in st.session_state:
        # Generate follow-up question
        followup_question = generate_followup_question(st.session_state.qa_history)
        st.subheader("🔍 Follow-up Question")
        
        # Display follow-up question form
        with st.form("followup_form"):
            st.markdown(f"**{followup_question}**")
            followup_answer = st.text_input("Your response:")
            submitted = st.form_submit_button("Submit Follow-up")
            
            if submitted:
                if followup_answer.strip():
                    # Save the follow-up answer and mark as answered
                    st.session_state.qa_history["followup"] = followup_answer
                    st.session_state.followup_answered = True
                    st.rerun()
                else:
                    st.warning("Please provide a response before submitting")
        
        # Stop further code execution if follow-up question is displayed
        st.stop()

if len(st.session_state.qa_history) > len(prompts):
    # Handle report upload based on the user's answer to "recent_tests"
    report_answer = st.session_state.qa_history.get("recent_tests", "no").lower()
    
    # If no medical report is provided, show a message
    if 'no' in report_answer:
        uploaded_file = 'no medical report provided'
    else:
        st.subheader("📄 Pathology Report Upload")
        uploaded_file = st.file_uploader(
            "Please upload your pathology report (PDF format)",
            type="pdf",
            key="report_uploader"
        )

    # Extract text from the uploaded PDF and display findings
    st.subheader("🔍 Extracting Medical Report...")
    pdf_text = extract_text_from_pdf(uploaded_file)

    if "ERROR" in pdf_text:
        st.error("🚨 Failed to process the PDF.")
    else:
        st.success("✅ PDF processed successfully!")

        # Extract Key Findings
        key_findings = extract_key_findings(pdf_text)
        st.subheader("🔍 Key Medical Findings")
        st.write(key_findings)

        # Generate a Medical Summary
        summary = summarize_disease(st.session_state.qa_history, key_findings)
        st.subheader("📝 Medical Summary")
        st.write(summary)

        # Analyze Severity of the Condition
        severity_analysis = analyze_lab_severity(summary)
        st.subheader("🚨 Severity Analysis")
        st.write(severity_analysis)

        # Recommend a Specialist Based on Summary
        recommended_specialist = recommend_specialist(summary)
        st.subheader("👨‍⚕️ Recommended Specialist")
        st.success(f"**{recommended_specialist}**")

        # Appointment Booking Flow
        if "show_appointment_form" not in st.session_state:
            st.session_state.show_appointment_form = False

        # First step: Ask if the user wants to book an appointment
        if not st.session_state.show_appointment_form:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, I want to book an appointment"):
                    st.session_state.show_appointment_form = True
                    st.rerun()
            with col2:
                if st.button("❌ No, thank you"):
                    st.success("Thank you for using our service! Feel free to come back anytime.")

        # Second step: Show appointment form
        if st.session_state.show_appointment_form:
            with st.form("appointment_form"):
                st.write("**Appointment Details**")
                
                # Auto-fill the specialist name in the form
                default_specialist = recommended_specialist.split(":")[-1].strip() if ":" in recommended_specialist else recommended_specialist
                specialist = st.text_input("Specialist", value=default_specialist, disabled=True)
                
                # User input fields for appointment details
                name = st.text_input("Full Name*", placeholder="John Doe")
                contact = st.text_input("Contact Info*", placeholder="Phone/Email")
                appointment_date = st.date_input("Preferred Date*")
                appointment_time = st.selectbox("Preferred Time*", 
                                            ["9:00 AM", "10:00 AM", "2:00 PM", "3:00 PM", "4:00 PM"])
                symptoms = st.text_area("Additional Notes", 
                                    placeholder="Briefly describe your main symptoms")
                
                # Submit button to confirm appointment
                submitted = st.form_submit_button("Book Appointment")
                if submitted:
                    if name.strip() and contact.strip():
                        st.session_state.appointment_booked = True
                        st.success("✅ Appointment Request Submitted!")
                        st.balloons()
                        
                        # Display appointment summary
                        st.subheader("Appointment Summary")
                        st.markdown(f"""
                        - **Specialist:** {specialist}
                        - **Patient Name:** {name}
                        - **Contact:** {contact}
                        - **Preferred Time:** {appointment_date} at {appointment_time}
                        """)
                        
                        # Display next steps for appointment confirmation
                        st.info("""
                        **Next Steps:**
                        1. Our staff will confirm your appointment within 24 hours
                        2. Please arrive 15 minutes before your scheduled time
                        3. Bring your ID and insurance card
                        """)
                    else:
                        st.warning("⚠️ Please fill all required fields (marked with *)")
