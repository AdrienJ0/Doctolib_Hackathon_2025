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

@app.post("/chat")
def chat(request: ChatRequest):
    if not request.conversation:
        raise HTTPException(status_code=400, detail="Conversation is empty")
    
    # Get last user message
    user_message = request.conversation[-1]
    specialty = detect_specialty(user_message)
    
    # Modify prompt with detected specialty
    prompt = (f"You are an AI medical assistant specializing in {specialty}. "
              "Answer the patient's question in a clear and empathetic way.\n\n"
              + "\n".join(request.conversation) + "\nAI:")
    
    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 or GPT-3.5
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"response": response["choices"][0]["message"]["content"]}
