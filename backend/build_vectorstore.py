from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_DIR = Path("data")
VECTORSTORE_DIR = Path("vectorstore")


def load_documents():
    documents = []

    for path in DATA_DIR.rglob("*"):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            loader = PyPDFLoader(str(path))
            documents.extend(loader.load())

        elif suffix in {".txt", ".md"}:
            loader = TextLoader(
                str(path),
                encoding="utf-8"
            )
            documents.extend(loader.load())

    return documents


def main():
    documents = load_documents()

    print(f"Loaded {len(documents)} document pages.")

    if not documents:
        print("No source documents found.")
        print("Add PDF/TXT/MD files under data/ and run this script again.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")

    VECTORSTORE_DIR.mkdir(exist_ok=True)

    print("Vector database preparation is ready.")
    print(f"Vectorstore directory: {VECTORSTORE_DIR}")


if __name__ == "__main__":
    main()
