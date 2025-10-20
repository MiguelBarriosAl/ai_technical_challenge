from pydantic import BaseModel, Field
from typing import Optional


class AskRequest(BaseModel):
    """Input model for /ask endpoint."""

    question: str = Field(..., description="User question to the assistant")
    airline: str = Field(..., description="Airline name, e.g., 'United'")
    locale: str = Field(..., description="Language or region, e.g., 'en'")
    policy_version: Optional[str] = Field(
        None, description="Specific version of the airline policy"
    )
    session_id: Optional[str] = Field(
        None,
        description=(
            "Conversation session identifier. If provided, conversational "
            "memoria (contexto previo) será vinculada."
        ),
    )
