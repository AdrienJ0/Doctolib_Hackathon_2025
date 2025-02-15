from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Load the model and tokenizer
MODEL_NAME = "BioMistral/BioMistral-7B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    torch_dtype=torch.float16, 
    device_map="auto"
)

class ChatRequest(BaseModel):
    conversation: list[str]  # List of past messages
    max_length: int = 200

@app.get("/")
def home():
    return {"message": "BioMistral-7B Chatbot API is running!"}

@app.post("/chat")
def chat(request: ChatRequest):
    conversation = "\n".join(request.conversation) + "\nAI: "
    inputs = tokenizer(conversation, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=request.max_length)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": response}
