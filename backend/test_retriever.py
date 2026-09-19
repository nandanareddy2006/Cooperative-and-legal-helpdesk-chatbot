from rag_retriever import retrieve_documents


query = "Who can vote in a cooperative society general election?"

results = retrieve_documents(query, k=5)

print("\nQUERY:")
print(query)

print("\nUNIQUE RETRIEVED SOURCES:\n")

for i, doc in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print("Page:", doc.metadata.get("page"))
    print("Source:", doc.metadata.get("source_file"))
    print("Document:", doc.metadata.get("document_title"))
    print("Text:")
    print(doc.page_content[:800])
    print()