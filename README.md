# Travel Assistant - AI Technical Challenge

A RAG (Retrieval-Augmented Generation) powered travel assistant application that helps users with travel-related queries using airline policies as a knowledge base. The system combines vector search capabilities with AI language models to provide accurate and contextual responses.

## Architecture

This project consists of:

- **Travel Assistant API**: A Streamlit-based web application that serves as the user interface
- **Qdrant Vector Database**: Stores and retrieves policy documents using vector embeddings
- **RAG System**: Combines retrieval and generation for intelligent responses
- **Policy Documents**: Airline policies from American Airlines, Delta, and United

## Prerequisites

Before starting, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

## Environment Setup

### 1. Environment Configuration

Create a `.env` file in the project root directory. **This file is required** for the service to start properly.

```bash
# Example .env file
LITELLM_API_KEY=your_api_key_here
QDRANT_URL=http://qdrant:6333
ENVIRONMENT=dev
```

**Important**: Without the `.env` file, the containers will fail to start.

### 2. Build and Run

Since there's no Makefile in the current setup, use Docker Compose directly:

```bash
# Build and start all services
docker compose up --build

# Or run in detached mode
docker compose up --build -d
```

This command will:
- Build the application Docker image using the local Dockerfile
- Start Qdrant vector database on port 6333
- Start the Streamlit application on port 8501
- Set up the necessary volume mounts and networking

### 3. Access the Application

Once the containers are running, access the application at:

**http://localhost:8501**

## Stopping Services

To stop and remove all containers:

```bash
docker compose down

# To also remove volumes (will delete stored data)
docker compose down -v
```

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
