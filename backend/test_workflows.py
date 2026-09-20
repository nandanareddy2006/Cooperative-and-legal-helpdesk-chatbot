"""
End-to-End Verification Suite for Sahakaar Saathi:
1. Gemini Quota & Smart Multi-Tier Router Fix
2. Canonical Guided Procedures Catalog & Matching
3. Statutory Grievance Redressal Engine
4. ReportLab PDF Generation Engine
5. Unified End-to-End Workflow Orchestrator
6. FastAPI Endpoint Responses & PDF Streaming
"""

import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from backend.router import route_query, classify_rule_based
from backend.procedures import (
    get_all_procedures,
    get_procedure_by_id,
    match_procedure_by_query,
    PROCEDURES_CATALOG
)
from backend.grievance import (
    get_grievance_categories,
    generate_grievance_draft,
    GrievanceDraftRequest,
    GRIEVANCE_CATEGORIES
)
from backend.pdf_generator import (
    generate_grievance_pdf,
    generate_procedure_pdf
)
from backend.main import app, process_query


client = TestClient(app)


def test_hybrid_router():
    print("\n--- 1. Testing Hybrid Router & Zero-Quota Protection ---", flush=True)
    samples = [
        ("What is the weather today in Hyderabad?", "OUT_OF_SCOPE"),
        ("Who can vote in a cooperative society election?", "GOVERNANCE"),
        ("What are my legal rights as a member under Section 19?", "LEGAL_RIGHTS"),
        ("How do I register a new cooperative society?", "PROCEDURE"),
        ("The president embezzled society funds and I want to file a complaint", "GRIEVANCE"),
        ("How can society bye-laws be amended under Section 16?", "PROCEDURE"),
        ("Who is the prime minister of India?", "OUT_OF_SCOPE"),
    ]
    for q, expected in samples:
        cat = route_query(q)
        print(f"Query: '{q}'\n  -> Routed: {cat} (Expected: {expected})", flush=True)
        assert cat == expected, f"Expected {expected}, got {cat}"

    # Verify cache idempotency
    assert route_query("How do I register a new cooperative society?") == "PROCEDURE"
    print("Hybrid Router: ALL PASSED.", flush=True)


def test_procedures_catalog():
    print("\n--- 2. Testing Canonical Procedures System ---", flush=True)
    all_procs = get_all_procedures()
    print(f"Total canonical procedures available: {len(all_procs)}", flush=True)
    assert len(all_procs) >= 7, f"Expected at least 7 procedures, got {len(all_procs)}"
    for p in all_procs:
        print(f" - [{p['id']}] {p['title']} ({p['step_count']} steps, {p['document_count']} docs)", flush=True)

    for proc_id in ["registration", "agm", "elections", "dispute_filing", "membership", "bylaw_amendment", "audit_inspection"]:
        proc = get_procedure_by_id(proc_id)
        assert proc is not None, f"Procedure {proc_id} not found"
        assert len(proc["steps"]) >= 4, f"Procedure {proc_id} missing steps"
        assert len(proc["required_documents"]) >= 3, f"Procedure {proc_id} missing docs"

    print("Procedures System: ALL PASSED.", flush=True)


def test_grievance_system():
    print("\n--- 3. Testing Statutory Grievance System ---", flush=True)
    cats = get_grievance_categories()
    print(f"Available statutory grievance categories: {len(cats)}", flush=True)
    assert len(cats) >= 8, f"Expected 8 categories, got {len(cats)}"

    req = GrievanceDraftRequest(
        complainant_name="Srikanth Rao",
        complainant_address="H.No. 4-12, Karimnagar, Telangana",
        complainant_phone="9876543210",
        complainant_membership_no="MEM-842",
        society_name="Karimnagar Farmers Cooperative Credit Society",
        society_address="Main Road, Karimnagar",
        society_reg_no="CCS-1988/KM",
        category_id="FINANCIAL_IRREGULARITY",
        statement_of_facts=(
            "The managing committee released unsecured loans to ineligible non-members "
            "without board sanction, resulting in non-recovery of over Rs. 15 Lakhs. "
            "Despite repeated requests, no audit report or books were made available to members."
        ),
        relief_sought="Initiate statutory inquiry under Section 51 and surcharge proceedings under Section 60."
    )

    draft = generate_grievance_draft(req)
    print(f"Subject Line: {draft.subject_line}", flush=True)
    print(f"Addressed to: {draft.addressed_to}", flush=True)
    print(f"Required enclosures: {len(draft.required_enclosures)}", flush=True)
    assert "Section 60" in draft.subject_line
    assert "Srikanth Rao" in draft.formal_letter
    assert len(draft.required_enclosures) >= 4
    print("Grievance System: ALL PASSED.", flush=True)


def test_pdf_generation():
    print("\n--- 4. Testing ReportLab PDF Generation Engine ---", flush=True)

    # A: Test Procedure PDF
    proc = get_procedure_by_id("registration")
    assert proc is not None
    proc_pdf = generate_procedure_pdf(proc)
    print(f"Generated Procedure PDF size: {len(proc_pdf)} bytes", flush=True)
    assert isinstance(proc_pdf, bytes)
    assert len(proc_pdf) > 2000
    assert proc_pdf[:4] == b"%PDF", "Generated file is not a valid PDF header"

    # B: Test Grievance Petition PDF
    req = GrievanceDraftRequest(
        complainant_name="Nagaraju Goud",
        complainant_address="Warangal, Telangana",
        complainant_phone="9123456789",
        complainant_membership_no="MEM-104",
        society_name="Warangal Weavers Cooperative Society",
        society_address="Hanamkonda, Warangal",
        category_id="MEMBERSHIP_DENIAL",
        statement_of_facts="The society managing committee refused my application without giving any reason under Section 19.",
        relief_sought="Direct the society to admit me as an active member."
    )
    draft = generate_grievance_draft(req)
    griev_pdf = generate_grievance_pdf(draft.model_dump(), req.model_dump())
    print(f"Generated Grievance Petition PDF size: {len(griev_pdf)} bytes", flush=True)
    assert isinstance(griev_pdf, bytes)
    assert len(griev_pdf) > 2000
    assert griev_pdf[:4] == b"%PDF", "Generated file is not a valid PDF header"

    print("PDF Generation: ALL PASSED.", flush=True)


def test_workflow_orchestrator():
    print("\n--- 5. Testing End-to-End Workflow Orchestrator ---", flush=True)

    # A: Out of scope (short-circuits with 0 quota consumed)
    res_oos = process_query("What is the recipe for Hyderabadi biryani?")
    assert res_oos["category"] == "OUT_OF_SCOPE"
    assert res_oos["workflow"] == "out_of_scope_guard"
    assert "Sahakaar Saathi" in res_oos["answer"]
    assert len(res_oos["suggested_followups"]) > 0

    # B: Procedure matching
    res_proc = process_query("How do I register a new cooperative society?")
    assert res_proc["category"] == "PROCEDURE"
    assert res_proc["workflow"] == "procedure_guidance"
    assert res_proc["procedure"] is not None
    assert res_proc["procedure"]["id"] == "registration"
    assert res_proc["pdf_url"] == "/procedures/registration/download-pdf"

    # C: Grievance matching
    res_griev = process_query("The committee illegally rejected my membership application")
    assert res_griev["category"] == "GRIEVANCE"
    assert res_griev["workflow"] == "grievance_redressal"
    assert res_griev["grievance_suggestion"] is not None
    assert res_griev["grievance_suggestion"]["category_id"] == "MEMBERSHIP_DENIAL"

    # D: Governance question
    res_gov = process_query("Who can vote in managing committee elections?")
    assert res_gov["category"] == "GOVERNANCE"
    assert len(res_gov["suggested_followups"]) > 0

    # E: Legal Rights
    res_rights = process_query("What are the legal rights of a member to inspect accounts under Section 114?")
    assert res_rights["category"] == "LEGAL_RIGHTS"

    print("Workflow Orchestrator: ALL PASSED.", flush=True)


def test_fastapi_endpoints():
    print("\n--- 6. Testing FastAPI Endpoints & PDF Streaming ---", flush=True)

    # Health & Root
    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

    # Procedures Endpoints
    res_procs = client.get("/procedures")
    assert res_procs.status_code == 200
    assert len(res_procs.json()) >= 7

    res_proc_single = client.get("/procedures/registration")
    assert res_proc_single.status_code == 200
    assert res_proc_single.json()["id"] == "registration"

    # Procedure PDF Download Stream
    res_proc_pdf = client.get("/procedures/registration/download-pdf")
    assert res_proc_pdf.status_code == 200
    assert res_proc_pdf.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in res_proc_pdf.headers.get("content-disposition", "")
    assert res_proc_pdf.content[:4] == b"%PDF"

    # Grievance Categories & Draft
    res_cats = client.get("/grievance/categories")
    assert res_cats.status_code == 200
    assert len(res_cats.json()) >= 8

    req_payload = {
        "complainant_name": "Ramesh Reddy",
        "complainant_address": "Secunderabad, Telangana",
        "society_name": "Secunderabad Cooperative Bank",
        "society_address": "MG Road, Secunderabad",
        "category_id": "RECORDS_DENIAL",
        "statement_of_facts": "The Secretary refused to allow me to inspect audited balance sheets."
    }
    res_draft = client.post("/grievance/draft", json=req_payload)
    assert res_draft.status_code == 200
    assert "RECORDS_DENIAL" in res_draft.json()["category_id"]

    # Grievance PDF Download Stream
    res_griev_pdf = client.post("/grievance/download-pdf", json=req_payload)
    assert res_griev_pdf.status_code == 200
    assert res_griev_pdf.headers["content-type"] == "application/pdf"
    assert res_griev_pdf.content[:4] == b"%PDF"

    # Ask & Chat Endpoints
    res_ask = client.post("/ask", json={"question": "What are my voting rights?"})
    assert res_ask.status_code == 200
    assert "answer" in res_ask.json()

    res_chat = client.post("/chat", json={"message": "How do I register a new society?"})
    assert res_chat.status_code == 200
    assert res_chat.json()["category"] == "PROCEDURE"

    print("FastAPI Endpoints: ALL PASSED.", flush=True)


if __name__ == "__main__":
    test_hybrid_router()
    test_procedures_catalog()
    test_grievance_system()
    test_pdf_generation()
    test_workflow_orchestrator()
    test_fastapi_endpoints()
    print("\n[SUCCESS] ALL 6 TEST SUITES PASSED FLAWLESSLY!", flush=True)
