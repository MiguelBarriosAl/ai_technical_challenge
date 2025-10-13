import fitz
import os
from travel_assistant.rag.pipeline.errors import ExtractionError


def extract_text_from_md(file_path: str) -> str:
    """Extract text from a Markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise ExtractionError(f"Failed to extract text from Markdown file: {e}") from e


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file. Detects image-only pages."""
    doc = None
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            page_text = page.get_text("text").strip()
            text += page_text + "\n"

        # If the document is not a digital PDF (i.e., contains only images)
        if not text.strip():
            raise ExtractionError(
                f"PDF '{file_path}' appears to contain only images. " "OCR required."
            )

        return text
    except ExtractionError:
        raise
    except Exception as e:
        raise ExtractionError(f"Failed to extract text from PDF file: {e}") from e
    finally:
        if doc is not None:
            doc.close()


def load_document(file_path: str) -> str:
    """Load a document and extract its text based on file type."""
    if not os.path.isfile(file_path):
        raise ExtractionError(f"File does not exist: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".md":
        return extract_text_from_md(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        raise ExtractionError(f"Unsupported file type: {ext}")
