from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

ROUTER_PROMPT = """
You are the query router for Sahakaar Saathi, a cooperative governance
and legal helpdesk.

Classify the user's question into exactly ONE category.

Categories:

GOVERNANCE:
Questions about cooperative society elections, voting, committees,
members, meetings, governance, office bearers, or administration.

LEGAL_RIGHTS:
Questions about legal rights, duties, protections, eligibility,
entitlements, or legal provisions concerning cooperative societies.

PROCEDURE:
Questions asking how to perform a cooperative society procedure,
including elections, registration, meetings, filing, approvals,
or required documents.

GRIEVANCE:
Questions describing a dispute, complaint, violation, unfair action,
misconduct, or asking how to file a grievance/complaint.

GENERAL:
General questions related to cooperative societies that do not
clearly belong to the categories above.

OUT_OF_SCOPE:
Questions unrelated to cooperative societies, cooperative governance,
or the legal/procedural helpdesk.

Return ONLY the category name.

USER QUESTION:
{question}
"""


def route_query(question: str) -> str:
    prompt = ROUTER_PROMPT.format(question=question)

    response = llm.invoke(prompt)

    category = response.content.strip().upper()

    valid_categories = {
        "GOVERNANCE",
        "LEGAL_RIGHTS",
        "PROCEDURE",
        "GRIEVANCE",
        "GENERAL",
        "OUT_OF_SCOPE",
    }

    if category not in valid_categories:
        return "GENERAL"

    return category


if __name__ == "__main__":
    test_questions = [
        "Who can vote in a cooperative society election?",
        "What are my legal rights as a cooperative society member?",
        "How do I conduct a cooperative society election?",
        "I have a complaint against my society committee.",
        "What is a cooperative society?",
        "What is the weather today?",
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        print(f"Category: {route_query(question)}")