from fastapi import FastAPI
from pydantic import BaseModel

from backend.rag_answer import answer_query
from backend.router import route_query


app = FastAPI(
    title="Sahakaar Saathi",
    description="Cooperative Governance & Legal Helpdesk",
    version="0.1.0"
)


class AskRequest(BaseModel):
    question: str
    jurisdiction: str = "Telangana"

class AskResponse(BaseModel):
    question: str
    jurisdiction: str
    category: str
    answer: str


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


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    category = route_query(request.question)

    answer = answer_query(
        request.question,
        jurisdiction=request.jurisdiction
    )

    return {
    "question": request.question,
    "jurisdiction": request.jurisdiction,
    "category": category,
    "answer": answer
}