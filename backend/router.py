import re
import os
from typing import Optional, Dict
from functools import lru_cache
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

VALID_CATEGORIES = {
    "GOVERNANCE",
    "LEGAL_RIGHTS",
    "PROCEDURE",
    "GRIEVANCE",
    "GENERAL",
    "OUT_OF_SCOPE",
}

ROUTER_PROMPT = """You are the query router for Sahakaar Saathi, a cooperative governance and legal helpdesk.

Classify the user's question into exactly ONE category:

GOVERNANCE:
Questions about cooperative society elections, voting, committee members, board of directors, general body meetings, quorum, office bearers, or administration.

LEGAL_RIGHTS:
Questions about legal rights, duties, protections, statutory entitlements, rights to inspect books/accounts, or legal provisions under the Cooperative Societies Act.

PROCEDURE:
Questions asking how to perform a cooperative society procedure, including society registration, convening AGM, filing disputes, bye-law amendments, or required documents checklist.

GRIEVANCE:
Questions describing a dispute, complaint, violation, fraud, embezzlement, membership denial, election malpractice, unfair action, or asking how to file a statutory grievance/petition.

GENERAL:
General questions or definitions related to cooperative societies that do not clearly belong to the categories above.

OUT_OF_SCOPE:
Questions completely unrelated to cooperative societies, governance, agriculture, housing societies, or legal/procedural helpdesk (e.g., weather, sports, movies, cooking, coding, general trivia).

Return ONLY the category name.

USER QUESTION:
{question}"""

# Deterministic regex patterns to classify questions with zero latency and 0 API quota usage
OUT_OF_SCOPE_PATTERNS = [
    r"\b(weather|temperature|forecast|rain|climate)\b",
    r"\b(cricket|football|fifa|ipl|nba|tennis|olympic|world cup)\b",
    r"\b(movie|cinema|actor|actress|hollywood|bollywood|netflix|song|music|singer)\b",
    r"\b(recipe|cook|food|restaurant|biryani|pizza|burger|bake)\b",
    r"\b(code|python|javascript|java|c\+\+|html|css|bug|regex|programming|sql query)\b",
    r"\b(crypto|bitcoin|ethereum|forex trading|stock market ticker)\b",
    r"\b(capital of|who is the prime minister of|who is the president of|elon musk|taylor swift)\b",
    r"\b(game|gaming|playstation|xbox|pubg|freefire)\b",
    r"\b(joke|riddle|poem|story about aliens)\b",
]

GRIEVANCE_PATTERNS = [
    r"\b(grievance|complain|complaint|dispute|illegal|fraud|corruption|corrupt)\b",
    r"\b(embezzle|misappropriat|surcharge|tamper|cheating|bribe|scam|mismanagement)\b",
    r"\b(rejected my membership|denied my membership|expel|expulsion|arbitrary|unfair)\b",
    r"\b(section 60|section 61|section 51|tribunal|arbitrat|refuse to show accounts)\b",
    r"\b(not holding agm|failure to hold agm|violation of rights|misconduct)\b",
    r"\b(file a complaint|draft a petition|legal notice|demand justice)\b",
]

PROCEDURE_PATTERNS = [
    r"\b(how to|steps to|step-by-step|procedure for|procedure to|how do i|how can|how is|how are)\b",
    r"\b(how to register|how to start a|how to form a|register a society|registration process)\b",
    r"\b(documents required|checklist of documents|what documents|forms needed|form a|form b|form i|form c)\b",
    r"\b(conduct agm|conduct meeting|conduct election|apply for membership|process of|steps for)\b",
    r"\b(amend.*bye-law|amendment of bye-law|byelaw.*amendment|byelaw change)\b",
]

LEGAL_RIGHTS_PATTERNS = [
    r"\b(legal rights|my rights|right of member|entitled to|entitlement|statutory right)\b",
    r"\b(inspection of books|inspect records|copy of accounts|audit rights|right to information)\b",
    r"\b(section 19|section 21|section 114|section 115|section 116)\b",
    r"\b(what are my rights|protection against expulsion|right to receive dividend)\b",
]

GOVERNANCE_PATTERNS = [
    r"\b(who can vote|voting rights|vote in|elections?|general body|managing committee)\b",
    r"\b(quorum|term of office|board of directors|president|secretary|office bearers?)\b",
    r"\b(bylaws?|bye-laws?|amendment of bylaws?|disqualification|section 30|section 31|section 32)\b",
    r"\b(powers of registrar|powers of managing committee|tenure of committee)\b",
]

# In-memory session cache for fast router lookups
_ROUTER_CACHE: Dict[str, str] = {}


def classify_rule_based(question: str) -> Optional[str]:
    """
    Zero-latency, quota-free deterministic classification.
    Returns matched category or None if ambiguous.
    """
    text = question.strip().lower()

    # 1. Out-of-scope check (unless cooperative terms are present)
    has_coop_term = any(
        w in text for w in [
            "cooperative", "society", "societies", "member", "membership",
            "registrar", "committee", "agm", "sahakaar", "bye-law", "byelaw",
            "surcharge", "section", "shareholder", "dccb", "general body"
        ]
    )

    for pattern in OUT_OF_SCOPE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE) and not has_coop_term:
            return "OUT_OF_SCOPE"

    # 2. Check grievance
    for pattern in GRIEVANCE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "GRIEVANCE"

    # 3. Check procedure
    for pattern in PROCEDURE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "PROCEDURE"

    # 4. Check legal rights
    for pattern in LEGAL_RIGHTS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "LEGAL_RIGHTS"

    # 5. Check governance
    for pattern in GOVERNANCE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "GOVERNANCE"

    # 6. Fallback cooperative general terms
    if has_coop_term:
        return "GENERAL"

    return None


def get_llm_instance(model_name: str = "gemini-1.5-flash"):
    """Safely initialize ChatGoogleGenerativeAI instance with fast timeout."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.startswith("AQ.") or "your_" in api_key.lower():
        return None
    try:
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=api_key,
            request_timeout=3,
            max_retries=1
        )
    except Exception:
        return None


def classify_llm(question: str) -> str:
    """
    Call Gemini with supported multi-model fallback and quota protection.
    Falls back gracefully if quota is exhausted.
    """
    models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    prompt = ROUTER_PROMPT.format(question=question)

    for model_name in models:
        llm = get_llm_instance(model_name)
        if not llm:
            continue
        try:
            response = llm.invoke(prompt)
            if response and response.content:
                cat = response.content.strip().upper()
                for valid in VALID_CATEGORIES:
                    if valid in cat:
                        return valid
        except Exception as e:
            err_str = str(e).lower()
            # 429 / ResourceExhausted -> try next model
            if "429" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
                continue
            break

    # If LLM unavailable or quota exhausted, heuristic classification
    return "GENERAL"


def route_query(question: str) -> str:
    """
    Hybrid query router:
    1. In-memory cache check (0ms, 0 quota).
    2. Rule-based fast regex engine (0ms, 0 quota).
    3. Fallback to Gemini with multi-model quota resilience.
    """
    if not question or not question.strip():
        return "GENERAL"

    q_clean = question.strip()
    cache_key = q_clean.lower()
    if cache_key in _ROUTER_CACHE:
        return _ROUTER_CACHE[cache_key]

    # Step 1: Rule-based fast path
    rule_category = classify_rule_based(q_clean)
    if rule_category:
        _ROUTER_CACHE[cache_key] = rule_category
        return rule_category

    # Step 2: LLM path with quota-exhaustion protection
    try:
        llm_category = classify_llm(q_clean)
        _ROUTER_CACHE[cache_key] = llm_category
        return llm_category
    except Exception:
        _ROUTER_CACHE[cache_key] = "GENERAL"
        return "GENERAL"


if __name__ == "__main__":
    test_cases = [
        ("Who can vote in a cooperative society election?", "GOVERNANCE"),
        ("What are my legal rights as a cooperative society member?", "LEGAL_RIGHTS"),
        ("How do I register a new cooperative society?", "PROCEDURE"),
        ("The committee illegally rejected my membership application!", "GRIEVANCE"),
        ("What is a cooperative society?", "GENERAL"),
        ("What is the weather today?", "OUT_OF_SCOPE"),
    ]

    print("\nTesting Hybrid Router:")
    for q, expected in test_cases:
        routed = route_query(q)
        print(f"[{routed}] (Expected: {expected}) -> '{q}'")