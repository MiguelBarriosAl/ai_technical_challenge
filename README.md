# Travel Assistant - AI Technical Challenge

A RAG (Retrieval-Augmented Generation) powered travel assistant application that helps users with travel-related queries using airline policies as a knowledge base. The system combines vector search capabilities with AI language models to provide accurate and contextual responses.

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)
- OpenAI API Key

### Setup and Run

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_technical_challenge
   ```

2. **Configure environment**
   ```bash
   # Create environment file with your OpenAI API key
   cp .env.docker.example .env.docker
   # Edit .env.docker and add your API key:
   # LITELLM_API_KEY=sk-your-actual-openai-api-key-here
   ```

3. **Start the application** (One command - includes tests, build, and deployment)
   ```bash
   make
   ```

The system will:
- Run comprehensive tests
- Build Docker images
- Deploy all services (Qdrant + Web App)
- Ingest airline policy documents
- Verify system health

### Access the Application

- **Web Interface**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **API Health**: http://localhost:6333/collections/airline_policies

### Additional Commands

```bash
make          # Run
make help     # Show all available commands
make test     # Run tests only
make clean    # Stop all services
make status   # Check service status
make logs     # View service logs
```

## Verification

### Check System Status

After running `make`, verify that everything is working:

```bash
# 1. Check Qdrant collection status and document count
curl -X GET "http://localhost:6333/collections/airline_policies"
```

**Expected Response:**
```json
{
  "result": {
    "status": "green",
    "points_count": 183,
    "indexed_vectors_count": 183,
    "vectors_count": 183,
    "segments_count": 1,
    "config": {
      "params": {
        "vectors": {
          "size": 1536,
          "distance": "Cosine"
        }
      }
    }
  }
}
```

```bash
# 2. Check some indexed documents with metadata
curl -X POST "http://localhost:6333/collections/airline_policies/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{"limit": 3, "with_payload": true, "with_vector": false}'
```

**Expected Response:**
```json
{
  "result": {
    "points": [
      {
        "id": "uuid-here",
        "payload": {
          "source": "policies/AmericanAirlines/Policy.md",
          "page_content": "American Airlines policy content..."
        }
      }
    ]
  }
}
```

```bash
# 3. Check service health
make status
```

**Success Indicators:**
- Qdrant collection shows `"status":"green"` and `"points_count":183`
- All services show status "Up"
- Web interface responds at http://localhost:8501
- You can ask questions about airline policies and get relevant responses

## System Architecture

### Troubleshooting

**API Key Issues:**
- Ensure `.env.docker` contains valid OpenAI API key starting with `sk-`
- Check key has sufficient credits and permissions

**System Issues:**
```bash
make clean    # Stop all services
make          # Restart complete pipeline
make logs     # Check service logs
```

**Build Issues:**
```bash
make clean    # Clean everything
make build    # Rebuild images
```

## Architecture

This project consists of:

- **Streamlit Web App**: User interface on port 8501
- **Qdrant Vector Database**: Document storage and vector search on port 6333
- **RAG Ingestion**: Processes airline policies into searchable chunks
- **OpenAI Embeddings**: High-quality text embeddings via API
- **Policy Documents**: American Airlines, Delta, and United policies
- Start the Streamlit application on port 8501
- Set up the necessary volume mounts and networking

### 3. Access the Application

Once the containers are running, access the application at:

**http://localhost:8501**

## 🐳 Docker Commands Reference

```bash
# Start everything (recommended)
docker compose up --build

# Start only specific services
docker compose up qdrant          # Just the database
docker compose up qdrant ingest   # Database + data ingestion
docker compose up app             # Just the web app (needs data)

# Check logs
docker compose logs app           # Streamlit logs
docker compose logs qdrant        # Database logs
docker compose logs ingest        # Ingestion logs

# Stop services
docker compose down               # Stop and remove containers
docker compose down -v           # Also remove data volumes

# Rebuild from scratch
docker compose down
docker compose build --no-cache
docker compose up
```

## 💡 Development Notes

### Why This Setup Works
- ✅ **No local Python environment needed** - Everything runs in Docker
- ✅ **Fast builds** - ~4 seconds (no heavy ML dependencies)
- ✅ **Lightweight images** - ~500MB (vs 3+ GB with sentence-transformers)
- ✅ **Production ready** - OpenAI embeddings for quality
- ✅ **Persistent data** - Qdrant data survives container restarts

### For Production Deployment
- Update `.env.docker` with production API keys
- Use Docker secrets for sensitive data
- Configure proper networking and load balancing
- Monitor OpenAI API usage and costs

## Project Structure

```
ai_technical_challenge/
├── travel_assistant/           # Main application package
│   ├── app/                   # Streamlit web application
│   ├── core/                  # Core configurations and settings
│   ├── rag/                   # RAG (Retrieval-Augmented Generation) logic
│   └── tests/                 # Unit tests
├── policies/                  # Airline policy documents
│   ├── AmericanAirlines/      # American Airlines policies
│   ├── Delta/                 # Delta Airlines policies
│   └── United/                # United Airlines policies
├── qdrant_storage/            # Qdrant database storage (auto-generated)
├── docker-compose.yml         # Multi-container Docker application
├── Dockerfile                 # Application container definition
├── pyproject.toml            # Poetry dependencies and project metadata
└── .env                      # Environment variables (create this file)
```

### Key Files Description

| File/Folder | Description |
|-------------|-------------|
| `Dockerfile` | Builds the application image with Python 3.11, Poetry, and Streamlit |
| `docker-compose.yml` | Orchestrates the `qdrant` and `app` services with proper networking |
| `.env` | Contains environment-specific settings (API keys, URLs, etc.) |
| `pyproject.toml` | Poetry configuration with dependencies and development tools |
| `policies/` | Knowledge base containing airline policy documents |

## Code Quality and Best Practices

This project maintains high code quality through automated tools:

### **Black** - Code Formatter
Automatically applies consistent formatting following PEP8 guidelines:
```bash
poetry run black .
```

### **Ruff** - Ultra-fast Linter
Detects errors, bad practices, and unused imports:
```bash
# Check for issues
poetry run ruff check .

# Auto-fix issues
poetry run ruff check --fix .
```

### **Pre-commit** - Git Hooks
Ensures code quality before commits by running Black and Ruff automatically:
```bash
# Install pre-commit hooks
poetry run pre-commit install

# Manually run all hooks
poetry run pre-commit run --all-files
```

## Development Workflow

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_technical_challenge
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env  # if available, or create manually
   # Edit .env with your API keys
   ```

3. **Start services**
   ```bash
   docker compose up --build
   ```

4. **Install pre-commit hooks** (for contributors)
   ```bash
   poetry run pre-commit install
   ```

### Running Tests

```bash
# Run tests inside the container
docker compose exec app poetry run pytest

# Or run locally if you have Poetry installed
poetry run pytest
```

## Configuration

The application uses environment variables for configuration:

- `LITELLM_API_KEY`: API key for the language model service
- `QDRANT_URL`: URL for the Qdrant vector database
- `ENVIRONMENT`: Deployment environment (dev/prod)

## Technology Stack

- **Backend**: Python 3.11, Poetry
- **Frontend**: Streamlit
- **Vector Database**: Qdrant
- **Containerization**: Docker & Docker Compose
- **Code Quality**: Black, Ruff, Pre-commit
- **Testing**: Pytest

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install pre-commit hooks (`poetry run pre-commit install`)
4. Make your changes
5. Run tests and linting
6. Commit your changes (pre-commit hooks will run automatically)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is part of an AI technical challenge and is intended for evaluation purposes.
