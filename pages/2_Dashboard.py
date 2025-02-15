import streamlit as st
import time
import numpy as np
import pandas as pd
from huggingface_hub import InferenceApi

st.markdown("# Patient Dashboard")
st.sidebar.header("Patient Dashboard")

# Load Doctolib Dataset
df = pd.read_excel("doctorlib_dataset.xlsx", sheet_name="dataset")

# Hugging Face API Setup
API_KEY = "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"  # Replace with your actual API key
MODEL_NAME = "BioMistral/BioMistral-7B"
inference = InferenceApi(repo_id=MODEL_NAME, token=API_KEY)

def query_model(prompt):
    response = inference(inputs=prompt)
    if isinstance(response, dict) and "generated_text" in response:
        return response["generated_text"]
    return "⚠️ No response from model. Please try again."

# Doctolib-inspired UI Setup
#st.set_page_config(page_title="Life GuardIANs", page_icon="💙", layout="wide")

# Tabs for navigation
tabs = st.tabs(["🏥 Patient Triage", "📊 Healthcare Access", "💬 Chatbot"])

# Patient Triage Tab
with tabs[0]:
    st.title("🏥 Patient Triage Dashboard")
    patient_data = pd.DataFrame({
        "Patient ID": [f"PT-{i}" for i in range(1, 6)],
        "Symptom Severity Score": [3, 8, 6, 9, 2],
        "Recommendation": ["Teleconsultation", "Urgent Care", "Specialist", "Urgent Care", "Self-monitor"],
    })
    st.dataframe(patient_data)
    st.bar_chart(patient_data.set_index("Patient ID")["Symptom Severity Score"])

# Healthcare Access Tab
with tabs[1]:
    st.title("📊 Healthcare Access Analysis")
    region = st.selectbox("Choose a region:", df["practice_region"].unique())
    specialty = st.selectbox("Choose a specialty:", df["specialty"].unique())
    filtered_data = df[(df["practice_region"] == region) & (df["specialty"] == specialty)]
    st.metric(label="🩺 Available Doctors", value=filtered_data["prats"].sum())
    st.metric(label="⏳ Median Waiting Days", value=int(filtered_data["median_waiting_days_dep"].mean()))
    st.bar_chart(filtered_data.set_index("year")["median_waiting_days_dep"])

# Conversational Chatbot Tab
with tabs[2]:
    st.title("💬 Life GuardIANs Medical Chatbot")
    st.write("Chat with our AI-powered assistant about symptoms and healthcare access.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("You:")
    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            chatbot_reply = query_model(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", chatbot_reply))
    
    for role, text in st.session_state.chat_history:
        if role == "You":
            st.write(f"👤 **You**: {text}")
        else:
            st.write(f"🤖 **AI**: {text}")
# import streamlit as st
# import pandas as pd
# from huggingface_hub import InferenceApi
# import numpy as np
# from datetime import datetime
# from langchain import PromptTemplate, LLMChain
# from langchain.llms import HuggingFaceTextGenInference
# import googlemaps
# # Set Page Config First (Fix Streamlit Error)
# st.set_page_config(page_title="Life GuardIANs", page_icon="💙", layout="wide")

# # Load Doctolib Dataset
# df = pd.read_excel("doctorlib_dataset.xlsx", sheet_name="dataset")

# # Hugging Face API Setup
# API_KEY = "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"  # Replace with your actual API key
# MODEL_NAME = "BioMistral/BioMistral-7B"

# # Initialize Mistral LLM
# llm = HuggingFaceTextGenInference(
#     inference_server_url=f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
#     max_new_tokens=512,
#     top_k=10,
#     top_p=0.95,
#     temperature=0.7,
#     repetition_penalty=1.03,
#     api_key=API_KEY
# )
# # Google Maps API Setup (Replace with your API Key)
# GMAPS_API_KEY = "your_google_maps_api_key"
# gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# def get_nearest_doctors(patient_location, specialty):
#     """Finds the nearest doctors based on location and specialty."""
#     filtered_data = df[df["specialty"] == specialty]
#     if filtered_data.empty:
#         return None
    
#     # Simulate geolocation processing (replace with real geocoding API if needed)
#     results = [
#         {
#             "name": f"Dr. {row['specialty']} #{i+1}",
#             "address": row["practice_region"],
#             "waiting_days": row["median_waiting_days_dep"],
#             "distance_km": np.random.randint(1, 20)  # Placeholder for real distance
#         }
#         for i, row in filtered_data.iterrows()
#     ]
    
#     # Sort by distance first, then by shortest waiting time
#     sorted_results = sorted(results, key=lambda x: (x["distance_km"], x["waiting_days"]))
#     return sorted_results[:5]

# # Create medical analysis prompt template
# template = """You are an AI medical assistant specialized in symptom analysis and specialist referrals.
# Analyze the following symptoms and patient information, then provide:
# 1. Urgency Assessment (Emergency/Urgent/Non-urgent)
# 2. Recommended next steps (ER visit/GP consultation/Online consultation)
# 3. Most relevant medical specialties based on symptoms
# 4. Analysis of any patterns in patient history (if provided)

# Patient information and symptoms: {user_input}

# Please provide a structured response with clear recommendations:"""

# prompt = PromptTemplate(template=template, input_variables=["user_input"])
# chain = LLMChain(llm=llm, prompt=prompt)

# def get_medical_analysis(user_input):
#     """Get AI medical analysis and recommendations"""
#     try:
#         response = chain.run(user_input=user_input)
#         return response.strip()
#     except Exception as e:
#         return f"Error analyzing symptoms: {str(e)}"

# # Tabs for navigation
# tabs = st.tabs(["🏥 Patient Triage", "📊 Healthcare Access", "💬 Chatbot"])

# # Patient Triage Tab
# with tabs[0]:
#     st.title("🏥 Patient Triage Dashboard")
#     patient_data = pd.DataFrame({
#         "Patient ID": [f"PT-{i}" for i in range(1, 6)],
#         "Symptom Severity Score": [3, 8, 6, 9, 2],
#         "Recommendation": ["Teleconsultation", "Urgent Care", "Specialist", "Urgent Care", "Self-monitor"],
#     })
#     st.dataframe(patient_data)
#     st.bar_chart(patient_data.set_index("Patient ID")["Symptom Severity Score"])

# # Healthcare Access Tab
# with tabs[1]:
#     st.title("📊 Healthcare Access Analysis")
#     region = st.selectbox("Choose a region:", df["practice_region"].unique())
#     specialty = st.selectbox("Choose a specialty:", df["specialty"].unique())
#     patient_location = st.text_input("Enter your location (City, Address, or ZIP Code):")
    
#     if st.button("Find Nearest Doctor"):
#         if patient_location:
#             nearest_doctors = get_nearest_doctors(patient_location, specialty)
#             if nearest_doctors:
#                 st.write("### 🏥 Nearest Available Doctors:")
#                 for doc in nearest_doctors:
#                     st.write(f"**{doc['name']}** - {doc['address']} (⏳ {doc['waiting_days']} days waiting, 📍 {doc['distance_km']} km away)")
#             else:
#                 st.warning("No available doctors found for the selected specialty.")
#         else:
#             st.warning("Please enter your location to find the nearest doctor.")
    
#     st.metric(label="🩺 Available Doctors", value=df[df["specialty"] == specialty]["prats"].sum())
#     st.metric(label="⏳ Median Waiting Days", value=int(df[df["specialty"] == specialty]["median_waiting_days_dep"].mean()))
#     st.bar_chart(df[df["specialty"] == specialty].set_index("year")["median_waiting_days_dep"])

# # Conversational Chatbot Tab
# with tabs[2]:
#     st.title("💬 Life GuardIANs Medical Chatbot")
#     st.write("Chat with our AI-powered assistant about symptoms and healthcare access.")
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
    
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
    
#     if prompt := st.chat_input("Describe your symptoms and medical history..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)
        
#         with st.chat_message("assistant"):
#             with st.spinner("Analyzing your symptoms..."):
#                 analysis = get_medical_analysis(prompt)
#                 st.markdown(analysis)
#                 st.session_state.messages.append({"role": "assistant", "content": analysis})

# # Disclaimer
# st.markdown("---")
# st.caption("""
# ⚠️ **Important Disclaimer:** This is an AI-powered medical assistance tool for informational purposes only.
# In case of emergency, immediately contact emergency services or visit the nearest emergency room.
# Always consult with qualified healthcare professionals for medical advice.
# """)


