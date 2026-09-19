from pathlib import Path

DATA_DIR = Path("data")

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def collect_documents():
    documents = []

    for path in DATA_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.append(path)

    return documents


if __name__ == "__main__":
    documents = collect_documents()

    print(f"Found {len(documents)} source documents.")

    for document in documents:
        print(f"- {document}")
