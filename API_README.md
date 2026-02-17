# RAG Chatbot API

Production-ready REST API for the Advanced RAG Pipeline with citations, history tracking, and summarization.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your GROQ_API_KEY
```

### 3. Run the API
```bash
# Development mode (with auto-reload)
uvicorn api:app --reload

# Production mode
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 4. Access the API
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

---

## 📚 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-17T00:24:22+05:30"
}
```

---

### Basic Query
```http
POST /api/query/basic
Content-Type: application/json

{
  "question": "Who is the CEO of Bhavna corp?",
  "top_k": 3
}
```

**Response:**
```json
{
  "question": "Who is the CEO of Bhavna corp?",
  "answer": "Unmesh Mehta is the Founder and CEO...",
  "timestamp": "2026-02-17T00:24:22+05:30"
}
```

---

### Advanced Query
```http
POST /api/query/advanced
Content-Type: application/json

{
  "question": "Who is the CEO of Bhavna corp?",
  "top_k": 3,
  "min_score": 0.0,
  "stream": false,
  "summarize": true
}
```

**Response:**
```json
{
  "question": "Who is the CEO of Bhavna corp?",
  "answer": "Unmesh Mehta is the Founder and CEO...\n\nCitations:\n[1] handbook.pdf (page 4)",
  "sources": [
    {
      "source": "Employee Handbook_Bhavna Corp_2.0 (1).pdf",
      "page": 4,
      "score": 0.6923,
      "preview": "Unmesh Mehta is the Founder..."
    }
  ],
  "summary": "Unmesh Mehta is the CEO. He has 30+ years experience.",
  "timestamp": "2026-02-17T00:24:22+05:30"
}
```

---

### Get History
```http
GET /api/history
```

**Response:**
```json
{
  "history": [
    {
      "question": "Who is the CEO?",
      "answer": "Unmesh Mehta...",
      "sources": [...],
      "summary": "..."
    }
  ],
  "count": 1
}
```

---

### Clear History
```http
DELETE /api/history
```

**Response:**
```json
{
  "message": "History cleared successfully",
  "timestamp": "2026-02-17T00:24:22+05:30"
}
```

---

## 🧪 Testing with cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Basic Query
```bash
curl -X POST http://localhost:8000/api/query/basic \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is the CEO?", "top_k": 3}'
```

### Advanced Query
```bash
curl -X POST http://localhost:8000/api/query/advanced \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Who is the CEO?",
    "top_k": 3,
    "summarize": true
  }'
```

---

## 🎨 Frontend Integration

### JavaScript/React Example
```javascript
const API_BASE_URL = 'http://localhost:8000';

async function queryRAG(question) {
  const response = await fetch(`${API_BASE_URL}/api/query/advanced`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
      top_k: 3,
      summarize: true
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
const result = await queryRAG("Who is the CEO?");
console.log(result.answer);
console.log(result.sources);
```

---

## 🔧 Configuration

### CORS Origins
Edit `.env` to add your frontend URL:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://your-frontend.com
```

### Port Configuration
```bash
# Change port
uvicorn api:app --port 8080
```

---

## 📦 Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Render/Railway
1. Push code to GitHub
2. Connect repository to Render/Railway
3. Set environment variables
4. Deploy!

---

## 🐛 Troubleshooting

### CORS Errors
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Restart the API server

### Import Errors
```bash
# Make sure you're in the project directory
cd HuggingFaceChatbot-test

# Install dependencies
pip install -r requirements.txt
```

### FAISS Index Not Found
- Run `python main.py` first to build the FAISS index
- Or add documents to the `data/` folder

---

## 📝 API Features

- ✅ RESTful API with FastAPI
- ✅ Automatic API documentation (Swagger UI)
- ✅ CORS enabled for frontend integration
- ✅ Request/response validation with Pydantic
- ✅ Error handling and logging
- ✅ Health check endpoint
- ✅ Both basic and advanced RAG options
- ✅ Query history management

---

## 🎯 Next Steps

1. **Test locally** with Swagger UI at http://localhost:8000/docs
2. **Integrate with frontend** using the JavaScript example
3. **Deploy to production** using Docker or cloud platform
4. **Add authentication** for production use
5. **Monitor performance** and optimize as needed
