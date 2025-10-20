from typing import Annotated

# Constants for text chunking and retrieval
CHUNK_SIZE: Annotated[int, "Characters per chunk"] = 1000
CHUNK_OVERLAP: Annotated[int, "Overlap between chunks"] = 120

# Retrieval Configuration
TOP_K: Annotated[int, "Number of top similar chunks to retrieve"] = 5
SCORE_THRESHOLD: Annotated[float, "Minimum similarity score threshold"] = 0.2

# Embedding Model Configuration
VECTOR_SIZE: Annotated[int, "Size of the embedding vectors"] = (
    1536  # OpenAI's text-embedding-ada-002 vector size
)

# Ingestion Configuration
SUPPORTED_FILE_FORMATS: Annotated[set[str], "Allowed document extensions"] = {
    ".md",
    ".pdf",
}

# Context Building Configuration
CONTEXT_MAX_LENGTH: Annotated[int, "Maximum context string length"] = 3000

# LLM Configuration

# Conversational Memory Configuration
CONVERSATION_BUFFER_WINDOW_K: Annotated[int, "Conversation memory window size (last K turns)"] = 5
