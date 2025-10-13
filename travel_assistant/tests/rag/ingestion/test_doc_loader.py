"""Unit tests for doc_loader module functions."""

import pytest
from unittest.mock import Mock, patch
from travel_assistant.rag.ingestion.doc_loader import (
    extract_text_from_md,
    extract_text_from_pdf,
    load_document,
)
from travel_assistant.rag.pipeline.errors import ExtractionError


class TestDocLoader:
    """Test class for document loader functions."""

    def test_extract_text_from_md_success(self, temp_md_file):
        """Test successful markdown text extraction."""
        file_path, expected_content = temp_md_file
        result = extract_text_from_md(file_path)
        assert result == expected_content

    def test_extract_text_from_md_file_not_found(self, nonexistent_file_path):
        """Test markdown extraction with non-existent file."""
        with pytest.raises(ExtractionError) as exc_info:
            extract_text_from_md(nonexistent_file_path)
        assert "Failed to extract text from Markdown file" in str(exc_info.value)

    def test_extract_text_from_md_permission_error(self, temp_md_file):
        """Test markdown extraction with permission error."""
        file_path, _ = temp_md_file

        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(ExtractionError) as exc_info:
                extract_text_from_md(file_path)
            assert "Failed to extract text from Markdown file" in str(exc_info.value)

    def test_extract_text_from_pdf_success(self, temp_pdf_file):
        """Test successful PDF text extraction."""
        file_path, expected_content = temp_pdf_file
        result = extract_text_from_pdf(file_path)
        assert expected_content in result
        assert len(result.strip()) > 0

    def test_extract_text_from_pdf_empty_content(self, temp_empty_pdf_file):
        """Test PDF extraction with image-only content (OCR required)."""
        with pytest.raises(ExtractionError) as exc_info:
            extract_text_from_pdf(temp_empty_pdf_file)

        error_message = str(exc_info.value)
        assert "appears to contain only images" in error_message
        assert "OCR required" in error_message

    def test_extract_text_from_pdf_file_not_found(self, nonexistent_file_path):
        """Test PDF extraction with non-existent file."""
        pdf_path = nonexistent_file_path.replace(".md", ".pdf")
        with pytest.raises(ExtractionError) as exc_info:
            extract_text_from_pdf(pdf_path)
        assert "Failed to extract text from PDF file" in str(exc_info.value)

    @patch("travel_assistant.rag.ingestion.doc_loader.fitz.open")
    def test_extract_text_from_pdf_fitz_error(self, mock_fitz_open, temp_pdf_file):
        """Test PDF extraction with fitz library error."""
        file_path, _ = temp_pdf_file
        mock_fitz_open.side_effect = Exception("Fitz error")

        with pytest.raises(ExtractionError) as exc_info:
            extract_text_from_pdf(file_path)
        assert "Failed to extract text from PDF file" in str(exc_info.value)

    def test_extract_text_from_pdf_document_cleanup(self, temp_pdf_file):
        """Test that PDF document is properly closed after extraction."""
        file_path, _ = temp_pdf_file

        with patch("travel_assistant.rag.ingestion.doc_loader.fitz.open") as mock_fitz_open:
            mock_doc = Mock()
            mock_page = Mock()
            mock_page.get_text.return_value = "Test content"
            mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
            mock_fitz_open.return_value = mock_doc

            extract_text_from_pdf(file_path)

            # Verify document was closed
            mock_doc.close.assert_called_once()

    @pytest.mark.parametrize(
        "file_extension,expected_function",
        [
            (".md", "extract_text_from_md"),
            (".pdf", "extract_text_from_pdf"),
        ],
    )
    def test_load_document_dispatch(self, file_extension, expected_function):
        """Test load_document dispatches to correct extraction function."""
        test_file = f"/tmp/test{file_extension}"

        with patch("travel_assistant.rag.ingestion.doc_loader.os.path.isfile", return_value=True):
            patch_path = f"travel_assistant.rag.ingestion.doc_loader.{expected_function}"
            with patch(patch_path) as mock_func:
                mock_func.return_value = "test content"

                result = load_document(test_file)

                mock_func.assert_called_once_with(test_file)
                assert result == "test content"

    def test_load_document_file_not_exists(self, nonexistent_file_path):
        """Test load_document with non-existent file."""
        with pytest.raises(ExtractionError) as exc_info:
            load_document(nonexistent_file_path)
        expected_msg = f"File does not exist: {nonexistent_file_path}"
        assert expected_msg in str(exc_info.value)

    def test_load_document_unsupported_file_type(self, temp_unsupported_file):
        """Test load_document with unsupported file extension."""
        with pytest.raises(ExtractionError) as exc_info:
            load_document(temp_unsupported_file)
        assert "Unsupported file type: .txt" in str(exc_info.value)

    @pytest.mark.parametrize(
        "extension",
        [
            ".MD",
            ".Md",
            ".mD",
            ".PDF",
            ".Pdf",
            ".pDF",
        ],
    )
    def test_load_document_case_insensitive_extensions(self, extension):
        """Test that file extensions are handled case-insensitively."""
        test_file = f"/tmp/test{extension}"
        expected_lower = extension.lower()

        patch_isfile = "travel_assistant.rag.ingestion.doc_loader.os.path.isfile"
        with patch(patch_isfile, return_value=True):
            if expected_lower == ".md":
                patch_path = "travel_assistant.rag.ingestion.doc_loader.extract_text_from_md"
                with patch(patch_path) as mock_func:
                    mock_func.return_value = "content"
                    load_document(test_file)
                    mock_func.assert_called_once_with(test_file)
            elif expected_lower == ".pdf":
                patch_path = "travel_assistant.rag.ingestion.doc_loader.extract_text_from_pdf"
                with patch(patch_path) as mock_func:
                    mock_func.return_value = "content"
                    load_document(test_file)
                    mock_func.assert_called_once_with(test_file)

    def test_load_document_integration_md(self, temp_md_file):
        """Integration test for loading markdown document."""
        file_path, expected_content = temp_md_file
        result = load_document(file_path)
        assert result == expected_content

    def test_load_document_integration_pdf(self, temp_pdf_file):
        """Integration test for loading PDF document."""
        file_path, expected_content = temp_pdf_file
        result = load_document(file_path)
        assert expected_content in result

    def test_exception_chaining_md(self, temp_md_file):
        """Test original exceptions are properly chained in markdown."""
        file_path, _ = temp_md_file

        with patch("builtins.open", side_effect=IOError("Original error")):
            try:
                extract_text_from_md(file_path)
            except ExtractionError as e:
                # Check that the original exception is chained
                assert e.__cause__ is not None
                assert "Original error" in str(e.__cause__)

    def test_exception_chaining_pdf(self, temp_pdf_file):
        """Test original exceptions are properly chained in PDF."""
        file_path, _ = temp_pdf_file

        mock_path = "travel_assistant.rag.ingestion.doc_loader.fitz.open"
        with patch(mock_path, side_effect=IOError("Original error")):
            try:
                extract_text_from_pdf(file_path)
            except ExtractionError as e:
                # Check that the original exception is chained
                assert e.__cause__ is not None
                assert "Original error" in str(e.__cause__)
