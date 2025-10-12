"""
Simple prompts for airline policy assistance.
Simplified for technical interview demonstration.
"""

SYSTEM_PROMPT = """You are a helpful airline travel assistant. Answer questions
about airline policies using only the provided context. Be clear, accurate,
and helpful."""


def build_rag_prompt(question: str, context: str) -> str:
    """
    Build simple prompt for airline policy questions.

    Args:
        question: User's question
        context: Retrieved context from RAG

    Returns:
        Formatted prompt
    """
    return f"""{SYSTEM_PROMPT}

Context:
{context}

Question: {question}

Answer:"""
