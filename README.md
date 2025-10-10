# Travel Assistant - AI Technical Challenge

A RAG (Retrieval-Augmented Generation) powered travel assistant application that helps users with travel-related queries using airline policies as a knowledge base. The system combines vector search capabilities with AI language models to provide accurate and contextual responses.

## 🚀 Quick Start (Reproducible Setup)

### Prerequisites

- [Docker](https://www.docker.com/get-started) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)
- OpenAI API Key

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai_technical_challenge
```

### 2. Configure Environment Variables

**CRITICAL**: Create and configure your `.env.docker` file with your real API key:

```bash
# Copy the template
cp .env.docker .env.docker.local

# Edit with your real API key
nano .env.docker
```

Update the `.env.docker` file:
```bash
LITELLM_API_KEY=sk-your-real-openai-api-key-here
QDRANT_URL=http://qdrant:6333
ENVIRONMENT=dev
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_SIZE=1536
```

⚠️ **Important**: Replace `sk-your-real-openai-api-key-here` with your actual OpenAI API key from https://platform.openai.com/api-keys

### 3. Start the System

```bash
# Build and start all services (first time)
docker compose up --build

# Or start with data ingestion (if needed)
docker compose up qdrant ingest

# Then start the web application
docker compose up app
```

### 4. Access the Application

- **Web App**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **API Health**: http://localhost:6333/collections/airline_policies

## ✅ Verification Steps

### Check if Data Ingestion was Successful

After running `docker compose up`, verify that documents were properly indexed:

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
# 3. Verify all services are running
docker compose ps
```

**Expected Output:**
```
NAME                     IMAGE                      STATUS
qdrant                   qdrant/qdrant:latest       Up
travel_assistant         ai_technical_challenge-*   Up
travel_assistant_ingest  ai_technical_challenge-*   Exited (0) ✓
```
*Note: `travel_assistant_ingest` exits with code 0 after successful ingestion*

### Access the Application

- **🌐 Web Interface**: http://localhost:8501
- **📊 Qdrant Dashboard**: http://localhost:6333/dashboard
- **🔍 Quick API Test**: http://localhost:6333/collections/airline_policies

### Troubleshooting Verification

**✅ Success Indicators:**
- Qdrant collection shows `"status":"green"` and `"points_count":183`
- Documents contain metadata from all airlines: `American Airlines`, `Delta`, `United`
- Streamlit app loads without errors at http://localhost:8501
- You can ask questions about airline policies and get relevant responses

**❌ Common Issues:**
- `points_count: 0` → API key invalid or ingestion failed
- Connection errors → Services not running or wrong ports
- Empty responses → No data ingested or collection doesn't exist

## 🔧 Complete Reproduction Guide

### For a Fresh Environment (New Machine)

This section shows how to completely reproduce the system from scratch:

```bash
# 1. Clone repository
git clone <your-repo-url>
cd ai_technical_challenge

# 2. Clean any existing Docker state (optional)
docker system prune -f
docker compose down
sudo rm -rf qdrant_storage/*

# 3. Set up environment variables
cp .env.docker.example .env.docker
# Edit .env.docker with your real OpenAI API key

# 4. Build and run complete system
docker compose build --no-cache
docker compose up

# 5. Verify installation (in another terminal)
curl -X GET "http://localhost:6333/collections/airline_policies"
```

### Build Time Expectations
- **Fresh build**: ~45 seconds (optimized dependencies)
- **Data ingestion**: ~30 seconds (183 documents)
- **Total startup**: ~75 seconds from zero to ready

## 🔧 Troubleshooting

### Common Issues

**1. API Key Error (401 Unauthorized)**
```bash
# Check your .env.docker file has a valid OpenAI API key
cat .env.docker
# Make sure LITELLM_API_KEY starts with "sk-proj-" or "sk-" and is valid
```

**2. No Data in Qdrant (points_count: 0)**
```bash
# Run data ingestion manually
docker compose up qdrant ingest
```

**3. Port Already in Use**
```bash
# Check what's using the ports
lsof -i :6333  # Qdrant
lsof -i :8501  # Streamlit

# Stop conflicting services or change ports in docker-compose.yml
```

**4. Build Errors**
```bash
# Clean rebuild
docker compose down
docker system prune -f
docker compose build --no-cache
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
