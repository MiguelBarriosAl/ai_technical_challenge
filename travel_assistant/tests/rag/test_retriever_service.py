"""
Tests for RetrieverService to verify dependency injection.
"""

from unittest.mock import Mock, patch
from travel_assistant.rag.retriever_service import RetrieverService


class TestRetrieverService:
    """Test suite for RetrieverService with dependency injection."""

    @patch("travel_assistant.rag.retriever_service.QdrantRepository")
    def test_dependency_injection(self, mock_qdrant_repo):
        """Test that RetrieverService accepts injected dependencies."""
        # Arrange
        mock_embedding_provider = Mock()
        collection_name = "test_collection"
        k = 5

        # Act
        retriever = RetrieverService(
            collection_name=collection_name, embedding_provider=mock_embedding_provider, k=k
        )

        # Assert
        assert retriever.collection_name == collection_name
        assert retriever.k == k
        assert retriever.embedding_provider == mock_embedding_provider

    @patch("travel_assistant.rag.retriever_service.QdrantRepository")
    def test_uses_settings_vector_size(self, mock_qdrant_repo):
        """Test that RetrieverService uses VECTOR_SIZE from settings."""
        # Arrange
        mock_embedding_provider = Mock()
        collection_name = "test_collection"

        # Act
        retriever = RetrieverService(
            collection_name=collection_name, embedding_provider=mock_embedding_provider
        )

        # Assert
        mock_qdrant_repo.assert_called_once_with(
            host="localhost",
            port=6333,
            collection_name=collection_name,
            vector_size=1536,
        )
        assert retriever.collection_name == collection_name

    @patch("travel_assistant.rag.retriever_service.QdrantRepository")
    def test_retrieve_calls_embeddings_and_search(self, mock_qdrant_repo):
        """Test that retrieve method properly calls embeddings and search."""
        # Arrange
        mock_embedding_provider = Mock()
        mock_embedding_provider.embed_query.return_value = [0.1, 0.2, 0.3]

        mock_qdrant_instance = Mock()
        mock_qdrant_repo.return_value = mock_qdrant_instance

        mock_result = Mock()
        mock_result.payload = {"text": "Sample policy text"}
        mock_qdrant_instance.search.return_value = [mock_result]

        mock_query = Mock()
        mock_query.build.return_value = {"filter": "test"}

        retriever = RetrieverService(
            collection_name="test_collection", embedding_provider=mock_embedding_provider
        )
        query_text = "Can I travel with pets?"

        # Act
        results = retriever.retrieve(query_text, mock_query)

        # Assert
        mock_embedding_provider.embed_query.assert_called_once_with(query_text)
        mock_query.build.assert_called_once()
        mock_qdrant_instance.search.assert_called_once_with(
            vector=[0.1, 0.2, 0.3], top_k=5, filters={"filter": "test"}
        )
        assert results == ["Sample policy text"]

    def test_default_k_value(self):
        """Test that default k value is 5."""
        mock_embedding_provider = Mock()

        with patch("travel_assistant.rag.retriever_service.QdrantRepository"):
            retriever = RetrieverService(
                collection_name="test_collection", embedding_provider=mock_embedding_provider
            )
            assert retriever.k == 5

    def test_custom_k_value(self):
        """Test that custom k value is properly set."""
        mock_embedding_provider = Mock()

        with patch("travel_assistant.rag.retriever_service.QdrantRepository"):
            custom_k = 10
            retriever = RetrieverService(
                collection_name="test_collection",
                embedding_provider=mock_embedding_provider,
                k=custom_k,
            )
            assert retriever.k == custom_k
