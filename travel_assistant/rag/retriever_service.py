"""
Handles semantic retrieval from Qdrant using embedding similarity and flexible query filters.
"""

import logging
from typing import List
from urllib.parse import urlparse

from travel_assistant.infra.qdrant_repository import QdrantRepository
from travel_assistant.rag.queries import BaseQuery
from travel_assistant.infra.embedding_interface import EmbeddingProvider
from travel_assistant.core.settings import settings

logger = logging.getLogger(__name__)


class RetrieverService:
    """Service responsible for retrieving relevant documents from Qdrant."""

    def __init__(self, collection_name: str, embedding_provider: EmbeddingProvider, k: int = 5):
        self.collection_name = collection_name
        self.k = k
        self.embedding_provider = embedding_provider

        # Parse Qdrant connection settings
        parsed_url = urlparse(settings.QDRANT_URL)
        host = parsed_url.hostname
        port = parsed_url.port

        self.qdrant_repo = QdrantRepository(
            host=host,
            port=port,
            collection_name=collection_name,
            vector_size=settings.VECTOR_SIZE,
        )

    def retrieve(self, query_text: str, query: BaseQuery) -> List[str]:
        """
        Retrieves the most relevant text chunks from Qdrant given a query
        and a filter.

        Args:
            query_text: User input or question to embed.
            query: Query object implementing BaseQuery that defines the
                filtering logic.

        Returns:
            List of retrieved text chunks (strings).
        """
        logger.info("Starting retrieval process for query: %s", query_text)

        embedding = self.embedding_provider.embed_query(query_text)
        logger.debug("Embedding generated for query text.")

        filter_query = query.build()
        logger.debug("Filter query built: %s", filter_query)

        # Retrieve results from Qdrant
        results = self.qdrant_repo.search(vector=embedding, top_k=self.k, filters=filter_query)

        retrieved_texts = [r.payload.get("text", "") for r in results]
        logger.info("Retrieved %d relevant documents.", len(retrieved_texts))

        return retrieved_texts
