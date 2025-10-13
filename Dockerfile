FROM python:3.11-slim

# Avoids Python buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./

RUN pip install --no-cache-dir poetry==2.2.1

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY travel_assistant ./travel_assistant
COPY policies ./policies

RUN poetry install --no-interaction --no-ansi

EXPOSE 8080

ENV PYTHONPATH="/app"

# Default command for FastAPI (can be overridden in docker-compose)
CMD ["uvicorn", "travel_assistant.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
