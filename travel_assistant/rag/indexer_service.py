import hashlib
import logging
from typing import List, Dict
from qdrant_client.models import PointStruct
from travel_assistant.core.errors import IndexingError
from travel_assistant.core.settings import settings


logger = logging.getLogger(__name__)


class IndexerService:
    """Handles the ingestion and indexing of document chunks into Qdrant."""

    def __init__(self, qdrant_repo, embeddings_provider):
        self.qdrant_repo = qdrant_repo
        self.embeddings_provider = embeddings_provider

    @staticmethod
    def _hash_text(text: str) -> str:
        """Generate deterministic hash for deduplication."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def index_chunks(self, chunks: List[Dict]) -> None:
        """
        Index a list of chunks into Qdrant.
        Each chunk must include:
        {
            'text': str,
            'airline': str,
            'locale': str,
            'policy_version': str,
            'doc_id': str,
            'chunk_id': int,
            'source': str
        }
        """
        try:
            # Ensure collection exists
            self.qdrant_repo.ensure_collection()

            # Compute embeddings
            texts = [c["text"] for c in chunks]
            vectors = self.embeddings_provider.embed_texts(texts)

            if not vectors or len(vectors[0]) != settings.VECTOR_SIZE:
                raise IndexingError("Embedding dimension mismatch or empty vector output.")

            points = []
            for chunk, vector in zip(chunks, vectors):
                # Generate a valid point ID by hashing the combination of identifiers
                id_string = f"{chunk['doc_id']}:{chunk['policy_version']}:{chunk['chunk_id']}"
                point_id = hashlib.md5(id_string.encode()).hexdigest()
                payload = {
                    "airline": chunk["airline"],
                    "locale": chunk["locale"],
                    "policy_version": chunk["policy_version"],
                    "doc_id": chunk["doc_id"],
                    "chunk_id": chunk["chunk_id"],
                    "sha256": self._hash_text(chunk["text"]),
                    "source": chunk["source"],
                }
                points.append(PointStruct(id=point_id, vector=vector, payload=payload))

            self.qdrant_repo.upsert_points(points)
            logger.info(f"Indexed {len(points)} chunks successfully.")
        except Exception as e:
            logger.error(f"Indexing failed: {e}")
            raise IndexingError(f"Failed to index chunks: {e}")
