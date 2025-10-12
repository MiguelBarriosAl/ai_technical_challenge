# Travel Assistant - RAG System

RAG (Retrieval-Augmented Generation) system that answers questions about airline policies using vector search and LLM.

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
curl http://localhost:3000

# API
curl http://localhost:8080/health

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

## System Verification

### 1. Verify Qdrant (Vector DB)
```bash
# Collection status
curl "http://localhost:6333/collections/airline_policies"
```
**Expected response:** `"status":"green"`, `"points_count":183`

### 2. Verify API Backend
```bash
# Health check
curl "http://localhost:8080/health"

# Test RAG query
curl -X POST "http://localhost:8080/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Can I travel with pets on Delta?", "airline": "Delta", "locale": "en-US"}'
```

### 3. Verify Frontend
```bash
# Web interface available
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```
**Expected response:** `200`

### 4. Check Services Status
```bash
make status
```





## Project Structure

```
ai_technical_challenge/
├── travel_assistant/              # Python application
│   ├── app/                      # FastAPI backend (routes, models, handlers)
│   │   ├── models/               # Pydantic request/response models
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── routes.py             # API endpoint definitions
│   │   └── error_handlers.py     # Global exception handlers
│   ├── core/                     # Central configuration
│   │   ├── settings.py           # Environment variables & config
│   │   ├── constants.py          # Application constants
│   │   └── errors.py             # Custom exception classes
│   ├── rag/                      # RAG logic (ingestion, retrieval, generation)
│   │   ├── ingestion/            # Document processing pipeline
│   │   ├── retriever_service.py  # Vector similarity search
│   │   ├── generation_service.py # LLM response generation
│   │   └── context_builder.py    # Context assembly for prompts
│   ├── infra/                    # External service clients
│   │   ├── embeddings.py         # OpenAI embeddings via LiteLLM
│   │   ├── llm_client.py         # LLM API client (ChatOpenAI)
│   │   └── qdrant_repository.py  # Vector database operations
│   ├── prompts/                  # LLM prompt templates
│   └── tests/                    # Unit tests
├── policies/                      # Policy documents (ingested data)
│   ├── AmericanAirlines/         # AA policies (4 markdown files)
│   ├── Delta/                    # Delta policies (6 markdown files)
│   └── United/                   # United policies (4 PDF files)
├── qdrant_storage/               # Vector database storage (auto-generated)
├── docker-compose.yml            # Service orchestration definition
├── Dockerfile                    # Application container image
├── frontend.html                 # Static web interface
├── nginx.conf                    # Frontend server configuration
├── Makefile                      # Build automation & CI/CD pipeline
├── .env.docker                   # Docker environment variables
└── pyproject.toml               # Python dependencies (Poetry)
```

## Technical Components

- **FastAPI**: REST API for RAG queries
- **Qdrant**: Vector database for embeddings
- **LangChain**: RAG framework with OpenAI/LiteLLM
- **Nginx**: Web server for static frontend
- **Docker**: Containerization and orchestration



## Testing and Development

```bash
# Tests with make
make test

# Tests with Docker directly
docker-compose run --rm api poetry run pytest

# Linting and formatting
poetry run ruff check .
poetry run black .
```

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

### Manual Execution
```bash
# Run on all files
pre-commit run --all-files
```

## Usage Examples

### Query via API
```bash
curl -X POST "http://localhost:8080/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the baggage restrictions for Delta flights?",
    "airline": "Delta",
    "locale": "en-US"
  }'
```

### Query via Frontend
1. Open http://localhost:3000
2. Use the web interface to ask questions
3. View contextual responses based on policies

## Tech Stack

- **Python 3.11** + **Poetry** (dependency management)
- **FastAPI** (API REST backend)
- **LangChain** + **LiteLLM** (LLM integration)
- **Qdrant** (vector database)
- **Docker** + **Docker Compose** (containerization)
- **Nginx** (frontend web server)
- **Ruff** + **Black** (code quality)
