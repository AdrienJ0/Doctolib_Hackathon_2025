from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import spacy
import os
import requests
from spacy.cli import download

# Load medical NER model
download("en_core_web_md")
nlp = spacy.load("en_core_web_md")  # Ensure model is installed separately

# Use a smaller transformer model like distilGPT-2
MODEL_NAME = "BioMistral/BioMistral-7B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,  # Use float32 for CPU compatibility
    device_map="cpu",  # Ensure it's on the CPU
    offload_folder="offload_dir"
)

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

def generate_response(prompt: str) -> str:
    """Generates a response using the smaller transformer model."""
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")  # Move to CPU for smaller model
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

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
    
    try:
        response_text = generate_response(prompt)
        formatted_response = restrict_response_format(response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
    
    return {"response": formatted_response}
