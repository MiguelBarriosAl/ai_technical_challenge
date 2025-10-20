import logging
from fastapi import APIRouter, HTTPException
from travel_assistant.rag.queries import MetadataQuery
from travel_assistant.rag.pipeline.context_builder import ContextBuilder
from travel_assistant.rag.pipeline.retriever_service import RetrieverService
from travel_assistant.rag.pipeline.generation_service import (
    RAGGenerationService,
)
from travel_assistant.infra.embeddings import EmbeddingsProvider
from travel_assistant.core.settings import settings
from travel_assistant.app.models.ask_models import AskRequest
from langchain.memory import ConversationBufferWindowMemory

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Initialize services with dependency injection
embedding_provider = EmbeddingsProvider(model_name=settings.EMBEDDING_MODEL)
retriever = RetrieverService(
    collection_name="airline_policies",
    embedding_provider=embedding_provider,
    k=5,
)
context_builder = ContextBuilder(max_length=3000)
generation_service = RAGGenerationService()

# Una instancia compartida para todas las sesiones
conversation_memory = ConversationBufferWindowMemory(k=5)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/ask")
async def ask(req: AskRequest):
    """
    Ask a question about airline policies using RAG.

    Args:
        req: Request containing question, airline, locale, and optional
            policy_version

    Returns:
        Response with question, context, and generated answer
    """
    try:
        # Load history from memory (if session_id provided)
        history = conversation_memory.chat_memory.messages
        history_str = "\n".join([f"{m.type}: {m.content}" for m in history])
        logger.debug("Loaded history for session %s", req.session_id)

        # Build query
        query = MetadataQuery(
            airline=req.airline,
            locale=req.locale,
            policy_version=req.policy_version,
        )

        # Retrieve fragments
        fragments = retriever.retrieve(req.question, query)
        logger.info("Retrieved %d fragments", len(fragments))

        # Prepend history to context (if exists)
        if history_str:
            fragments = [history_str] + fragments
            logger.info("Prepended history to fragments for session %s", req.session_id)

        # Build context
        context = context_builder.build(fragments)
        logger.info("Built context with length: %d", len(context))

        # Generate answer
        answer = generation_service.generate_answer(req.question, context)
        logger.info("Generated answer with length: %d", len(answer))

        # Save to memory (if session_id exists)
        conversation_memory.save_context(inputs={"input": req.question}, outputs={"output": answer})
        logger.info("Saved turn to memory for session %s", req.session_id)

        return {
            "question": req.question,
            "context": context,
            "answer": answer,
            "session_id": req.session_id,
        }

    except Exception as e:
        logger.exception("Error processing question: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
