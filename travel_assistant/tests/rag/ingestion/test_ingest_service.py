import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch
from travel_assistant.rag.ingestion.ingest_service import run_ingestion


class TestIngestService:
    """Test class for ingestion service functionality."""

    @pytest.fixture
    def mock_indexer(self):
        """Mock IndexerService for testing."""
        from unittest.mock import Mock

        mock_indexer = Mock()
        mock_indexer.index_chunks = Mock()
        return mock_indexer

    @pytest.fixture
    def temp_airline_structure(self):
        """Create temporary directory structure with airline files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)

            # Create airline directory
            airline_dir = base_path / "Delta"
            airline_dir.mkdir()

            # Create supported files
            (airline_dir / "policy.md").write_text("# Delta Policy\nThis is a test policy.")
            (airline_dir / "baggage.pdf").write_text("PDF content placeholder")

            # Create unsupported file
            (airline_dir / "ignored.txt").write_text("This should be ignored")

            yield str(base_path)

    @pytest.fixture
    def mock_dependencies(self):
        """Mock all external dependencies."""
        with patch(
            "travel_assistant.rag.ingestion.ingest_service.load_document"
        ) as mock_load, patch(
            "travel_assistant.rag.ingestion.ingest_service.split_text"
        ) as mock_split, patch(
            "travel_assistant.rag.ingestion.ingest_service.logger"
        ) as mock_logger:

            # Configure default returns
            mock_load.return_value = "Sample document content"
            mock_split.return_value = [
                {
                    "text": "Sample chunk 1",
                    "airline": "Delta",
                    "locale": "en-US",
                    "policy_version": "2024.1",
                    "doc_id": "policy",
                    "chunk_id": 1,
                    "source": "/path/to/policy.md",
                }
            ]

            yield {
                "load_document": mock_load,
                "split_text": mock_split,
                "logger": mock_logger,
            }

    def test_run_ingestion_success(self, temp_airline_structure, mock_dependencies, mock_indexer):
        """Test successful ingestion of airline documents."""
        run_ingestion(
            base_path=temp_airline_structure,
            airline="Delta",
            locale="en-US",
            policy_version="2024.1",
            indexer=mock_indexer,
        )

        # Verify documents were loaded
        assert mock_dependencies["load_document"].call_count == 2  # .md and .pdf files

        # Verify texts were split
        assert mock_dependencies["split_text"].call_count == 2

        # Verify chunks were indexed
        mock_indexer.index_chunks.assert_called_once()

        # Verify logging
        mock_dependencies["logger"].info.assert_called()

    def test_run_ingestion_airline_not_found(
        self, temp_airline_structure, mock_dependencies, mock_indexer
    ):
        """Test ingestion with non-existent airline directory."""
        run_ingestion(
            base_path=temp_airline_structure,
            airline="NonExistentAirline",
            locale="en-US",
            policy_version="2024.1",
            indexer=mock_indexer,
        )

        # Should log error and return early
        mock_dependencies["logger"].error.assert_called_with(
            f"Airline folder not found: {temp_airline_structure}/NonExistentAirline"
        )

        # Should not process any documents
        mock_dependencies["load_document"].assert_not_called()
        mock_indexer.index_chunks.assert_not_called()

    def test_run_ingestion_file_filtering(
        self, temp_airline_structure, mock_dependencies, mock_indexer
    ):
        """Test that only supported file formats are processed."""
        run_ingestion(
            base_path=temp_airline_structure,
            airline="Delta",
            locale="en-US",
            policy_version="2024.1",
            indexer=mock_indexer,
        )

        # Should process only .md and .pdf files (not .txt)
        assert mock_dependencies["load_document"].call_count == 2

        # Should log warning about unsupported file
        mock_dependencies["logger"].warning.assert_any_call(
            "Skipping unsupported file format: ignored.txt"
        )

    def test_run_ingestion_document_loading_error(
        self, temp_airline_structure, mock_dependencies, mock_indexer
    ):
        """Test handling of document loading errors."""
        # Make load_document raise an exception for one file
        mock_dependencies["load_document"].side_effect = [
            "Success content",
            Exception("Failed to load PDF"),
        ]
        mock_dependencies["split_text"].return_value = [{"text": "chunk"}]

        run_ingestion(
            base_path=temp_airline_structure,
            airline="Delta",
            locale="en-US",
            policy_version="2024.1",
            indexer=mock_indexer,
        )

        # Should still process the successful file
        mock_indexer.index_chunks.assert_called_once()

        # Should log error for failed file
        mock_dependencies["logger"].error.assert_called()

    def test_run_ingestion_no_valid_chunks(
        self, temp_airline_structure, mock_dependencies, mock_indexer
    ):
        """Test ingestion when no valid chunks are extracted."""
        # Configure split_text to return empty chunks
        mock_dependencies["split_text"].return_value = []

        run_ingestion(
            base_path=temp_airline_structure,
            airline="Delta",
            locale="en-US",
            policy_version="2024.1",
            indexer=mock_indexer,
        )

        # Should not call indexer
        mock_indexer.index_chunks.assert_not_called()

        # Should log warning about no chunks
        mock_dependencies["logger"].warning.assert_any_call("No chunks indexed for Delta")

    def test_run_ingestion_empty_airline_directory(self, mock_dependencies, mock_indexer):
        """Test ingestion with empty airline directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            airline_dir = base_path / "EmptyAirline"
            airline_dir.mkdir()  # Create empty directory

            run_ingestion(
                base_path=str(base_path),
                airline="EmptyAirline",
                locale="en-US",
                policy_version="2024.1",
                indexer=mock_indexer,
            )

            # Should not process any files
            mock_dependencies["load_document"].assert_not_called()
            mock_indexer.index_chunks.assert_not_called()

            # Should log warning about no chunks
            mock_dependencies["logger"].warning.assert_called_with(
                "No chunks indexed for EmptyAirline"
            )

    def test_run_ingestion_parameter_passing(
        self, temp_airline_structure, mock_dependencies, mock_indexer
    ):
        """Test that parameters are correctly passed to split_text."""
        run_ingestion(
            base_path=temp_airline_structure,
            airline="TestAirline",
            locale="fr-FR",
            policy_version="v2.5.0",
            indexer=mock_indexer,
        )

        # Verify split_text was called with correct parameters
        calls = mock_dependencies["split_text"].call_args_list
        if calls:  # If files were processed
            for call in calls:
                args, kwargs = call
                assert kwargs["airline"] == "TestAirline"
                assert kwargs["locale"] == "fr-FR"
                assert kwargs["policy_version"] == "v2.5.0"
                assert "doc_id" in kwargs
                assert "source" in kwargs

    @patch("travel_assistant.rag.ingestion.ingest_service.SUPPORTED_FILE_FORMATS", {".md"})
    def test_run_ingestion_different_supported_formats(
        self, temp_airline_structure, mock_dependencies, mock_indexer
    ):
        """Test ingestion with different supported file formats configuration."""
        run_ingestion(
            base_path=temp_airline_structure,
            airline="Delta",
            locale="en-US",
            policy_version="2024.1",
            indexer=mock_indexer,
        )

        # Should only process .md files now
        assert mock_dependencies["load_document"].call_count == 1

        # Should warn about PDF file being unsupported
        mock_dependencies["logger"].warning.assert_any_call(
            "Skipping unsupported file format: baggage.pdf"
        )
