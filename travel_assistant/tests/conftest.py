"""Test configuration and fixtures for travel_assistant tests."""

import os
import tempfile
import fitz
import pytest
from unittest.mock import Mock
from travel_assistant.rag.ingestion.indexer_service import IndexerService


@pytest.fixture
def temp_md_file():
    """Create a temporary markdown file for testing."""
    content = """# Test Document

This is a test markdown document with:
- **Bold text**
- *Italic text*
- [Links](https://example.com)

## Section 2
Some more content here.
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        temp_path = f.name

    yield temp_path, content

    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def temp_pdf_file():
    """Create a temporary PDF file for testing."""
    content = "This is a test PDF document with some text content."

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        temp_path = f.name

    # Create a simple PDF with text
    doc = fitz.open()  # Create new empty document
    page = doc.new_page()  # Add a page
    page.insert_text((50, 50), content)  # Insert text
    doc.save(temp_path)
    doc.close()

    yield temp_path, content

    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def temp_empty_pdf_file():
    """Create a temporary PDF file with no text (image-only simulation)."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        temp_path = f.name

    # Create a PDF with just a blank page (no text)
    doc = fitz.open()
    doc.new_page()  # Add empty page without text
    # Don't insert any text - simulates image-only PDF
    doc.save(temp_path)
    doc.close()

    yield temp_path

    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def temp_unsupported_file():
    """Create a temporary file with unsupported extension."""
    content = "This is a test file with unsupported format."

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def nonexistent_file_path():
    """Provide a path to a file that doesn't exist."""
    return "/nonexistent/path/to/file.md"


@pytest.fixture
def mock_fitz_document():
    """Mock fitz document for testing PDF operations."""
    mock_doc = Mock()
    mock_page = Mock()
    mock_page.get_text.return_value = "Mocked PDF content"
    mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
    mock_doc.close = Mock()
    return mock_doc


# IndexerService fixtures
@pytest.fixture
def mock_qdrant_repo():
    """Mock Qdrant repository."""
    mock_repo = Mock()
    mock_repo.ensure_collection = Mock()
    mock_repo.upsert_points = Mock()
    return mock_repo


@pytest.fixture
def mock_embeddings_provider():
    """Mock embeddings provider."""
    mock_provider = Mock()
    # Default: return valid 1536-dimensional vectors
    mock_provider.embed_texts.return_value = [
        [0.1] * 1536,
        [0.2] * 1536,
        [0.3] * 1536,
    ]
    return mock_provider


@pytest.fixture
def indexer_service(mock_qdrant_repo, mock_embeddings_provider):
    """Create IndexerService instance with mocked dependencies."""

    return IndexerService(mock_qdrant_repo, mock_embeddings_provider)


@pytest.fixture
def sample_chunks():
    """Sample chunks data for testing."""
    return [
        {
            "text": "Sample airline policy text 1",
            "airline": "Delta",
            "locale": "en-US",
            "policy_version": "2024.1",
            "doc_id": "delta_policy_001",
            "chunk_id": 1,
            "source": "/policies/Delta/policy.md",
        },
        {
            "text": "Another policy chunk with different content",
            "airline": "American Airlines",
            "locale": "en-US",
            "policy_version": "2024.2",
            "doc_id": "aa_policy_002",
            "chunk_id": 2,
            "source": "/policies/AmericanAirlines/baggage.md",
        },
        {
            "text": "Third chunk for comprehensive testing",
            "airline": "United",
            "locale": "es-ES",
            "policy_version": "2024.1",
            "doc_id": "united_policy_003",
            "chunk_id": 1,
            "source": "/policies/United/pets.pdf",
        },
    ]
