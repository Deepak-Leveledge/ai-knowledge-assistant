from typing import List
import os
import docx2txt


from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
# prefer langchain's built-in splitter when available
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except Exception:
    # fallback package name used in some environments
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore

# Import Document type with a couple of fallbacks depending on langchain version
try:
    from langchain_core.documents import Document
except Exception:
    try:
        from langchain_core.documents import Document  # type: ignore
    except Exception:
        # last resort: create a minimal Document dataclass-like holder
        from dataclasses import dataclass

        @dataclass
        class Document:
            page_content: str
            metadata: dict


def _extract_text_with_pymupdf(path: str) -> List[str]:
    """Try extracting text using PyMuPDF (fitz). Returns list of page texts."""
    try:
        import fitz  # PyMuPDF
    except Exception as e:
        # PyMuPDF not installed or failed to import
        print("pymupdf (fitz) not available:", e)
        return []

    texts: List[str] = []
    try:
        doc = fitz.open(path)
        for p in range(len(doc)):
            page = doc.load_page(p)
            txt = page.get_text("text") or ""
            texts.append(txt)
    except Exception as e:
        print("Error extracting text with pymupdf:", e)
        return []
    return texts


def _extract_text_with_loader(path: str) -> List[str]:
    """Fallback extractor using LangChain's PyPDFLoader/Docx2txtLoader."""
    if path.lower().endswith(".pdf"):
        loader = PyPDFLoader(path)
    else:
        loader = Docx2txtLoader(path)

    documents = loader.load()
    texts: List[str] = []
    for d in documents:
        # prefer page_content if available
        txt = getattr(d, "page_content", None) or getattr(d, "content", None)
        if not txt:
            # last resort: try to extract text from object or metadata
            try:
                txt = str(d)
            except Exception:
                txt = ""
        texts.append(txt)
    return texts


def _extract_text_with_ocr(path: str) -> List[str]:
    """OCR fallback using pdf2image + pytesseract. Requires poppler and tesseract installed."""
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except Exception as e:
        print("pdf2image/pytesseract not available:", e)
        return []

    try:
        images = convert_from_path(path, dpi=300)
    except Exception as e:
        print("pdf2image.convert_from_path failed:", e)
        return []

    texts = []
    for img in images:
        try:
            texts.append(pytesseract.image_to_string(img))
        except Exception as e:
            print("pytesseract failed on an image:", e)
            texts.append("")
    return texts


def load_and_split(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Load a PDF or DOCX, extract text (with OCR fallback), and split into chunks.

    Returns a list of LangChain `Document` objects with `page_content` and metadata.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    page_texts: List[str] = []

    # Try PyMuPDF for PDFs (better text extraction). Fall back to loaders if not available.
    extractor_used = None
    if file_path.lower().endswith(".pdf"):
        try:
            page_texts = _extract_text_with_pymupdf(file_path)
            if any(p and p.strip() for p in page_texts):
                extractor_used = "pymupdf"
        except Exception:
            page_texts = []

        if not extractor_used:
            # PyMuPDF failed or returned empty pages -> try LangChain loader
            page_texts = _extract_text_with_loader(file_path)
            if any(p and p.strip() for p in page_texts):
                extractor_used = "loader"
    elif file_path.lower().endswith(".docx"):
        page_texts = _extract_text_with_loader(file_path)
        if any(p and p.strip() for p in page_texts):
            extractor_used = "loader"
    else:
        raise ValueError("Unsupported file format, please upload pdf or docx")

    # If pages are empty (likely scanned PDF), try OCR fallback
    if not extractor_used and all((not (p and p.strip())) for p in page_texts):
        try:
            page_texts = _extract_text_with_ocr(file_path)
            if any(p and p.strip() for p in page_texts):
                extractor_used = "ocr"
        except Exception as e:
            # OCR not available or failed; keep current texts (may be empty)
            print("OCR fallback failed or not available:", e)

    # Debug info: report which extractor produced results
    non_empty = sum(1 for p in page_texts if p and p.strip())
    total_pages = len(page_texts)
    print(f"Extractor used: {extractor_used}")
    print(f"Pages: {total_pages}, Non-empty pages: {non_empty}")
    if non_empty:
        # show small sample of first non-empty page
        for p in page_texts:
            if p and p.strip():
                print("Sample text (first 300 chars):", p.strip()[:300])
                break

    # Build Documents (one per page) with metadata
    page_docs: List[Document] = []
    for i, text in enumerate(page_texts):
        meta = {"source": file_path, "page": i + 1}
        page_docs.append(Document(page_content=text or "", metadata=meta))

    # Split into chunks suitable for embeddings/vector store
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    split_docs = text_splitter.split_documents(page_docs)
    print(f"Loaded and split {file_path} into {len(split_docs)} chunks.")
    return split_docs

