import os
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.rag_answer import answer_query, get_out_of_scope_response
from backend.router import route_query
from backend.procedures import (
    get_all_procedures,
    get_procedure_by_id,
    match_procedure_by_query
)
from backend.grievance import (
    get_grievance_categories,
    generate_grievance_draft,
    GrievanceDraftRequest,
    GrievanceDraftResponse,
    GRIEVANCE_CATEGORIES
)
from backend.pdf_generator import (
    generate_grievance_pdf,
    generate_procedure_pdf
)

app = FastAPI(
    title="Sahakaar Saathi API",
    description="Cooperative Governance, Legal Helpdesk, Canonical Procedures & Grievance Redressal AI",
    version="2.0.0"
)

# Enable CORS for web frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: Optional[str] = None
    message: Optional[str] = None
    jurisdiction: str = "Telangana"
    language: str = "English"


class AskResponse(BaseModel):
    question: str
    jurisdiction: str
    category: str
    workflow: str
    answer: str
    language: str = "English"
    procedure: Optional[Dict[str, Any]] = None
    grievance_suggestion: Optional[Dict[str, Any]] = None
    pdf_url: Optional[str] = None
    suggested_followups: List[str] = Field(default_factory=list)


@app.get("/")
def root():
    return {
        "project": "Sahakaar Saathi",
        "status": "running",
        "version": "2.0.0",
        "jurisdiction": "Telangana",
        "modules": [
            "Smart Multi-Tier Query Router (Zero-Quota Fast Path)",
            "Chroma RAG Retrieval & Structured Extractive Fallback",
            "Statutory Grievance Redressal & Representation Generator",
            "Canonical Cooperative Guided Procedures Engine",
            "ReportLab Legal PDF Generation & Export Engine"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Sahakaar Saathi",
        "procedures_available": len(get_all_procedures()),
        "grievance_categories": len(get_grievance_categories())
    }


# ==========================================
# GUIDED PROCEDURES ENDPOINTS
# ==========================================

@app.get("/procedures")
def list_procedures():
    """List all available canonical cooperative procedures."""
    return get_all_procedures()


@app.get("/procedures/{procedure_id}")
def get_procedure(procedure_id: str):
    """Retrieve full step-by-step checklist, timeline, and document requirements."""
    proc = get_procedure_by_id(procedure_id)
    if not proc:
        raise HTTPException(status_code=404, detail=f"Procedure '{procedure_id}' not found.")
    return proc


@app.get("/procedures/{procedure_id}/download-pdf")
def download_procedure_pdf(procedure_id: str):
    """Generate and stream a print-ready PDF manual for the specified procedure."""
    proc = get_procedure_by_id(procedure_id)
    if not proc:
        raise HTTPException(status_code=404, detail=f"Procedure '{procedure_id}' not found.")
    
    try:
        pdf_bytes = generate_procedure_pdf(proc)
        filename = f"Procedure_Guide_{procedure_id.upper()}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate procedure PDF: {str(e)}")


# ==========================================
# GRIEVANCE SYSTEM ENDPOINTS
# ==========================================

@app.get("/grievance/categories")
def list_grievance_categories():
    """List all 8 statutory grievance categories under Telangana Act 1964."""
    return get_grievance_categories()


@app.post("/grievance/draft", response_model=GrievanceDraftResponse)
def draft_grievance(request: GrievanceDraftRequest):
    """Generate a legally grounded complaint / representation letter."""
    try:
        return generate_grievance_draft(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/grievance/download-pdf")
def download_grievance_pdf(request: GrievanceDraftRequest):
    """Generate and download an official statutory petition / representation PDF."""
    try:
        draft = generate_grievance_draft(request)
        pdf_bytes = generate_grievance_pdf(draft.model_dump(), request.model_dump())
        safe_name = "".join(c for c in request.society_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"Grievance_Petition_{safe_name.replace(' ', '_')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate grievance PDF: {str(e)}")


# ==========================================
# UNIFIED WORKFLOW ORCHESTRATOR
# ==========================================

def process_query(query_text: str, jurisdiction: str = "Telangana", language: str = "English") -> dict:
    query_clean = query_text.strip()
    if not query_clean:
        return {
            "question": "",
            "jurisdiction": jurisdiction,
            "category": "GENERAL",
            "workflow": "general",
            "answer": "Please ask a question regarding cooperative society governance, legal rights, procedures, or disputes.",
            "language": language,
            "procedure": None,
            "grievance_suggestion": None,
            "pdf_url": None,
            "suggested_followups": [
                "How do I register a new cooperative society?",
                "What are my voting rights in elections?",
                "How do I file a dispute under Section 61?"
            ]
        }

    # Step 1: Hybrid Routing (Fast regex + LRU Cache + Quota-safe LLM)
    category = route_query(query_clean)

    procedure_data = None
    grievance_data = None
    pdf_url = None
    suggested_followups = []

    # Step 2: Intent-based Workflow Orchestration
    if category == "OUT_OF_SCOPE":
        # Short-circuit: saves 100% LLM quota and vector search latency
        answer = get_out_of_scope_response(language)
        workflow = "out_of_scope_guard"
        suggested_followups = [
            "How do I become a cooperative member?",
            "What are member voting rights?",
            "How to file a complaint against society management?"
        ]

    elif category == "PROCEDURE":
        workflow = "procedure_guidance"
        matched_proc = match_procedure_by_query(query_clean)
        if matched_proc:
            procedure_data = matched_proc
            pdf_url = f"/procedures/{matched_proc['id']}/download-pdf"
            suggested_followups = [
                f"What documents are required for {matched_proc['title']}?",
                f"What is the statutory timeline for {matched_proc['title']}?",
                "How do I file an appeal if my application is delayed?"
            ]
        else:
            suggested_followups = [
                "How do I register a new cooperative society?",
                "How do I conduct an Annual General Meeting?",
                "What is the procedure for committee elections?"
            ]

        answer = answer_query(
            query=query_clean,
            jurisdiction=jurisdiction,
            language=language,
            pre_routed_category="PROCEDURE"
        )

    elif category == "GRIEVANCE":
        workflow = "grievance_redressal"
        q_lower = query_clean.lower()
        matched_cat = None
        
        if "membership" in q_lower or "reject" in q_lower or "admit" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["MEMBERSHIP_DENIAL"]
        elif "election" in q_lower or "vote" in q_lower or "tamper" in q_lower or "nominat" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["ELECTION_MALPRACTICE"]
        elif "fund" in q_lower or "corrupt" in q_lower or "money" in q_lower or "surcharge" in q_lower or "embezzle" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["FINANCIAL_IRREGULARITY"]
        elif "account" in q_lower or "book" in q_lower or "inspect" in q_lower or "minutes" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["RECORDS_DENIAL"]
        elif "agm" in q_lower or "meeting" in q_lower or "annual" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["FAILURE_TO_HOLD_AGM"]
        elif "expel" in q_lower or "expulsion" in q_lower or "disqualif" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["ARBITRARY_EXPULSION"]
        elif "loan" in q_lower or "recovery" in q_lower or "attach" in q_lower or "auction" in q_lower:
            matched_cat = GRIEVANCE_CATEGORIES["UNLAWFUL_LOAN_RECOVERY"]
        else:
            matched_cat = GRIEVANCE_CATEGORIES["GENERAL_DISPUTE"]

        if matched_cat:
            grievance_data = {
                "category_id": matched_cat["id"],
                "category_title": matched_cat["title"],
                "act_sections": matched_cat["act_sections"],
                "authority": matched_cat["authority"],
                "limitation_period": matched_cat.get("limitation_period", "Within statutory period"),
                "sample_relief": matched_cat.get("sample_relief", "")
            }

        suggested_followups = [
            "Draft a formal grievance letter for this issue",
            "What evidence and documents should I attach to my complaint?",
            "Which statutory authority has jurisdiction over this dispute?"
        ]

        answer = answer_query(
            query=query_clean,
            jurisdiction=jurisdiction,
            language=language,
            pre_routed_category="GRIEVANCE"
        )

    elif category == "GOVERNANCE":
        workflow = "governance_advisory"
        suggested_followups = [
            "What are the qualifications and disqualifications for directors?",
            "What is the quorum requirement for General Body meetings?",
            "How can bye-laws of a cooperative society be amended?"
        ]
        answer = answer_query(
            query=query_clean,
            jurisdiction=jurisdiction,
            language=language,
            pre_routed_category="GOVERNANCE"
        )

    elif category == "LEGAL_RIGHTS":
        workflow = "legal_rights_advisory"
        suggested_followups = [
            "Can a member inspect society books and audited balance sheets?",
            "What are the statutory grounds for membership expulsion?",
            "What remedies exist under Section 61 for member grievances?"
        ]
        answer = answer_query(
            query=query_clean,
            jurisdiction=jurisdiction,
            language=language,
            pre_routed_category="LEGAL_RIGHTS"
        )

    else:
        workflow = "legal_rag_retrieval"
        suggested_followups = [
            "How do I register a new cooperative society?",
            "What are my statutory rights as a member?",
            "How do I file a dispute under Section 61?"
        ]
        answer = answer_query(
            query=query_clean,
            jurisdiction=jurisdiction,
            language=language,
            pre_routed_category=category
        )

    return {
        "question": query_clean,
        "jurisdiction": jurisdiction,
        "category": category,
        "workflow": workflow,
        "answer": answer,
        "language": language,
        "procedure": procedure_data,
        "grievance_suggestion": grievance_data,
        "pdf_url": pdf_url,
        "suggested_followups": suggested_followups
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