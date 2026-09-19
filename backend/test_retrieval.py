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

query = "Who can vote in a cooperative society general election?"

results = vectorstore.similarity_search(query, k=3)

print("\nQUERY:")
print(query)

print("\nRETRIEVED SOURCES:\n")

for i, doc in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print("Page:", doc.metadata.get("page"))
    print("Source:", doc.metadata.get("source_file"))
    print("Document:", doc.metadata.get("document_title"))
    print()
    print(doc.page_content[:1000])
    print()