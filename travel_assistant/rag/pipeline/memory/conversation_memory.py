"""Base abstractions for conversational memory.

English-only comments for consistency with existing codebase.
Runtime behavior will produce Spanish responses as required.

Phase 1 Scope:
- Define minimal data structures to represent conversation turns.
- Define an interface (protocol-like) for memory implementations.
- Keep it simple to allow easy extension (e.g., in-memory, Redis later).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Protocol


@dataclass
class ConversationTurn:
    """Represents a single user/assistant exchange.

    Attributes:
        role: "user" or "assistant"
        content: Raw text of the message.
    """

    role: str
    content: str


class ConversationMemory(Protocol):
    """Minimal interface for conversation memory backends.

    Responsibilities:
    - Store turns associated with a session identifier.
    - Retrieve ordered history for a given session.
    - (Later) Support trimming or summarization.
    """

    def append(self, session_id: str, turn: ConversationTurn) -> None:  # pragma: no cover
        """Add a turn to a session history (create if missing)."""
        raise NotImplementedError

    def get(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ConversationTurn]:  # pragma: no cover
        """Return history oldest→newest; optionally limit to last N."""
        raise NotImplementedError

    def clear(self, session_id: str) -> None:  # pragma: no cover
        """Remove a session history entirely."""
        raise NotImplementedError
