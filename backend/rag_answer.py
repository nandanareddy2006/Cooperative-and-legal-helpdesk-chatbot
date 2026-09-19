import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.rag_retriever import retrieve_documents

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)


def answer_query(query: str, jurisdiction: str = "Telangana"):
    jurisdiction = jurisdiction.strip()

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

    prompt = f"""
You are Sahakaar Saathi, a cooperative governance and legal helpdesk.

Answer the user's question using ONLY the legal source material provided below.

Rules:
1. Do not invent legal provisions.
2. If the sources do not contain enough information, say so clearly.
3. Mention the relevant page number(s).
4. Do not present the answer as a substitute for professional legal advice.
5. Keep the answer clear and concise.
SELECTED JURISDICTION:
{jurisdiction}

Use legal sources relevant to this jurisdiction. If the provided sources do not contain sufficient jurisdiction-specific information, say so clearly.
LEGAL SOURCES:
{context}

USER QUESTION:
{query}
"""

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":
    query = "Who can vote in a cooperative society general election?"

    answer = answer_query(query)

    print("\nANSWER:\n")
    print(answer)