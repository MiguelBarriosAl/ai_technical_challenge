"""Test configuration and fixtures for travel_assistant tests."""

import os
import tempfile
import fitz
import pytest
from unittest.mock import Mock


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
