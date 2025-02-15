import streamlit as st
import requests
import time
import PyPDF2

# Set up the FastAPI endpoint URL
API_URL = "http://localhost:8006/chat"  # Assuming FastAPI is running locally

# Function to call the FastAPI endpoint
def get_chatbot_response(conversation: list[str], pdf_text: str) -> str:
    """Sends conversation and PDF text to the FastAPI backend and retrieves the response."""
    response = requests.post(API_URL, json={"conversation": conversation, "pdf_text": pdf_text})
    if response.status_code == 200:
        return response.json().get("response", "Error")
    else:
        return "Error calling API."

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file) -> str:
    """Extracts text from the provided PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

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
            st.write("Extracted text from medical record:")
            st.text_area("PDF Text", extracted_text, height=200)

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
                # Send complete conversation and PDF text to the FastAPI backend
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
    "Are you on any medication?"
    "What is your address ? City and street ?"
]

if __name__ == "__main__":
    main()
