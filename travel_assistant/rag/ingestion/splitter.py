from typing import List, Dict
from travel_assistant.core.constants import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(
    text: str,
    airline: str,
    locale: str,
    policy_version: str,
    doc_id: str,
    source: str,
) -> List[Dict]:
    """
    Split text into overlapping chunks.

    Each returned dict includes:
    {
        "text": str,
        "airline": str,
        "locale": str,
        "policy_version": str,
        "doc_id": str,
        "chunk_id": int,
        "source": str
    }
    """
    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    chunk_id = 1

    # Divide the text in windows of CHUNK_SIZE with overlap
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()

        chunks.append(
            {
                "text": chunk_text,
                "airline": airline,
                "locale": locale,
                "policy_version": policy_version,
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "source": source,
            }
        )

        # Move start considering overlap
        start += CHUNK_SIZE - CHUNK_OVERLAP
        chunk_id += 1

    return chunks
