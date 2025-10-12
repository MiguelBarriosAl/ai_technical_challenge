"""
Pure LLM client for external API communication.
Follows Single Responsibility Principle - only handles API calls.
"""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from travel_assistant.core.settings import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract interface for LLM providers following SOLID principles."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from a complete prompt."""
        pass


class OpenAILLMClient(LLMProvider):
    """OpenAI GPT implementation of LLM provider."""

    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1):
        """
        Initialize OpenAI LLM provider.

        Args:
            model_name: OpenAI model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')
            temperature: Response creativity (0.0 = deterministic,
                1.0 = creative)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.client = ChatOpenAI(
            model=model_name, temperature=temperature, openai_api_key=settings.LITELLM_API_KEY
        )

    def generate_response(self, question: str, context: str) -> str:
        """
        Generate response using OpenAI GPT with RAG context.

        Args:
            question: User's question
            context: Retrieved relevant context from RAG

        Returns:
            Generated response from the LLM
        """
        logger.info("Generating LLM response for question length: %d", len(question))

        prompt = self._build_prompt(question, context)

        try:
            response = self.client.invoke(prompt)
            answer = response.content.strip()

            logger.info("LLM response generated successfully, length: %d", len(answer))
            return answer

        except Exception as e:
            logger.error("Failed to generate LLM response: %s", str(e))
            return (
                "I apologize, but I'm unable to process your question "
                "right now. Please try again later."
            )

    def _build_prompt(self, question: str, context: str) -> str:
        """
        Build a professional prompt for airline policy questions.

        Args:
            question: User's question
            context: Retrieved relevant context

        Returns:
            Formatted prompt for the LLM
        """
        system_instructions = """
You are a professional airline travel assistant. Answer questions about
airline policies using only the provided context. Be helpful, accurate,
and concise.

Guidelines:
- Only use information from the provided context
- If the context doesn't contain enough information, say so politely
- Focus on practical, actionable advice
- Be professional and customer-service oriented
- Use clear, easy-to-understand language
"""

        return f"""{system_instructions}

Context:
{context}

Question: {question}

Answer:"""


class LLMService:
    """
    High-level LLM service that orchestrates question answering.
    Follows Single Responsibility Principle.
    """

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize LLM service with dependency injection.

        Args:
            llm_provider: LLM provider implementation
        """
        self.llm_provider = llm_provider

    def answer_question(self, question: str, context: str) -> Dict[str, Any]:
        """
        Generate a comprehensive answer to a question using context.

        Args:
            question: User's question
            context: Relevant context from RAG retrieval

        Returns:
            Dictionary with answer and metadata
        """
        logger.info("Processing question through LLM service")

        answer = self.llm_provider.generate_response(question, context)

        return {
            "answer": answer,
            "model_used": getattr(self.llm_provider, "model_name", "unknown"),
            "context_length": len(context),
        }
