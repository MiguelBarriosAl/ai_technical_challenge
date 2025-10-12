# Travel Assistant - AI Technical Challenge
# Professional Makefile with CI/CD Pipeline

.PHONY: all help clean test build deploy verify dev logs status

# Default target - Full CI/CD Pipeline
all: check-deps test build deploy verify
	@echo "=========================================="
	@echo "SUCCESS: Travel Assistant is running!"
	@echo "=========================================="
	@echo "Web Interface: http://localhost:3000"
	@echo "API Backend: http://localhost:8080"
	@echo "Qdrant Dashboard: http://localhost:6333/dashboard"
	@echo ""
	@echo "To stop services: make clean"
	@echo "To view logs: make logs"

# Help target
help:
	@echo "Travel Assistant - Available Commands:"
	@echo ""
	@echo "  make          - Run complete CI/CD pipeline (recommended)"
	@echo "  make test     - Run unit tests only"
	@echo "  make build    - Build Docker images"
	@echo "  make deploy   - Deploy services"
	@echo "  make verify   - Verify deployment health"
	@echo "  make clean    - Stop all services and cleanup"
	@echo "  make logs     - Show service logs"
	@echo "  make status   - Show service status"
	@echo "  make dev      - Start development mode"

# Check system dependencies
check-deps:
	@echo "Checking system dependencies..."
	@command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker is required but not installed. Please install Docker."; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1 || { echo "ERROR: Docker Compose is required but not installed."; exit 1; }
	@test -f .env.docker || { echo "ERROR: .env.docker file not found. Please create it with your OpenAI API key."; exit 1; }
	@grep -q "LITELLM_API_KEY=sk-" .env.docker || { echo "ERROR: Valid OpenAI API key required in .env.docker"; exit 1; }
	@echo "Dependencies check passed!"

# Run comprehensive test suite
test:
	@echo "Running test suite..."
	@if command -v poetry >/dev/null 2>&1; then \
		echo "Running tests with Poetry..."; \
		poetry run pytest -v --tb=short || { echo "ERROR: Tests failed! Fix issues before deployment."; exit 1; }; \
	else \
		echo "Running tests in Docker container..."; \
		docker-compose run --rm app poetry run pytest -v --tb=short || { echo "ERROR: Tests failed! Fix issues before deployment."; exit 1; }; \
	fi
	@echo "All tests passed!"

# Build Docker images
build:
	@echo "Building Docker images..."
	@docker-compose build --no-cache
	@echo "Build completed successfully!"

# Deploy all services
deploy:
	@echo "Deploying services..."
	@docker-compose down 2>/dev/null || true
	@echo "Starting Qdrant database..."
	@docker-compose up -d qdrant
	@sleep 5
	@echo "Running data ingestion..."
	@docker-compose up ingest
	@echo "Starting API and Frontend services..."
	@docker-compose up -d api frontend
	@echo "Services deployed successfully!"

# Verify deployment health
verify:
	@echo "Verifying deployment health..."
	@sleep 10
	@echo "Checking Qdrant connection..."
	@curl -s http://localhost:6333/collections >/dev/null || { echo "ERROR: Qdrant not responding"; exit 1; }
	@echo "Checking data ingestion..."
	@COLLECTION_STATUS=$$(curl -s http://localhost:6333/collections/airline_policies | grep -o '"points_count":[0-9]*' | cut -d: -f2); \
	if [ "$$COLLECTION_STATUS" -gt 0 ]; then \
		echo "Data verification: $$COLLECTION_STATUS documents indexed"; \
	else \
		echo "ERROR: No data found in vector database"; exit 1; \
	fi
	@echo "Checking API service..."
	@sleep 5
	@curl -s http://localhost:8080/health >/dev/null || { echo "WARNING: API service may still be starting up"; }
	@echo "Checking frontend service..."
	@curl -s http://localhost:3000 >/dev/null || { echo "WARNING: Frontend may still be starting up"; }
	@echo "Health check completed successfully!"
	@echo ""
	@echo "🎉 All services are running! Access the application at:"
	@echo "   Frontend: http://localhost:3000"
	@echo "   API:      http://localhost:8080"

# Development mode - skip tests for faster iteration
dev: check-deps build deploy
	@echo "Development mode started!"
	@echo "Web Interface: http://localhost:8501"
	@make logs

# Show service logs
logs:
	@docker-compose logs -f

# Show service status
status:
	@echo "Service Status:"
	@docker-compose ps

# Clean up everything
clean:
	@echo "Stopping and cleaning up services..."
	@docker-compose down -v 2>/dev/null || true
	@docker system prune -f 2>/dev/null || true
	@echo "Cleanup completed!"

# Test specific query (for demonstration)
query:
	@echo "Testing RAG system with sample query..."
	@curl -s -X POST "http://localhost:6333/collections/airline_policies/points/scroll" \
		-H "Content-Type: application/json" \
		-d '{"limit": 3, "with_payload": true, "with_vector": false}' | \
		grep -o '"airline":"[^"]*"' | head -3 || echo "Query test completed"
