# 🤖 CoreAssist AI

CoreAssist AI is an internal AI assistant designed to help employees quickly access company knowledge through semantic search and Retrieval-Augmented Generation (RAG).

Instead of manually searching through documents or internal tools, users can ask natural language questions such as:

> "How do I request time off?"
> "Who works in Software Engineering?"
> "Where can I find the onboarding procedure?"

The assistant retrieves relevant context from internal data sources and generates contextual answers using Gemini AI.

---

# ✨ Features

- 🔎 Semantic search with embeddings
- 📄 PDF RAG pipeline
- 🧠 Gemini AI generated responses
- 👥 Contacts knowledge base
- 📚 Dynamic source selection
- ⚡ FastAPI backend
- 🎨 Streamlit SaaS-style frontend
- 🗂 PostgreSQL vector storage
- 🔗 Modular RAG architecture

---

# 🧠 Architecture

CoreAssist AI combines:

- FastAPI for backend APIs
- PostgreSQL for structured data & embeddings
- Gemini API for embeddings + answer generation
- Streamlit for the frontend interface
- RAG pipeline for contextual responses

Current supported sources:

- Contacts database
- Internal PDF documents

---

# 🛠 Tech Stack

## Backend
- Python
- FastAPI
- SQLModel
- PostgreSQL

## AI / RAG
- Gemini API
- Embeddings
- Semantic Search
- Cosine Similarity

## Frontend
- Streamlit

## PDF Processing
- pdfplumber

---

# 📂 Project Structure

```bash
app/
├── api/
├── rag/
├── database/
├── models/
├── services/
├── embeddings/
└── main.py
```
# 🚀 Installation

## Clone repository

git clone https://github.com/Leticia-Temmar/coreassist-ai.git
cd coreassist-ai

# Create virtual environment

python -m venv venv
source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

# Configure environment variables
```env
DATABASE_URL=your_postgresql_url
GOOGLE_API_KEY=your_gemini_api_key
```
# Run FastAPI backend 
uvicorn app.main:app --reload

# Run Streamlit frontend

streamlit run streamlit_app.py

# API Routes

/ask/contacts-rag : RAG over contacts database
/ask/pdf-rag : RAG over PDF documents

# Roadmap

 - [ ] Conversation memory
 - [ ] Hybrid search
 - [ ] Multi-document upload
 - [ ] Authentication system
 - [ ] Vector database optimization
 - [ ] Docker deployment
 - [ ] Cloud deployment
# 👩‍💻 Author

Leticia Temmar
Data & AI student focused on:
- Data Engineering
- Data Analysis
- Data Science
- RAG Systems
- AI Applications
- Cloud & Modern Data Architectures