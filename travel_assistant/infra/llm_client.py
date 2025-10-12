"""
Pure LLM client for external API communication.
Follows Single Responsibility Principle - only handles API calls.
"""

from abc import ABC, abstractmethod
import logging
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
    """Pure OpenAI API client - no business logic, just API communication."""

    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1):
        """
        Initialize OpenAI client.

        Args:
            model_name: OpenAI model to use
            temperature: Response creativity (0.0 = deterministic,
                1.0 = creative)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.client = ChatOpenAI(
            model=model_name, temperature=temperature, openai_api_key=settings.LITELLM_API_KEY
        )

    def generate(self, prompt: str) -> str:
        """
        Generate response using OpenAI API.

        Args:
            prompt: Complete formatted prompt

        Returns:
            Generated response from OpenAI
        """
        logger.info("Sending prompt to OpenAI, length: %d", len(prompt))

        try:
            response = self.client.invoke(prompt)
            answer = response.content.strip()

            logger.info("Received response from OpenAI, length: %d", len(answer))
            return answer

        except Exception as e:
            logger.error("OpenAI API call failed: %s", str(e))
            raise RuntimeError(f"LLM generation failed: {e}") from e
