import logging
from fastapi import FastAPI, HTTPException
from travel_assistant.rag.context_builder import ContextBuilder
from travel_assistant.rag.queries import MetadataQuery
from travel_assistant.rag.retriever_service import RetrieverService
from travel_assistant.rag.generation_service import RAGGenerationService
from travel_assistant.app.error_handlers import register_error_handlers
from travel_assistant.app.models.ask_models import AskRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="Travel Assistant AI")

register_error_handlers(app)
retriever = RetrieverService(collection_name="airline_policies", k=5)
context_builder = ContextBuilder(max_length=3000)
generation_service = RAGGenerationService()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/ask")
async def ask(req: AskRequest):
    try:
        query = MetadataQuery(
            airline=req.airline, locale=req.locale, policy_version=req.policy_version
        )

        # Step 1: Retrieve fragments from Qdrant
        fragments = retriever.retrieve(req.question, query)

        # Step 2: Build context
        context = context_builder.build(fragments)

        # Step 3: Generate answer using RAG
        answer = generation_service.generate_answer(req.question, context)

        return {"question": req.question, "context": context, "answer": answer}

    except Exception as e:
        logger.exception("Error processing question")
        raise HTTPException(status_code=500, detail=str(e))
