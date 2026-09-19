from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

VECTORSTORE_DIR = "vectorstore"
COLLECTION_NAME = "sahakaar_saathi_legal_sources"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=VECTORSTORE_DIR,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
)


def retrieve_documents(
    query: str,
    k: int = 5,
    jurisdiction: str = "Telangana",
):
    results = vectorstore.similarity_search(query, k=k)

    unique_results = []
    seen = set()

    for doc in results:
        doc_jurisdiction = doc.metadata.get("jurisdiction", "")

        if jurisdiction and doc_jurisdiction.lower() != jurisdiction.lower():
            continue

        key = (
            doc.metadata.get("source_file"),
            doc.metadata.get("page"),
            doc.page_content[:200],
        )

        if key not in seen:
            seen.add(key)
            unique_results.append(doc)

    return unique_results