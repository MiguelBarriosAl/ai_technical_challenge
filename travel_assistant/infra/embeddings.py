from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from travel_assistant.core.settings import settings
from travel_assistant.rag.exceptions import ExtractionError


class EmbeddingFactory:
    """
    Wrapper for creating and validating embedding models.
    Supports OpenAI and HuggingFace/BGE models.
    """

    @staticmethod
    def create(model_name: str):
        if model_name.startswith("text-embedding") or model_name.startswith("gpt"):
            return OpenAIEmbeddings(
                model=model_name,
                openai_api_key=settings.LITELLM_API_KEY,
            )
        elif "bge" in model_name.lower():
            return HuggingFaceEmbeddings(model_name=model_name)
        else:
            raise ExtractionError(f"Unsupported embedding model: {model_name}")

    @staticmethod
    def get_dimension(embedding_model) -> int:
        """
        Validate embedding dimensionality to ensure consistency with vector store.
        """
        try:
            sample = ["test sentence"]
            vec = embedding_model.embed_documents(sample)
            return len(vec[0])
        except Exception as e:
            raise ExtractionError(f"Failed to get embedding dimension: {e}")
