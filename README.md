# 🤖 RAG Chatbot — Complete Project Documentation

> **Who is this for?** This guide assumes you are brand new to Python and web development. Every concept is explained from the ground up.

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [How Does It Work? (The Big Picture)](#2-how-does-it-work-the-big-picture)
3. [Technologies Used](#3-technologies-used)
4. [Project Structure](#4-project-structure)
5. [Step-by-Step: How a Question Gets Answered](#5-step-by-step-how-a-question-gets-answered)
6. [Setting Up the Project (First Time)](#6-setting-up-the-project-first-time)
7. [Running the Project](#7-running-the-project)
8. [API Endpoints Reference](#8-api-endpoints-reference)
9. [Frontend (Chat UI)](#9-frontend-chat-ui)
10. [Configuration & Environment Variables](#10-configuration--environment-variables)
11. [Common Errors & Fixes](#11-common-errors--fixes)

---

## 1. What Is This Project?

This is an **AI-powered chatbot** that can answer questions about company documents — things like HR policies, leave rules, employee benefits, and more.

Instead of a generic AI that makes up answers, this chatbot **reads your actual company documents** and gives answers based only on what is written in those files. This technique is called **RAG** — _Retrieval-Augmented Generation_.

**What the user experiences:**
- A chat bubble appears on the bottom-right corner of a webpage.
- The user clicks it, types a question like *"What is the leave policy?"*
- The chatbot reads the company's PDF/Word/Excel documents and replies with an accurate, sourced answer in seconds.

---

## 2. How Does It Work? (The Big Picture)

Think of this like a very smart librarian:

```
┌─────────────────────────────────────────────────────────────┐
│                     ONE-TIME SETUP                          │
│                                                             │
│  Your Documents (PDF, Word, Excel, etc.)                    │
│        │                                                    │
│        ▼                                                    │
│  Documents are split into small "chunks" of text            │
│        │                                                    │
│        ▼                                                    │
│  Each chunk is turned into a list of numbers (embedding)    │
│        │                                                    │
│        ▼                                                    │
│  Numbers are saved in a "vector database" (FAISS)           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  EVERY TIME A USER ASKS A QUESTION          │
│                                                             │
│  User asks: "What is the leave policy?"                     │
│        │                                                    │
│        ▼                                                    │
│  The question is also turned into numbers (embedding)       │
│        │                                                    │
│        ▼                                                    │
│  FAISS finds the document chunks most similar to the Q      │
│        │                                                    │
│        ▼                                                    │
│  Those chunks + the question are sent to an LLM (Groq AI)  │
│        │                                                    │
│        ▼                                                    │
│  LLM generates a human-friendly answer with citations       │
│        │                                                    │
│        ▼                                                    │
│  Answer appears in the chat widget on the website           │
└─────────────────────────────────────────────────────────────┘
```

**In plain English:**
- We first process all company documents and store their meaning as numbers.
- When a user asks something, we find the most relevant passages using math (similarity search).
- We hand those passages to a powerful AI model (LLaMA via Groq) and ask it to write an answer.
- The AI answers **only from the given context** — it doesn't make things up.

---

## 3. Technologies Used

### 🐍 Backend (Python)

| Technology | What it Does | Why We Use It |
|---|---|---|
| **Python** | Programming language for the backend | Easy to read, massive AI/ML ecosystem |
| **FastAPI** | Web framework that creates the API server | Fast, modern, auto-generates API docs |
| **Uvicorn** | Runs the FastAPI server | Lightweight async server for Python |
| **LangChain** | Toolkit for building LLM-powered apps | Handles document loaders, text splitting |
| **Groq + LLaMA 3** | The AI brain (Large Language Model) | Free API, very fast inference |
| **FAISS** | Vector database for similarity search | Efficient nearest-neighbour search by Meta |
| **Sentence Transformers** | Converts text to numbers (embeddings) | `paraphrase-MiniLM-L3-v2` model |
| **PyPDF / python-docx** | Read PDF and Word documents | Parse company documents |
| **SlowAPI** | Rate limiting middleware | Prevents API abuse |
| **Pydantic** | Data validation | Ensures API inputs/outputs are correct |
| **python-dotenv** | Load secrets from `.env` file | Keep API keys out of source code |

### ⚛️ Frontend (JavaScript)

| Technology | What it Does | Why We Use It |
|---|---|---|
| **React** | JavaScript UI library | Component-based, reactive UI |
| **Vite** | Development server & build tool | Extremely fast, modern tooling |
| **Vanilla CSS** | Styling | Full design control, no extra dependencies |

### ☁️ External Services

| Service | Purpose |
|---|---|
| **Groq Cloud** | Hosts the LLaMA 3 AI model — free API |
| **Vercel** | Deploys the React frontend |
| **Render** | Deploys the Python backend |

---

## 4. Project Structure

```
RAG chatbot/
│
├── HuggingFaceChatbot-test/      ← Python Backend
│   ├── api.py                    ← Main API file (entry point)
│   ├── main.py                   ← Alternative entry point
│   ├── requirements.txt          ← Python packages list
│   ├── runtime.txt               ← Python version for deployment
│   ├── render.yaml               ← Render.com deployment config
│   ├── startup.py                ← Pre-startup script for deployment
│   ├── rebuild_index.py          ← Script to rebuild FAISS index
│   ├── .env                      ← Secret keys (NEVER commit this!)
│   ├── .gitignore                ← Files Git should ignore
│   │
│   ├── src/                      ← Core logic modules
│   │   ├── __init__.py           ← Makes src/ a Python package
│   │   ├── data_loader.py        ← Reads PDF/Word/Excel/CSV/JSON files
│   │   ├── embedding.py          ← Splits text & creates embeddings
│   │   ├── vectorstore.py        ← Manages FAISS vector database
│   │   └── search.py             ← RAG pipeline logic (the brain!)
│   │
│   ├── data/                     ← Your company documents go here
│   │   └── (PDF, Word, Excel, CSV, JSON files)
│   │
│   ├── faiss_store/              ← Auto-generated: stores the vector index
│   │   ├── faiss.index           ← The vector index file
│   │   └── metadata.pkl          ← Which chunk belongs to which document
│   │
│   └── notebook/                 ← Jupyter notebooks for experimentation
│
└── bhavna-frontend/              ← React Frontend
    ├── index.html                ← HTML entry point
    ├── package.json              ← Node.js packages list
    ├── vite.config.js            ← Vite configuration
    ├── .env.local                ← Local API URL (dev)
    ├── .env.production           ← Production API URL
    │
    └── src/
        ├── main.jsx              ← React entry point
        ├── App.jsx               ← Root component
        ├── index.css             ← Global styles
        ├── components/
        │   ├── ChatWidget.jsx    ← The floating chat bubble & window
        │   ├── Hero.jsx          ← Landing page hero section
        │   └── Features.jsx      ← Features section
        └── styles/
            ├── ChatWidget.css    ← Chat UI styles
            ├── Hero.css          ← Hero section styles
            └── Features.css      ← Features section styles
```

---

## 5. Step-by-Step: How a Question Gets Answered

Here is the **detailed data flow** — what happens when a user types a question:

### Phase 1 — Document Indexing (Runs Once at Startup)

```
data/ folder
    │
    ▼  src/data_loader.py
Reads all PDF, TXT, CSV, Excel, Word, JSON files
    │
    ▼  src/embedding.py  →  EmbeddingPipeline.chunk_documents()
Splits each document into overlapping chunks
(chunk_size=1000 characters, overlap=200 characters)
Why overlap? So no important sentence gets cut off at a boundary.
    │
    ▼  src/embedding.py  →  EmbeddingPipeline.embed_chunks()
Uses SentenceTransformer ("paraphrase-MiniLM-L3-v2") to convert
each text chunk into a 384-dimensional vector (list of numbers)
    │
    ▼  src/vectorstore.py  →  FaissVectorStore.build_from_documents()
Adds all vectors to a FAISS index (L2 distance index)
Saves:
  • faiss_store/faiss.index     ← the vectors
  • faiss_store/metadata.pkl    ← source file names & page numbers
```

### Phase 2 — Answering a Question (Runs Every Request)

```
User types: "What is the casual leave entitlement?"
    │
    ▼  ChatWidget.jsx (Frontend)
Sends HTTP POST to /api/query/advanced
Body: { question, top_k: 5, conversation_history: [...] }
    │
    ▼  api.py  →  query_advanced() endpoint
Rate limit check: 10 requests/minute per IP
    │
    ▼  src/search.py  →  AdvancedRAGPipeline.query()
Step 1: _is_out_of_scope() — is this a greeting? (hello, hi, bye...)
         If yes → use LLM to give a friendly redirect message
         If no → continue to RAG
    │
    ▼  src/vectorstore.py  →  FaissVectorStore.query()
The question is embedded into a vector using SentenceTransformer
FAISS searches for the 5 most similar document chunks
Returns chunks with distance scores
    │
    ▼  src/search.py (continued)
Convert distances → similarity scores (score = 1 / (1 + distance))
Build context string from the top chunks
Build the prompt:
  "You are an HR assistant. Use the context below to answer..."
  + conversation history (last 3 turns)
  + retrieved context
  + current question
    │
    ▼  Groq API  →  ChatGroq.invoke(prompt)
LLaMA 3.1 (8B) generates the answer in ~1-2 seconds
    │
    ▼  src/search.py (post-processing)
• Add citation: "[1] filename.pdf (page 3)"
• Generate 2 follow-up questions the user might want to ask
• Optionally generate a 3-4 sentence summary
• Save Q&A to history[]
    │
    ▼  api.py (response)
Returns JSON:
  {
    "question": "...",
    "answer": "...",
    "sources": [{ source, page, score, preview }],
    "summary": null,
    "follow_up_questions": ["...", "..."],
    "timestamp": "..."
  }
    │
    ▼  ChatWidget.jsx (Frontend renders)
• Parses markdown (**bold**, *italic*, bullet points)
• Shows citation with hover tooltip (passage preview)
• Renders follow-up question chips the user can click
• Keeps conversation history for context in next question
```

---

## 6. Setting Up the Project (First Time)

### Prerequisites

Before you begin, make sure the following are installed:

| Tool | What it is | Download Link |
|---|---|---|
| **Python 3.12** | Programming language | [python.org](https://python.org) |
| **Node.js 18+** | JavaScript runtime for the frontend | [nodejs.org](https://nodejs.org) |
| **Git** | Version control | [git-scm.com](https://git-scm.com) |
| **VS Code** (optional) | Code editor | [code.visualstudio.com](https://code.visualstudio.com) |

> **What is `pip`?** `pip` is Python's package manager. Just like an app store, it downloads and installs Python libraries for you. It comes bundled with Python.

> **What is `npm`?** `npm` is Node.js's package manager. Same idea, but for JavaScript.

---

### Step 1: Get a Free Groq API Key

The chatbot uses Groq's AI service (free tier available).

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key (it starts with `gsk_...`)

---

### Step 2: Set Up the Python Backend

Open **PowerShell** or **Command Prompt** and run these commands one by one:

```powershell
# Navigate to the backend folder
cd "c:\Users\sood1\OneDrive\Desktop\AI Engg\RAG chatbot\HuggingFaceChatbot-test"

# Create a virtual environment
# A virtual environment is an isolated Python installation for this project only.
# This prevents package conflicts with other projects.
python -m venv .venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate
# You should see (.venv) appear at the start of your terminal prompt.

# Install all required packages
pip install -r requirements.txt
# This reads requirements.txt and installs every library listed.
# This may take 5-10 minutes the first time.
```

#### Create the `.env` file

The `.env` file stores secrets that should never be shared publicly.

```powershell
# Create or open the .env file in the backend folder
# It should contain exactly this (replace with your actual key):
GROQ_API_KEY="gsk_YourActualKeyHere"

# Optional: add allowed frontend origins (default already includes localhost)
CORS_ORIGINS="http://localhost:5173,http://localhost:3000"
```

> ⚠️ **Important:** Never commit `.env` to Git. It's already listed in `.gitignore` to protect you.

#### Add Your Documents

Drop your company documents into the `data/` folder:

```
HuggingFaceChatbot-test/
└── data/
    ├── leave_policy.pdf
    ├── employee_handbook.docx
    ├── benefits.xlsx
    └── any_other_file.txt
```

Supported formats: **PDF, Word (.docx), Excel (.xlsx), CSV, TXT, JSON**

---

### Step 3: Set Up the React Frontend

```powershell
# Navigate to the frontend folder
cd "c:\Users\sood1\OneDrive\Desktop\AI Engg\RAG chatbot\bhavna-frontend"

# Install all Node.js packages
npm install
# This reads package.json and installs React, Vite, etc.
```

The `.env.local` file should point to the backend:

```
VITE_API_URL=http://localhost:8000
```

This is already configured. No changes needed for local development.

---

## 7. Running the Project

You need **two terminals** open simultaneously — one for the backend, one for the frontend.

### Terminal 1 — Start the Backend

```powershell
cd "c:\Users\sood1\OneDrive\Desktop\AI Engg\RAG chatbot\HuggingFaceChatbot-test"

# Activate virtual environment first (if not already active)
.venv\Scripts\activate

# Start the API server
uvicorn api:app --reload --port 8000
```

**What happens:**
1. FastAPI starts up on `http://localhost:8000`
2. It checks if `faiss_store/faiss.index` exists
3. If **not found** → reads all files from `data/`, creates embeddings, builds the FAISS index (takes ~1-5 minutes depending on document sizes)
4. If **found** → loads the existing index instantly
5. Server is ready. You'll see: `Application startup complete.`

> 💡 **What is `--reload`?** It means the server automatically restarts whenever you change a Python file. Great for development.

### Terminal 2 — Start the Frontend

```powershell
cd "c:\Users\sood1\OneDrive\Desktop\AI Engg\RAG chatbot\bhavna-frontend"

npm run dev
```

**What happens:**
- Vite starts a development server on `http://localhost:5173`
- Open that URL in your browser
- You'll see the landing page with a blue chat bubble in the bottom-right corner

### ✅ Verify Everything Works

1. Open `http://localhost:8000/docs` — you should see the FastAPI Swagger UI with all endpoints
2. Open `http://localhost:5173` — you should see the landing page
3. Click the chat bubble and type: *"What is the leave policy?"*

---

## 8. API Endpoints Reference

The backend exposes these HTTP endpoints:

### `GET /health`
**Purpose:** Check if the server is running  
**Rate Limit:** None  
**Response:**
```json
{ "status": "healthy", "version": "1.0.0", "timestamp": "2024-..." }
```

---

### `POST /api/query/basic`
**Purpose:** Simple question → answer (no citations)  
**Rate Limit:** 20 requests/minute per IP  
**Request Body:**
```json
{
  "question": "What are the working hours?",
  "top_k": 3
}
```
**Response:**
```json
{
  "question": "What are the working hours?",
  "answer": "Working hours are 9 AM to 6 PM...",
  "timestamp": "2024-..."
}
```

---

### `POST /api/query/advanced`
**Purpose:** Full RAG pipeline — returns answer, citations, follow-up questions  
**Rate Limit:** 10 requests/minute per IP  
**Request Body:**
```json
{
  "question": "How many days of casual leave do I get?",
  "top_k": 5,
  "min_score": 0.0,
  "summarize": false,
  "stream": false,
  "conversation_history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help?" }
  ]
}
```
**Response:**
```json
{
  "question": "How many days of casual leave do I get?",
  "answer": "Employees are entitled to 12 days of casual leave per year...\n\nCitation:\n[1] leave_policy.pdf (page 2)",
  "sources": [
    {
      "source": "leave_policy.pdf",
      "page": 2,
      "score": 0.87,
      "preview": "Casual leave policy: Employees get 12 days..."
    }
  ],
  "summary": null,
  "follow_up_questions": [
    "Can casual leave be carried forward?",
    "How do I apply for casual leave?"
  ],
  "timestamp": "2024-..."
}
```

---

### `GET /api/history`
**Purpose:** Get all past Q&A pairs from the current session  

### `DELETE /api/history`
**Purpose:** Clear the session history  

### `GET /docs`
**Purpose:** Interactive API documentation (Swagger UI) — auto-generated by FastAPI

---

## 9. Frontend (Chat UI)

The frontend is a single-page React application with three main sections:

### Components

#### `ChatWidget.jsx` — The Chat Interface

This is the most important frontend file. It manages:

| Feature | How It Works |
|---|---|
| **Chat bubble toggle** | Click the 💬 button to open/close the chat window |
| **Starter questions** | Three preset questions appear when chat is first opened |
| **Sending messages** | HTTP POST to `/api/query/advanced` |
| **Conversation memory** | Keeps last 6 messages and sends them with each request for context |
| **Markdown rendering** | Parses `**bold**`, `*italic*`, bullet/numbered lists |
| **Citation display** | Shows source file and page, with hover tooltip previewing the passage |
| **Follow-up questions** | Clickable chip buttons appear after each bot response |
| **Copy button** | Copies the answer text (strips citation line) |
| **Rate limit handling** | Shows friendly message when 429 error occurs |
| **Typing indicator** | Three animated dots while waiting for response |
| **Character limit** | Input capped at 200 characters with live counter |

#### `Hero.jsx` — Landing Page

Simple hero section with headline, description, and a "Get Started" button.

#### `Features.jsx` — Features Section

Displays feature highlights of the chatbot.

### How the Frontend Talks to the Backend

```javascript
// From ChatWidget.jsx
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

fetch(`${API_URL}/api/query/advanced`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question, top_k: 5, conversation_history })
})
```

`import.meta.env.VITE_API_URL` reads from the `.env.local` file automatically. In production, it reads from `.env.production`.

---

## 10. Configuration & Environment Variables

### Backend `.env` File

Located at: `HuggingFaceChatbot-test/.env`

```env
# Required: Your Groq API key
GROQ_API_KEY="gsk_..."

# Optional: Which frontend URLs are allowed to call the API
# Default covers all localhost ports
CORS_ORIGINS="http://localhost:5173,https://your-production-site.vercel.app"
```

### Frontend `.env.local` (Development)

Located at: `bhavna-frontend/.env.local`

```env
VITE_API_URL=http://localhost:8000
```

### Frontend `.env.production` (Production/Deployed)

Located at: `bhavna-frontend/.env.production`

```env
VITE_API_URL=https://your-backend.onrender.com
```

### Model Configuration

These values are set in `src/search.py` and can be changed:

| Parameter | Default Value | Description |
|---|---|---|
| `embedding_model` | `paraphrase-MiniLM-L3-v2` | SentenceTransformer model for embeddings |
| `llm_model` | `llama-3.1-8b-instant` | Groq AI model used for generation |
| `chunk_size` | `1000` | Max characters per document chunk |
| `chunk_overlap` | `200` | Characters shared between consecutive chunks |
| `top_k` (default) | `5` | Number of document chunks retrieved per query |

---

## 11. Common Errors & Fixes

### ❌ `ModuleNotFoundError: No module named 'src'`
**Cause:** You ran the server from the wrong folder  
**Fix:** Make sure you are inside `HuggingFaceChatbot-test/` when running `uvicorn`

```powershell
cd "c:\Users\sood1\OneDrive\Desktop\AI Engg\RAG chatbot\HuggingFaceChatbot-test"
uvicorn api:app --reload --port 8000
```

---

### ❌ `AuthenticationError: Invalid API key`
**Cause:** Your Groq API key is wrong or missing  
**Fix:** Check `.env` file — make sure `GROQ_API_KEY` is set correctly with no spaces around `=`

```env
GROQ_API_KEY="gsk_your_actual_key_here"
```

---

### ❌ `CORS error` in browser console
**Cause:** The backend doesn't recognize your frontend's origin  
**Fix:** Add your frontend URL to `CORS_ORIGINS` in `.env`

```env
CORS_ORIGINS="http://localhost:5173,http://localhost:3000"
```

---

### ❌ FAISS index not being rebuilt after adding new documents
**Fix:** Delete the old index and restart the server, or run the rebuild script:

```powershell
# Option 1: Delete and let server rebuild automatically
Remove-Item -Recurse -Force faiss_store

# Option 2: Run the rebuild script explicitly
python rebuild_index.py
```

---

### ❌ `pip install` fails on Windows
**Cause:** Some packages (like `faiss-cpu`) need Visual C++ Build Tools  
**Fix:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

---

### ❌ Chat says "trouble connecting to the server"
**Cause:** Backend is not running, or running on a different port  
**Fix:**
1. Check Terminal 1 — is the backend running?
2. Check that `VITE_API_URL` in `.env.local` matches the backend port

---

### ❌ Rate limit exceeded (429 error)
**Cause:** Too many requests in a short time  
**Limits:**
- Basic endpoint: 20 requests/minute
- Advanced endpoint: 10 requests/minute  

**Fix:** Wait 60 seconds and try again. These limits prevent API abuse.

---

## Quick Reference Card

```
📁 Add documents    →  HuggingFaceChatbot-test/data/
🔑 Set API key      →  HuggingFaceChatbot-test/.env
🐍 Start backend    →  uvicorn api:app --reload --port 8000
⚛️  Start frontend  →  npm run dev  (inside bhavna-frontend/)
🌐 Backend URL      →  http://localhost:8000
🌐 Frontend URL     →  http://localhost:5173
📖 API docs         →  http://localhost:8000/docs
🔄 Rebuild index    →  python rebuild_index.py
```

---

*Documentation generated for the RAG Chatbot project — February 2026*
