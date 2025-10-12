from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


def split_text_into_chunks(
    text: str, chunk_size: int = 1000, chunk_overlap: int = 120
) -> List[str]:
    """
    Splits a long text into overlapping chunks for embedding and retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    )

    chunks = splitter.split_text(text)
    return chunks
