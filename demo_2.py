import os
import hashlib
import requests
import PyPDF2
from cryptography.fernet import Fernet
import spacy
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env (for local development) or directly from environment variables
load_dotenv()

# Fetch Vault secrets (like encryption key) from environment variables
secret_key = os.getenv("SECRET_KEY")
if secret_key is None:
    raise ValueError("SECRET_KEY environment variable is missing")

cipher = Fernet(secret_key)

# Load medical NER model
from spacy.cli import download
download("en_core_web_md")
nlp = spacy.load("en_core_web_md")

# Load transformer model
MODEL_NAME = "BioMistral/BioMistral-7B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Set up the FastAPI endpoint URL
API_URL = "http://localhost:8006/chat"  # Assuming FastAPI is running locally

# FastAPI Code
app = FastAPI()

# Function to decrypt data
def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data using symmetric encryption (Fernet)."""
    decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

# Function to hash sensitive data for identification
def hash_data(data: str) -> str:
    """Generate a SHA-256 hash for sensitive data."""
    return hashlib.sha256(data.encode()).hexdigest()

# Function to anonymize personal data (simple example)
def anonymize_data(text: str) -> str:
    """Anonymize PII in the text using simple techniques (e.g., replacing names)."""
    text = text.replace("John Doe", "[REDACTED]")
    text = text.replace("123-45-6789", "[REDACTED]")
    return text

# Function to detect medical specialty from a message (basic example)
def detect_specialty(message: str) -> str:
    """Detect medical specialty based on user message."""
    # You can expand this based on a specific NER or logic for detecting specialties
    if "heart" in message or "chest" in message:
        return "cardiology"
    elif "stomach" in message or "digestion" in message:
        return "gastroenterology"
    else:
        return "general"

# Function to generate AI response using the transformer model
def generate_response(prompt: str) -> str:
    """Generate response using transformer model."""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# FastAPI request body model
class ChatRequest(BaseModel):
    conversation: list[str]
    pdf_text: str

@app.post("/chat")
def chat(request: ChatRequest):
    if not request.conversation:
        raise HTTPException(status_code=400, detail="Conversation is empty")
    
    # Decrypt conversation and pdf_text
    decrypted_conversation = [decrypt_data(message) for message in request.conversation]
    decrypted_pdf_text = decrypt_data(request.pdf_text)

    # Anonymize data
    anonymized_conversation = [anonymize_data(message) for message in decrypted_conversation]
    anonymized_pdf_text = anonymize_data(decrypted_pdf_text)

    # Process the conversation and generate a response
    user_message = anonymized_conversation[-1]
    specialty = detect_specialty(user_message)
    prompt = f"You are an AI medical assistant specializing in {specialty}. " + "\n".join(anonymized_conversation) + "\nAI:"
    response = generate_response(prompt)
    
    return {"response": response}

# Streamlit App Code

# Encrypt data before sending
def encrypt_data(data: str) -> str:
    """Encrypt data using symmetric encryption (Fernet)."""
    return cipher.encrypt(data.encode()).decode()

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file) -> str:
    """Extracts text from the provided PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to call FastAPI endpoint
def get_chatbot_response(conversation: list[str], pdf_text: str) -> str:
    """Send conversation and PDF text to FastAPI backend and retrieve the response."""
    encrypted_conversation = [encrypt_data(message) for message in conversation]
    encrypted_pdf_text = encrypt_data(pdf_text)
    response = requests.post(API_URL, json={"conversation": encrypted_conversation, "pdf_text": encrypted_pdf_text})
    if response.status_code == 200:
        return response.json().get("response", "Error")
    else:
        return "Error calling API."

# Main Streamlit app
def main():
    st.title("Medical Chatbot with Existing Record")
    conversation = []

    # Step 1: Ask user if they have a medical record
    have_record = st.radio("Do you have a medical record?", ("Yes", "No"))
    
    if have_record == "Yes":
        # Step 2: Upload the medical record PDF
        pdf_file = st.file_uploader("Upload a medical record PDF", type="pdf")
        
        if pdf_file:
            # Step 3: Extract text from the PDF
            extracted_text = extract_text_from_pdf(pdf_file)
            anonymized_text = anonymize_data(extracted_text)  # Anonymize data
            st.write("Extracted text from medical record:")
            st.text_area("PDF Text", anonymized_text, height=200)

            # Store extracted text in session state
            st.session_state.extracted_text = extracted_text

            # Initialize conversation if not already initialized
            if "conversation" not in st.session_state:
                st.session_state.conversation = []

            # Step 4: Ask a series of questions
            if "question_index" not in st.session_state:
                st.session_state.question_index = 0  # Track which question we're on
                st.session_state.responses = []  # Store the user's responses

            if st.session_state.question_index < len(st.session_state.questions):
                question = st.session_state.questions[st.session_state.question_index]
                user_response = st.text_input(question)

                # After receiving the user's response, process it
                if user_response:
                    st.session_state.responses.append(user_response)
                    st.session_state.question_index += 1  # Move to the next question

                    # Append user response to the conversation
                    st.session_state.conversation.append(f"Q: {question}")
                    st.session_state.conversation.append(f"A: {user_response}")

                    # Display the updated conversation so far
                    if st.session_state.conversation:
                        for i, message in enumerate(st.session_state.conversation):
                            st.write(message)

            # After all questions are answered, show the final response
            if st.session_state.question_index == len(st.session_state.questions):
                # Send complete conversation and PDF text to FastAPI backend
                chatbot_response = get_chatbot_response(
                    st.session_state.conversation, st.session_state.extracted_text
                )
                st.write(f"Chatbot: {chatbot_response}")

        else:
            st.warning("Please upload a medical record PDF to proceed.")

    else:
        st.write("Please upload a medical record to proceed.")

# Initialize questions for the conversation
st.session_state.questions = [
    "What are your symptoms?",
    "How long have you been experiencing these symptoms?",
    "Do you have any pre-existing conditions?",
    "Have you seen a doctor recently?",
    "Are you on any medication?",
    "What is your address? City and street?"
]

if __name__ == "__main__":
    main()
