from langchain_openai import OpenAIEmbeddings
from travel_assistant.core.settings import settings
from travel_assistant.core.errors import IndexingError


class EmbeddingFactory:
    """
    Clean factory for creating OpenAI embedding models.
    Designed for production use with proper error handling.
    """

    @staticmethod
    def create(model_name: str) -> OpenAIEmbeddings:
        """
        Create OpenAI embedding model with validation.

        Args:
            model_name: OpenAI model name (e.g., 'text-embedding-3-small')

        Returns:
            Configured OpenAIEmbeddings instance

        Raises:
            IndexingError: If model_name is invalid or API key missing
        """
        if not model_name or not isinstance(model_name, str):
            raise IndexingError("Model name must be a non-empty string")

        if not settings.LITELLM_API_KEY:
            raise IndexingError("LITELLM_API_KEY not configured")

        # Validate OpenAI model name format
        valid_prefixes = ("text-embedding", "gpt")
        if not any(model_name.startswith(prefix) for prefix in valid_prefixes):
            raise IndexingError(
                f"Unsupported model: {model_name}. " f"Must start with {valid_prefixes}"
            )

        return OpenAIEmbeddings(model=model_name, openai_api_key=settings.LITELLM_API_KEY)

    @staticmethod
    def get_dimension(embedding_model) -> int:
        """
        Get embedding dimension by testing with sample text.

        Args:
            embedding_model: LangChain embeddings instance

        Returns:
            Dimension of the embedding vectors

        Raises:
            IndexingError: If unable to determine dimension
        """
        try:
            sample = ["test sentence"]
            vec = embedding_model.embed_documents(sample)
            if not vec or not vec[0]:
                raise IndexingError("Empty embedding returned")
            return len(vec[0])
        except IndexingError:
            raise
        except Exception as e:
            raise IndexingError(f"Failed to get embedding dimension: {e}") from e


class EmbeddingsProvider:
    """Unified interface over the selected embedding backend."""

    def __init__(self, model_name: str):
        self.model = EmbeddingFactory.create(model_name)
        self.dimension = EmbeddingFactory.get_dimension(self.model)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        try:
            return self.model.embed_documents(texts)
        except Exception as e:
            raise IndexingError(f"Embedding text batch failed: {e}")

    def embed_query(self, query: str) -> list[float]:
        try:
            return self.model.embed_query(query)
        except Exception as e:
            raise IndexingError(f"Embedding query failed: {e}")
