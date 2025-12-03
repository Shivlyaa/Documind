# DocuMind – Retrieval-Augmented Study Assistant

Transform any PDF into an interactive chat experience. Built to demonstrate production-grade RAG with clean architecture, semantic retrieval, and cloud deployment.

Live Demo  
https://foolish-bookings-179959.framer.app/

---

## What it does

1. Accepts a PDF upload
2. Extracts and chunks document text
3. Converts chunks to embeddings
4. Performs semantic retrieval using FAISS
5. Builds a context-aware query for the LLM
6. Returns grounded, concise answers only from the provided document

Use cases:
• Unit summaries from a syllabus
• Concept explanations and comparisons
• Study guidance powered by document context
• Safe fallback responses for irrelevant questions

---

## Tech Stack

Backend: FastAPI (Python)  
Frontend: Framer  
Vector Store: FAISS  
Embeddings: SentenceTransformers  
LLM: Llama 3.1 Instruct (inference API)  
Deployment: Docker + Google Cloud Run  
CI/CD: GitHub → Cloud Build → Cloud Run

---

## Architecture

User → Framer UI → FastAPI → Text Extraction and Chunking → Embeddings → FAISS Semantic Search → Context Builder → LLM → Final Response

Autoscaling serverless deployment with request-driven billing.

---

## Skills Demonstrated

• RAG system design  
• Prompt engineering and grounding strategies  
• Cloud deployment (containerized backend)  
• REST API development  
• Integrating LLMs into real products  
• Frontend to backend orchestration  
• Environment and secret management

---

## Example Interactions (for demo screenshots)

• What does Unit 3 cover
• Explain Pushdown Automata like I am 5
• Difference between DFA and regular expressions
• What will I learn by the end of this course
• Which unit covers Context Free Languages

Each demonstrates correct retrieval and structured reasoning grounded in syllabus context.

(Screenshots included in /screenshots directory)

---

## Run Locally

Clone:
git clone https://github.com/<your-username>/DocuMind
cd DocuMind/backend

Setup environment:
cp .env.example .env

Install:
pip install -r requirements.txt

Run:
uvicorn main:app --reload --port 8000

Swagger:
http://localhost:8000/docs

---

## Deployment Notes

• Backend is containerized and deployed to Cloud Run  
• CI/CD triggers from GitHub via Cloud Build  
• Framer frontend connected through REST endpoints  
• CORS configured for public access

---

## Known Limitations

• Single-document session context  
• Basic reranking and evaluation  
• No multi-user identity or persistence

Planned improvements:
• Multi-document knowledge store
• Metadata-based retrieval ranking
• Source citations inline
• Authentication and user sessions

---

## Author

Shiv  
AI / GenAI Engineering  
Open to internship roles in AI (Remote or Delhi NCR)  
LinkedIn:https://www.linkedin.com/in/shiv-pratap-singh-734a7928b?utm_source=share_via&utm_content=profile&utm_medium=member_ios) 
Email: shivpratapconnect@gmail.com



## Summary Pitch

Production-deployed RAG system using FastAPI, FAISS, SentenceTransformers, and Llama 3.1. Demonstrates real-world retrieval pipelines, clean API design, and cloud deployment with Modern GenAI product UX.
