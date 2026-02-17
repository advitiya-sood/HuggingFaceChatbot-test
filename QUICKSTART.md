# 🚀 Quick Start Guide - FastAPI Backend

## Start the API Server

```bash
# Make sure you're in the project directory
cd "c:\Users\sood1\OneDrive\Desktop\AI Engg\RAG chatbot\HuggingFaceChatbot-test"

# Start the server
uvicorn api:app --reload
```

## Access the API

Once the server is running, open your browser:

1. **Swagger UI (Interactive Docs):** http://localhost:8000/docs
2. **API Base URL:** http://localhost:8000

## Test the API

### Option 1: Use Swagger UI
1. Go to http://localhost:8000/docs
2. Click on `/api/query/advanced`
3. Click "Try it out"
4. Enter your question
5. Click "Execute"

### Option 2: Run Test Script
```bash
# In a new terminal
python test_api.py
```

## Integrate with Frontend

```javascript
const response = await fetch('http://localhost:8000/api/query/advanced', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: "Who is the CEO?",
    top_k: 3,
    summarize: true
  })
});

const data = await response.json();
console.log(data.answer);
console.log(data.sources);
```

## That's it! Your RAG API is ready! 🎉
