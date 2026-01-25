# Backend Component

This directory contains the Python/FastAPI backend source code.

## Structure

*   `src/`: The main Python package containing the application logic.
    *   `main.py`: Entry point for the FastAPI application.
    *   `core/`: Core configurations, database connections, and security settings.
    *   `auth/`, `users/`, `products/`, `orders/`: Feature modules containing APIs and business logic.
*   `Dockerfile`: Defines the Docker image for the backend service (Python 3.11).
*   `requirements.txt`: Python dependencies.
*   `alembic/`: Database migration scripts (if used).

## How it works

The backend runs as a FastAPI service using `uvicorn`. It connects to the PostgreSQL database and Redis cache defined in the root `docker-compose.yml`.

*   **API Documentation**: Access Swagger UI at `http://localhost:8000/docs`.

## Development

*   Adding dependencies: Update `requirements.txt`.
*   Running locally (without Docker):
    ```bash
    pip install -r requirements.txt
    uvicorn src.main:app --reload
    ```
