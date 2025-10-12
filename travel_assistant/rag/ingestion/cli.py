from urllib.parse import urlparse
from travel_assistant.core.settings import settings
from travel_assistant.infra.qdrant_repository import QdrantRepository
from travel_assistant.infra.embeddings import EmbeddingsProvider
from travel_assistant.rag.indexer_service import IndexerService
from travel_assistant.rag.ingestion.ingest_service import run_ingestion


def main():
    parsed_url = urlparse(settings.QDRANT_URL)
    host = parsed_url.hostname
    port = parsed_url.port

    qdrant_repo = QdrantRepository(
        host=host,
        port=port,
        collection_name="airline_policies",
        vector_size=settings.VECTOR_SIZE,
    )

    embeddings_provider = EmbeddingsProvider(model_name=settings.EMBEDDING_MODEL)
    indexer = IndexerService(qdrant_repo, embeddings_provider)

    for airline in ["Delta", "AmericanAirlines", "United"]:
        run_ingestion(
            base_path="policies",
            airline=airline,
            locale="en-US",
            policy_version="2025-10-01",
            indexer=indexer,
        )
