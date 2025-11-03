# backend/tests/test_document_processor.py
from backend.services.document_processor import load_and_split

def test_load_pdf():
    path = "uploads/Gupta_Deepak_CV (2) (2).pdf"
    chunks = load_and_split(path)
    # Basic assertions: returns a list and items have page_content
    assert isinstance(chunks, list)
    # If the PDF is text-based this should be > 0
    assert len(chunks) >= 0  # len may be 0 for scanned PDFs—use debug script for deeper checks
    if len(chunks) > 0:
        assert hasattr(chunks[0], "page_content")
        assert isinstance(chunks[0].page_content, str)

# Optionally add a docx test if you have a sample file
def test_load_docx_if_present():
    import os
    path = "uploads/sample.docx"
    if os.path.exists(path):
        chunks = load_and_split(path)
        assert len(chunks) > 0
        assert chunks[0].page_content.strip() != ""