import logging
from pathlib import Path

from travel_assistant.core.constants import SUPPORTED_FILE_FORMATS
from travel_assistant.rag.doc_loader import load_document
from travel_assistant.rag.splitter import split_text
from travel_assistant.rag.indexer_service import IndexerService

logger = logging.getLogger(__name__)


def run_ingestion(
    base_path: str, airline: str, locale: str, policy_version: str, indexer: IndexerService
) -> None:
    """
    Load, split, and index all policy documents for a given airline.

    Args:
        base_path: Root directory containing airline folders.
        airline: Airline name (e.g., 'Delta').
        locale: Language/region code (e.g., 'en-US').
        policy_version: Policy version identifier.
        indexer: Instance of IndexerService handling the indexing.
    """
    airline_path = Path(base_path) / airline
    if not airline_path.exists():
        logger.error(f"Airline folder not found: {airline_path}")
        return

    all_chunks = []
    for f in airline_path.glob("*"):
        ext = f.suffix.lower()
        if ext not in SUPPORTED_FILE_FORMATS:
            logger.warning(f"Skipping unsupported file format: {f.name}")
            continue

        try:
            text = load_document(str(f))
            chunks = split_text(
                text=text,
                airline=airline,
                locale=locale,
                policy_version=policy_version,
                doc_id=f.stem,
                source=str(f),
            )
            if chunks:
                all_chunks.extend(chunks)
                logger.info(f"{airline}: {f.name} → {len(chunks)} chunks")
            else:
                logger.warning(f"{airline}: {f.name} → no valid text extracted")
        except Exception as e:
            logger.error(f"Failed to process {f}: {e}")

    if all_chunks:
        indexer.index_chunks(all_chunks)
        logger.info(f"Indexed total of {len(all_chunks)} chunks for {airline}")
    else:
        logger.warning(f"No chunks indexed for {airline}")
