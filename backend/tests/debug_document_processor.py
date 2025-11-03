# backend/tests/debug_document_processor.py
from backend.services.document_processor import load_and_split
import sys


def run(path):
    print("Testing file:", path)
    chunks = load_and_split(path)
    print("Total chunks returned:", len(chunks))
    if len(chunks) > 0:
        print("First chunk metadata:", chunks[0].metadata)
        sample = chunks[0].page_content or ""
        print("First chunk text (first 500 chars):")
        print(sample[:500])
    else:
        print("No chunks produced. Possible causes: loader failed to extract text (scanned PDF or unsupported file).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backend/tests/debug_document_processor.py <path-to-file>")
        sys.exit(1)
    p = sys.argv[1]
    run(p)
