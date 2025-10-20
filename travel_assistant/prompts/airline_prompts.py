"""
Simple prompts for airline policy assistance.
Simplified for technical interview demonstration.
"""

SYSTEM_PROMPT = """You are a helpful airline travel assistant. Answer questions
about airline policies using only the provided context. Be clear, accurate,
and helpful. If conversation history is provided, consider it as context for
understanding follow-up questions."""


def build_rag_prompt(question: str, context: str, history: str = "") -> str:
    """
    Build prompt for airline policy questions with optional history.

    Args:
        question: User's current question.
        context: Retrieved context from RAG (fragments from Qdrant).
        history: Optional conversation history from memory buffer.

    Returns:
        Complete prompt with system instruction, history, context,
        and question.
    """
    history_section = ""
    if history:
        history_section = f"""Previous conversation:
{history}

"""

    return f"""{SYSTEM_PROMPT}

{history_section}Context:
{context}

Question: {question}

Answer:"""
