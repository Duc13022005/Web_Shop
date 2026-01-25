# Source Code Structure & Guide

This folder (`src/`) contains the complete source code for the 7coMART project, organized into three main components: Database, Backend, and Frontend.

## 📂 Directory Structure

```
src/
├── backend/       # Python FastAPI Backend
│   ├── src/       # Application code
│   ├── Dockerfile
│   └── ...
├── frontend/      # React TypeScript Frontend
│   ├── src/       # React components
│   ├── Dockerfile
│   └── nginx.conf
└── db/            # Database Initialization
    ├── init.sql
    └── ...
```

## 🚀 How to Run the Whole System (Docker)

We have refactored the project to run entirely on Docker, including the frontend.

1.  **Navigate to the project root** (where `docker-compose.yml` is located).
2.  **Build and Start**:
    ```bash
    docker-compose up --build -d
    ```
    This command will:
    *   Build the Backend image.
    *   Build the Frontend image (compile React to static HTML/JS).
    *   Start PostgreSQL, Redis, Backend, and Frontend containers.

3.  **Access the Application**:
    *   **Web Store**: [http://localhost](http://localhost) (Served by Nginx on port 80)
        *   *Note: Previously ran on port 5173, but the Dockerized production version runs on port 80.*
    *   **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠 Component Roles

*   **Frontend**: Runs Nginx. Serves the UI and forwards `/api` requests to the backend.
*   **Backend**: Runs Uvicorn. Handles API logic, connects to DB.
*   **DB**: Runs PostgreSQL. Stores data.
*   **Redis**: Caches data.

## 📝 Notes

*   If you encounter "File in use" errors during development, ensure checking `docker-compose logs` to see if a container is restarting or locked.
*   To stop: `docker-compose down`.
