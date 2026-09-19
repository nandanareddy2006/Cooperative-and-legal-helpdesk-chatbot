from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

DATA_DIR = Path("data")
VECTORSTORE_DIR = Path("vectorstore")

COLLECTION_NAME = "sahakaar_saathi_legal_sources"


def load_documents():
    documents = []

    for path in DATA_DIR.rglob("*.pdf"):
        loader = PyPDFLoader(str(path))
        docs = loader.load()

        for doc in docs:
            doc.metadata.update(
                {
                    "source_file": path.name,
                    "jurisdiction": "Telangana",
                    "document_type": "Act",
                    "document_title": "Telangana Cooperative Societies Act, 1964",
                }
            )

        documents.extend(docs)

    return documents


def main():
    print("Loading legal documents...")

    documents = load_documents()
    print(f"Loaded {len(documents)} pages.")

    if not documents:
        print("No PDF documents found under data/.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Loading local embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTORSTORE_DIR.mkdir(exist_ok=True)

    print("Creating Chroma vector store...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
        collection_name=COLLECTION_NAME,
    )

    print("Vector store created successfully.")
    print(f"Location: {VECTORSTORE_DIR}")


if __name__ == "__main__":
    main()