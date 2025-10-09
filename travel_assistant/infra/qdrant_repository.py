from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class QdrantRepository:
    """Infra layer: manages Qdrant collections and CRUD operations."""

    def __init__(self, host: str, port: int, collection_name: str, vector_size: int):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def ensure_collection(self) -> None:
        """Create collection if it doesn't exist."""
        if not self.client.collection_exists(self.collection_name):
            logger.info(f"Creating collection {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_points(self, points: List[PointStruct]) -> None:
        """Insert or update points (chunks) in Qdrant."""
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(
        self,
        vector: List[float],
        top_k: int = 5,
        filters: Optional[Filter] = None,
    ):
        """Search similar vectors."""
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=filters,
            limit=top_k,
        )
