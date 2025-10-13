"""Unit tests for splitter module."""

import pytest
from unittest.mock import patch

from travel_assistant.rag.ingestion.splitter import split_text


class TestSplitter:
    """Test class for text splitting functionality."""

    def test_split_text_normal_operation(self):
        """Test normal text splitting with chunks and overlap."""
        # Use constants to make the test predictable
        with patch("travel_assistant.rag.ingestion.splitter.CHUNK_SIZE", 50):
            with patch("travel_assistant.rag.ingestion.splitter.CHUNK_OVERLAP", 10):
                text = "This is a sample text that should be split into multiple chunks for testing purposes."

                result = split_text(
                    text=text,
                    airline="Delta",
                    locale="en-US",
                    policy_version="2024.1",
                    doc_id="test_doc_001",
                    source="/test/policy.md",
                )

                # Should create multiple chunks
                assert len(result) > 1

                # Verify first chunk structure
                first_chunk = result[0]
                assert first_chunk["airline"] == "Delta"
                assert first_chunk["locale"] == "en-US"
                assert first_chunk["policy_version"] == "2024.1"
                assert first_chunk["doc_id"] == "test_doc_001"
                assert first_chunk["chunk_id"] == 1
                assert first_chunk["source"] == "/test/policy.md"
                assert len(first_chunk["text"]) <= 50

                # Verify chunk IDs increment
                for i, chunk in enumerate(result):
                    assert chunk["chunk_id"] == i + 1

    def test_split_text_short_text(self):
        """Test splitting text shorter than chunk size."""
        text = "Short text"

        result = split_text(
            text=text,
            airline="United",
            locale="es-ES",
            policy_version="2024.2",
            doc_id="short_doc",
            source="/test/short.md",
        )

        # Should create exactly one chunk
        assert len(result) == 1
        assert result[0]["text"] == "Short text"
        assert result[0]["chunk_id"] == 1

    def test_split_text_empty_input(self):
        """Test handling of empty or whitespace-only text."""
        test_cases = ["", "   ", "\n\t  \n"]

        for empty_text in test_cases:
            result = split_text(
                text=empty_text,
                airline="American Airlines",
                locale="en-US",
                policy_version="2024.1",
                doc_id="empty_doc",
                source="/test/empty.md",
            )

            assert result == []

    def test_split_text_overlap_behavior(self):
        """Test that overlapping works correctly."""
        with patch("travel_assistant.rag.ingestion.splitter.CHUNK_SIZE", 20):
            with patch("travel_assistant.rag.ingestion.splitter.CHUNK_OVERLAP", 5):
                text = "123456789012345678901234567890"  # 30 chars

                result = split_text(
                    text=text,
                    airline="Delta",
                    locale="en-US",
                    policy_version="2024.1",
                    doc_id="overlap_test",
                    source="/test/overlap.md",
                )

                # Should create 2 chunks: [0:20] and [15:30]
                assert len(result) == 2
                assert result[0]["text"] == "12345678901234567890"
                assert result[1]["text"] == "678901234567890"  # text[15:30]

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("airline", "Test Airline"),
            ("locale", "fr-FR"),
            ("policy_version", "v1.0.0"),
            ("doc_id", "special-doc_123"),
            ("source", "/path/with spaces/file.pdf"),
        ],
    )
    def test_split_text_metadata_preservation(self, field_name, field_value):
        """Test that all metadata fields are correctly preserved in chunks."""
        text = "Sample text for metadata testing"

        kwargs = {
            "text": text,
            "airline": "Default Airline",
            "locale": "en-US",
            "policy_version": "2024.1",
            "doc_id": "default_doc",
            "source": "/default/source.md",
        }
        kwargs[field_name] = field_value

        result = split_text(**kwargs)

        assert len(result) == 1
        assert result[0][field_name] == field_value

    def test_split_text_whitespace_stripping(self):
        """Test that chunk text is properly stripped of whitespace."""
        text = "   Some text with leading and trailing spaces   "

        result = split_text(
            text=text,
            airline="Delta",
            locale="en-US",
            policy_version="2024.1",
            doc_id="whitespace_test",
            source="/test/whitespace.md",
        )

        assert len(result) == 1
        assert result[0]["text"] == "Some text with leading and trailing spaces"
