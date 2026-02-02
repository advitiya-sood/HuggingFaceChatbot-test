import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests  # We use 'requests' directly to bypass SSL checks

app = FastAPI()

# --- CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOUR API KEY
HF_TOKEN = "" 




# The Model URL (We call the API directly now)
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

PDF_CONTEXT = """
BRAND NAME: SMIK
ABOUT: SMIK is a premium clothing brand focusing on aesthetic streetwear.
PRODUCTS:
- Threads of Destiny Tee: 100% Cotton, Oversized fit. Price: $45.
- Shadow Hoodie: Heavyweight fleece. Price: $80.
RETURN POLICY: 30-day returns for unworn items.
SHIPPING: Free shipping on orders over $100.
CONTACT: support@smik.com
"""

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Construct the prompt
    prompt = f"""
    You are a helpful customer support assistant for a brand named SMIK.
    Use the context below to answer the user's question. Keep answers short and friendly.
    
    CONTEXT:
    {PDF_CONTEXT}
    
    USER QUESTION:
    {request.question}
    
    ANSWER:
    """

    # --- THE FIX: RAW REQUEST WITH verify=False ---
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    try:
        # verify=False forces Python to IGNORE the certificate error
        response = requests.post(API_URL, headers=headers, json=payload, verify=False)
        
        # Check if Hugging Face gave us an error (like loading)
        if response.status_code != 200:
            return {"answer": f"Error from AI: {response.text}"}
            
        # Parse the answer
        result = response.json()
        
        # Hugging Face returns a list, we want the text
        if isinstance(result, list) and 'generated_text' in result[0]:
            # Clean up the response (remove the prompt part)
            full_text = result[0]['generated_text']
            answer_only = full_text.split("ANSWER:")[-1].strip()
            return {"answer": answer_only}
        else:
            return {"answer": str(result)}

    except Exception as e:
        print(f"Error: {e}")
        return {"answer": "I'm having trouble connecting. Please try again."}

@app.get("/health")
def health_check():
    return {"status": "active"}