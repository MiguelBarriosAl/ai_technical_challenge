import logging
from travel_assistant.infra.llm_client import LLMProvider, OpenAILLMClient
from travel_assistant.prompts.airline_prompts import build_rag_prompt

logger = logging.getLogger(__name__)


class RAGGenerationService:
    """
    Handles the Generation part of RAG (Retrieval-Augmented Generation).
    Orchestrates prompt building and LLM interaction.
    """

    def __init__(self, llm_client: LLMProvider = None):
        """
        Initialize RAG generation service.

        Args:
            llm_client: LLM client for generating responses
        """
        self.llm_client = llm_client or OpenAILLMClient()  # Default to OpenAI client

    def generate_answer(self, question: str, context: str, history: str = "") -> str:
        """
        Generate an answer using RAG approach with optional history.

        Args:
            question: User's question.
            context: Retrieved context from RAG retrieval.
            history: Optional conversation history from memory buffer.

        Returns:
            Generated answer from LLM.
        """
        logger.info("Generating RAG answer for question length: %d", len(question))

        # Build prompt using our prompt template with history
        prompt = build_rag_prompt(question, context, history=history)

        # Generate response using LLM client
        try:
            answer = self.llm_client.generate(prompt)
            logger.info("RAG answer generated successfully, length: %d", len(answer))
            return answer

        except Exception as e:
            logger.error("RAG generation failed: %s", str(e))
            return (
                "I apologize, but I'm unable to process your question "
                "right now. Please try again later."
            )
