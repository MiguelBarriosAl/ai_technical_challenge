# Travel Assistant - RAG System

Travel Assistant is a modular Retrieval-Augmented Generation (RAG) system designed to answer questions about airline policies using vector search and Large Language Models (LLMs).

The project demonstrates a clean and production-oriented architecture with clear separation of concerns across ingestion, retrieval, and generation workflows.

# Core Components Overview

## Infrastructure Layer (infra/)

Contains integrations with external services and APIs:

- QdrantRepository – Handles vector storage and retrieval.

- EmbeddingsProvider – Wrapper around OpenAI (via LiteLLM) for text embeddings.

- EmbeddingFactory / Interface – Ensures clean creation, validation, and abstraction of embedding providers.

## Ingestion Workflow (rag/ingestion/)

Processes and indexes airline policy documents:

- Doc Loader – Extracts text from PDFs and Markdown (with error handling for image-based PDFs).

- Splitter – Chunks documents into overlapping text segments (optimized for 800–1000 characters).

- Indexer Service – Generates embeddings, validates vector dimensions, and stores them in Qdrant.

- CLI Runner – Executes the ingestion pipeline for multiple airlines.

### RAG Pipeline (rag/pipeline/)

Handles the question-answering process:

- RetrieverService – Fetches relevant chunks from Qdrant using metadata filters.

- ContextBuilder – Combines and cleans retrieved fragments into a coherent context block.

- RAGGenerationService – Builds a prompt and generates a grounded answer using the LLM.

### Application Layer (app/)

Exposes a simple FastAPI endpoint:

- /ask route orchestrates the full RAG workflow:
  - `retrieve → build context → generate answer`
  - returning both the answer and the supporting context.

### Prompts (prompts/)

Structured prompt templates specialized for different policy types (general, baggage, children travel), ensuring consistent and context-aware responses.

### Key Design Principles

Clean architecture with separated layers for ingestion, retrieval, and generation.

Dependency injection for embeddings and vector storage.

Error isolation and detailed logging for traceability.

Reproducible environment via Poetry and Docker Compose (includes Qdrant).

Comprehensive testing with more than 60 unit and integration tests using Pytest.

## Quick Start

### Requirements
- Docker and Docker Compose
- Make (build automation)
- Valid API Key for LiteLLM

### 1. Configure ENV
```bash
# Edit configuration file
nano .env.docker

# Add your API key:
LITELLM_API_KEY=sk-your-open-ai-api-key
ENVIRONMENT=dev
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_SIZE=1536
```

### 2. Start Complete System
```bash
make          # Execute: tests → build → deploy → verify
```

### 3. Verify Services
```bash
# Frontend
http://localhost:3000

# API
curl http://localhost:8080/health

# Test RAG query
curl -X POST "http://localhost:8080/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Can I travel with pets on Delta?", "airline": "Delta", "locale": "en-US"}'

# Qdrant Vector DB
curl http://localhost:6333/collections/airline_policies
```


## Docker Services

| Service | Port | Description |
|----------|--------|-------------|
| **frontend** | 3000 | Web interface (Nginx) |
| **api** | 8080 | FastAPI backend |
| **qdrant** | 6333 | Vector database |
| **ingest** | - | Document processing (runs and finishes) |

## Make Commands

```bash
make          # Pipeline complete
make help     # Show all commands
make test     # Run tests
make build    # Only build docker
make deploy   # Only run services
make clean    # Stop and clean all services
make status   # Containers status
make logs     # Show logs
```

## Project Structure

```
.
├── docker-compose.yml            # Service orchestration definition
├── Dockerfile                    # Application container image
├── front/                        # Frontend files
│   └── frontend.html             # Static web interface
├── Makefile                      # Build automation & CI/CD pipeline
├── nginx.conf                    # Frontend server configuration
├── poetry.lock                   # Locked dependency versions
├── policies/                     # Policy documents (ingested data)
│   ├── AmericanAirlines/
│   │   ├── Checked bag policy.md
│   │   ├── Pet Policy.md
│   │   ├── Policy.md
│   │   └── Traveling with children.md
│   ├── Delta/
│   │   ├── Baggage & Travel Fees.md
│   │   ├── Children Infant Travel.md
│   │   ├── Frequently Asked Questions.md
│   │   ├── Infant Air Travel.md
│   │   ├── Pets.md
│   │   └── Special Circumstances.md
│   └── United/
│       ├── Checked bags.pdf
│       ├── Flying while Pregnant.pdf
│       ├── Flying with Kids & Family Boarding.pdf
│       └── Traveling with pets.pdf
├── pyproject.toml               # Python dependencies & project config (Poetry)
├── README_challenge.md          # Original challenge requirements
├── README.md                    # Project documentation (this file)
└── travel_assistant/            # Python application
    ├── app/                     # FastAPI backend
    │   ├── error_handlers.py    # Global exception handlers
    │   ├── __init__.py
    │   ├── main.py              # FastAPI application entry point
    │   ├── models/              # Pydantic request/response models
    │   │   ├── ask_models.py    # Request and response data models
    │   │   └── __init__.py
    │   └── routes.py            # API endpoint definitions
    ├── core/                    # Central configuration
    │   ├── constants.py         # Application constants
    │   ├── __init__.py
    │   └── settings.py          # Environment variables & config
    ├── infra/                   # External service clients
    │   ├── embedding_interface.py # Embedding provider interface
    │   ├── embeddings.py        # OpenAI embeddings via LiteLLM
    │   ├── llm_client.py        # LLM API client (ChatOpenAI)
    │   └── qdrant_repository.py # Vector database operations
    ├── __init__.py
    ├── prompts/                 # LLM prompt templates
    │   └── airline_prompts.py   # Airline-specific prompt templates
    ├── rag/                     # RAG system components
    │   ├── ingestion/           # Document processing and indexing
    │   │   ├── cli.py           # Ingestion CLI interface
    │   │   ├── doc_loader.py    # Document loading (PDF, MD)
    │   │   ├── errors.py        # Ingestion-specific exceptions
    │   │   ├── indexer_service.py # Vector indexing to Qdrant
    │   │   ├── ingest_service.py # Ingestion orchestration
    │   │   ├── __init__.py
    │   │   └── splitter.py      # Text chunking and splitting
    │   ├── __init__.py
    │   ├── pipeline/            # RAG pipeline components
    │   │   ├── context_builder.py # Context assembly for prompts
    │   │   ├── errors.py        # Pipeline-specific exceptions
    │   │   ├── generation_service.py # LLM response generation
    │   │   ├── __init__.py
    │   │   └── retriever_service.py # Vector similarity search
    │   └── queries.py           # Query builders and filters
    └── tests/                   # Unit and integration tests
        ├── conftest.py          # Pytest configuration and fixtures
        └── rag/                 # RAG system tests
            ├── ingestion/       # Tests for ingestion components
            │   ├── __init__.py
            │   ├── test_doc_loader.py     # Document loader tests
            │   ├── test_indexer_service.py # Vector indexing tests
            │   ├── test_ingest_service.py  # Ingestion orchestration tests
            │   └── test_splitter.py       # Text chunking tests
            └── pipeline/        # Tests for pipeline components
                ├── __init__.py
                └── test_retriever_service.py # Vector retrieval tests
```

## Technical Components

- **FastAPI**: REST API for RAG queries
- **Qdrant**: Vector database for embeddings
- **LangChain**: RAG framework with OpenAI/LiteLLM
- **Nginx**: Web server for static frontend
- **Docker**: Containerization and orchestration

## Code Quality & Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistent formatting.

### Setup Pre-commit
```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install git hooks
pre-commit install
```

### Pre-commit Configuration
The project includes automated checks for:
- **Black**: Code formatting (line-length: 100)
- **Ruff**: Fast Python linter with auto-fix
- **Trailing whitespace**: Removes extra spaces
- **End-of-file**: Ensures proper file endings

## Tech Stack

- **Python 3.11** + **Poetry** (dependency management)
- **FastAPI** (API REST backend)
- **LangChain** + **LiteLLM** (LLM integration)
- **Qdrant** (vector database)
- **Docker** + **Docker Compose** (containerization)
- **Nginx** (frontend web server)
- **Ruff** + **Black** (code quality)

## Possible Next Improvements

- Advanced Retriever
Integrate hybrid retrieval strategies (vector + keyword filters) or semantic re-ranking (e.g., sentence-transformers) to improve contextual precision and relevance across multiple airlines or policy domains.

- Light Conversational Memory
Add short-term conversational memory to handle follow-up questions (e.g., “What about baggage for children?”).
This can be implemented via an in-memory buffer or Redis cache, appending recent Q&A context before each LLM call.
