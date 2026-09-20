import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag_answer import answer_query
from backend.router import route_query


app = FastAPI(
    title="Sahakaar Saathi",
    description="Cooperative Governance & Legal Helpdesk",
    version="0.1.0"
)

# Enable CORS so browser frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str | None = None
    message: str | None = None
    jurisdiction: str = "Telangana"
    language: str = "English"

class AskResponse(BaseModel):
    question: str
    jurisdiction: str
    category: str
    answer: str
    language: str = "English"


@app.get("/")
def root():
    return {
        "project": "Sahakaar Saathi",
        "status": "running",
        "message": "Cooperative Governance & Legal Helpdesk API"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


def process_query(query_text: str, jurisdiction: str = "Telangana", language: str = "English") -> dict:
    try:
        category = route_query(query_text)
    except Exception as e:
        category = "GENERAL"

    try:
        answer = answer_query(query_text, jurisdiction=jurisdiction)
    except Exception as e:
        answer = (
            f"Unable to generate response: {str(e)}\n\n"
            "Please verify that your GOOGLE_API_KEY is properly set in your .env file."
        )

    return {
        "question": query_text,
        "jurisdiction": jurisdiction,
        "category": category,
        "answer": answer,
        "language": language
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    query_text = request.question or request.message or ""
    return process_query(
        query_text=query_text,
        jurisdiction=request.jurisdiction,
        language=request.language
    )


@app.post("/chat", response_model=AskResponse)
def chat(request: AskRequest):
    query_text = request.message or request.question or ""
    return process_query(
        query_text=query_text,
        jurisdiction=request.jurisdiction,
        language=request.language
    )