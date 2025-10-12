from typing import Dict, Optional


def build_filter_query(airline: str, locale: str, policy_version: Optional[str] = None) -> Dict:
    """Builds the structured query filter for Qdrant based on metadata fields."""
    must_conditions = [
        {"key": "airline", "match": {"value": airline}},
        {"key": "locale", "match": {"value": locale}},
    ]
    should_conditions = []
    if policy_version:
        should_conditions.append({"key": "policy_version", "match": {"value": policy_version}})

    query_filter = {"must": must_conditions}
    if should_conditions:
        query_filter["should"] = should_conditions

    return query_filter
