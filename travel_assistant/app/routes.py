"""
FastAPI routes for Travel Assistant API.
Simple and direct route definitions.
"""

import logging
from fastapi import APIRouter, HTTPException
from travel_assistant.rag.queries import MetadataQuery
from travel_assistant.rag.context_builder import ContextBuilder
from travel_assistant.rag.retriever_service import RetrieverService
from travel_assistant.rag.generation_service import RAGGenerationService
from travel_assistant.app.models.ask_models import AskRequest

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Initialize services (simple approach)
retriever = RetrieverService(collection_name="airline_policies", k=5)
context_builder = ContextBuilder(max_length=3000)
generation_service = RAGGenerationService()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/ask")
async def ask(req: AskRequest):
    """
    Ask a question about airline policies using RAG.

    Args:
        req: Request containing question, airline, locale, and optional policy_version

    Returns:
        Response with question, context, and generated answer
    """
    try:
        logger.info("Processing question for airline=%s, locale=%s", req.airline, req.locale)

        query = MetadataQuery(
            airline=req.airline, locale=req.locale, policy_version=req.policy_version
        )

        # Step 1: Retrieve fragments from Qdrant
        fragments = retriever.retrieve(req.question, query)
        logger.info("Retrieved %d fragments", len(fragments))

        # Step 2: Build context
        context = context_builder.build(fragments)
        logger.info("Built context with length: %d", len(context))

        # Step 3: Generate answer using RAG
        answer = generation_service.generate_answer(req.question, context)
        logger.info("Generated answer with length: %d", len(answer))

        return {"question": req.question, "context": context, "answer": answer}

    except Exception as e:
        logger.exception("Error processing question: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
