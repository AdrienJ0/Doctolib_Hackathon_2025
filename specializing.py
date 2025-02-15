from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import spacy

# Load medical NER model
nlp = spacy.load("en_core_med7_lg")  # Requires installation of `en_core_med7_lg`

# Mapping keywords to medical specialties
MEDICAL_SPECIALTIES = {
    "heart": "Cardiology",
    "lungs": "Pulmonology",
    "brain": "Neurology",
    "diabetes": "Endocrinology",
    "pain": "General Medicine",
    "infection": "Infectious Disease",
    "cancer": "Oncology",
    "skin": "Dermatology"
}

RESPONSE_CATEGORIES = {
    "summary": "Summarize the patient's symptoms clearly and concisely.",
    "next_steps": "Provide the next recommended actions (e.g., visit a doctor, monitor symptoms, check parameters).",
    "actions": "Suggest a specialty and potential doctors, or take an action (e.g., book an appointment)."
}

app = FastAPI()

class ChatRequest(BaseModel):
    conversation: list[str]

def detect_specialty(text: str) -> str:
    """Extracts medical terms and assigns the closest specialty."""
    doc = nlp(text)
    for ent in doc.ents:
        for keyword, specialty in MEDICAL_SPECIALTIES.items():
            if keyword in ent.text.lower():
                return specialty
    return "General Medicine"

def restrict_response_format(response_text: str) -> str:
    """Ensure response follows one of the three categories and avoids diagnosis or prescriptions."""
    restricted_phrases = ["diagnosis", "prescribe", "medication", "drug"]
    for phrase in restricted_phrases:
        if phrase in response_text.lower():
            return "I'm sorry, but I cannot provide a diagnosis or prescribe medication. Please consult a medical professional."
    for category, instruction in RESPONSE_CATEGORIES.items():
        if category in response_text.lower():
            return response_text
    return "I'm sorry, but I can only provide a summary, next steps, or suggested actions. Please clarify your question."

@app.post("/chat")
def chat(request: ChatRequest):
    if not request.conversation:
        raise HTTPException(status_code=400, detail="Conversation is empty")
    
    # Get last user message
    user_message = request.conversation[-1]
    specialty = detect_specialty(user_message)
    
    # Modify prompt with controlled response types
    prompt = (f"You are an AI medical assistant specializing in {specialty}. "
              "Your responses must be strictly within these categories:\n"
              "1. Summary of symptoms\n"
              "2. Next steps (e.g., book appointment, check parameters)\n"
              "3. Suggested actions (e.g., suggest a doctor, book an appointment)\n"
              "\n"
              "You cannot provide a diagnosis or prescribe medication. Your role is to offer general guidance and suggest next steps.\n"
              "\n"
              "Important: You are not a real doctor and do not have medical authority. Your responses should always remind users to consult a healthcare professional for actual medical decisions.\n"
              "\n\n"
              + "\n".join(request.conversation) + "\nAI:")
    
    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    formatted_response = restrict_response_format(response["choices"][0]["message"]["content"])
    
    return {"response": formatted_response}
