"""Defines query builder abstractions and metadata-based implementations for Qdrant searches."""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any


class BaseQuery(ABC):
    """Abstract base class for all query builders."""

    @abstractmethod
    def build(self) -> Dict[str, Any]:
        """Builds and returns the query parameters or filters for Qdrant."""
        pass


class MetadataQuery(BaseQuery):
    """Builds a query filter for Qdrant based on airline metadata fields."""

    def __init__(self, airline: str, locale: str, policy_version: Optional[str] = None):
        self.airline = airline
        self.locale = locale
        self.policy_version = policy_version

    def build(self) -> Dict[str, Any]:
        """Constructs Qdrant filter structure for airline policies."""
        must_conditions = [
            {"key": "airline", "match": {"value": self.airline}},
            {"key": "locale", "match": {"value": self.locale}},
        ]
        should_conditions = []
        if self.policy_version:
            should_conditions.append(
                {"key": "policy_version", "match": {"value": self.policy_version}}
            )

        query_filter = {"must": must_conditions}
        if should_conditions:
            query_filter["should"] = should_conditions

        return query_filter
