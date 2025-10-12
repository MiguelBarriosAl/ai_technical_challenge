import logging
from typing import List

logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    Builds a clean and compact context string from retrieved text fragments.
    """

    def __init__(self, max_length: int = 3000):
        """
        :param max_length: Maximum number of characters to include in the context.
        """
        self.max_length = max_length

    def build(self, fragments: List[str]) -> str:
        """
        Combines and trims text fragments into a single context block.

        :param fragments: List of relevant text snippets retrieved from Qdrant.
        :return: A clean context string ready for LLM input.
        """
        if not fragments:
            logger.warning("No fragments provided to ContextBuilder.")
            return ""

        # Remove duplicates and empty strings
        unique_fragments = list({frag.strip() for frag in fragments if frag.strip()})
        context = "\n\n".join(unique_fragments)

        # Truncate if too long
        if len(context) > self.max_length:
            logger.info(f"Context truncated to {self.max_length} characters.")
            context = context[: self.max_length]

        logger.debug(f"Context built with {len(unique_fragments)} fragments.")
        return f"Context:\n{context}"
