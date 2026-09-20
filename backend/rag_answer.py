import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.rag_retriever import retrieve_documents

load_dotenv()

FALLBACK_MODELS = [
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]


def get_gemini_client(model_name: str):
    """Safely obtain a ChatGoogleGenerativeAI instance with fast timeout."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.startswith("AQ.") or "your_" in api_key.lower():
        return None
    try:
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1,
            google_api_key=api_key,
            request_timeout=3,
            max_retries=1
        )
    except Exception:
        return None


def get_out_of_scope_response(language: str = "English") -> str:
    """Friendly response for queries outside the cooperative helpdesk scope."""
    if language.lower() == "telugu" or "తెలుగు" in language:
        return (
            "నమస్కారం! సహకార సారథి (Sahakaar Saathi) కేవలం సహకార సంఘాల పాలన, నిబంధనలు, "
            "చట్టపరమైన హక్కులు, మరియు వివాద పరిష్కారానికి సంబంధించిన సమాచారాన్ని మాత్రమే అందిస్తుంది.\n\n"
            "దయచేసి తెలంగాణ సహకార సంఘాల చట్టం (1964), సంఘాల ఎన్నికలు, సభ్యత్వం, లేదా ఫిర్యాదుల ప్రక్రియ గురించి ప్రశ్నలు అడగండి."
        )
    elif language.lower() == "hindi" or "हिन्दी" in language:
        return (
            "नमस्ते! सहकार साथी (Sahakaar Saathi) केवल सहकारी समितियों के प्रशासन, नियमों, "
            "कानूनी अधिकारों और शिकायत निवारण में सहायता के लिए समर्पित है।\n\n"
            "कृपया तेलंगाना सहकारी समिति अधिनियम, 1964, चुनाव, सदस्यता, या प्रक्रिया से संबंधित प्रश्न पूछें।"
        )
    else:
        return (
            "Namaste! **Sahakaar Saathi** is specifically designed to provide assistance for **cooperative society governance, legal rights, guided procedures, and grievance redressal** under the *Telangana Cooperative Societies Act, 1964*.\n\n"
            "Your question appears to be outside this domain. Please ask about:\n"
            "- Voting and election rights in cooperative societies\n"
            "- How to register a new cooperative society\n"
            "- How to file a dispute or grievance under Section 61\n"
            "- Rights to inspect books, accounts, and audit reports\n"
            "- Procedures for conducting Annual General Body Meetings (AGM)"
        )


def generate_extractive_fallback(query: str, documents: list, jurisdiction: str = "Telangana") -> str:
    """
    Direct statutory extract fallback when Gemini API is rate-limited or quota-exhausted.
    Extracts high-relevance paragraphs directly from the indexed Telangana Act PDF.
    """
    if not documents:
        return (
            f"No direct legal provisions were found in the {jurisdiction} Cooperative Societies statutory records "
            f"matching your query: '{query}'. Please check your search terms or refer to the guided procedures section."
        )

    parts = [
        "### 📜 Statutory Reference from Telangana Cooperative Societies Act, 1964\n",
        "*(Extracted directly from statutory provisions — Zero-Quota Legal RAG Mode)*\n"
    ]

    for i, doc in enumerate(documents[:4], start=1):
        source = doc.metadata.get("source_file", "Telangana Cooperative Societies Act, 1964")
        page = doc.metadata.get("page", "N/A")
        content = doc.page_content.strip()
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        snippet = " ".join(lines[:6])
        if len(lines) > 6:
            snippet += "..."

        parts.append(
            f"**Statutory Provision {i}** — *Page {page}* (`{source}`):\n"
            f"> {snippet}\n"
        )

    parts.append(
        "\n⚖️ **Legal Disclaimer:** This guidance is grounded in the official provisions of the Telangana Cooperative Societies Act, 1964 for educational and helpdesk reference. "
        "For formal representation before the Registrar or Tribunal, please consult authorized legal counsel or use our Grievance Drafting tool."
    )

    return "\n".join(parts)


def answer_query(
    query: str,
    jurisdiction: str = "Telangana",
    language: str = "English",
    pre_routed_category: Optional[str] = None
) -> str:
    """
    Answers user question using RAG retrieval with quota protection and multi-model fallback.
    """
    jurisdiction = jurisdiction.strip() if jurisdiction else "Telangana"

    # If already known out of scope, return scope notice immediately without vector retrieval
    if pre_routed_category == "OUT_OF_SCOPE":
        return get_out_of_scope_response(language)

    documents = retrieve_documents(
        query,
        k=5,
        jurisdiction=jurisdiction
    )

    context_parts = []
    for doc in documents:
        page = doc.metadata.get("page")
        source = doc.metadata.get("source_file")
        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Text:\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    lang_instruction = f"Provide the answer in {language}." if language and language.lower() != "english" else "Answer in English."

    prompt = f"""You are Sahakaar Saathi, an expert cooperative governance and legal helpdesk assistant.

Answer the user's question using ONLY the legal source material provided below from the Telangana Cooperative Societies Act, 1964.

Rules:
1. Do not invent legal provisions or hallucinate sections.
2. If the sources do not contain enough information, state what is available and clarify clearly.
3. Mention the relevant page number(s) and Act sections when present in the sources.
4. Do not present the answer as a substitute for professional legal advice.
5. Keep the answer structured, clear, and actionable with bullet points and bold headers.
6. {lang_instruction}

SELECTED JURISDICTION:
{jurisdiction}

LEGAL SOURCES:
{context}

USER QUESTION:
{query}"""

    # Try Gemini models in sequence with graceful quota fallback
    for model_name in FALLBACK_MODELS:
        llm = get_gemini_client(model_name)
        if not llm:
            continue
        try:
            response = llm.invoke(prompt)
            if response and response.content:
                return response.content.strip()
        except Exception as e:
            err_str = str(e).lower()
            # If quota or rate-limited, try next model or drop to extractive fallback
            if "429" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
                continue
            continue

    # If all LLM calls were exhausted or failed, fall back to pure extractive RAG
    return generate_extractive_fallback(query, documents, jurisdiction)


if __name__ == "__main__":
    test_q = "Who can vote in a cooperative society general election?"
    print("\nTesting RAG Answer:")
    ans = answer_query(test_q)
    print(ans)