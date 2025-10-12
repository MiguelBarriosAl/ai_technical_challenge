from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """Abstract interface for embedding providers."""

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query text."""
