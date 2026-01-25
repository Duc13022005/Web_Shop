# Database Component

This directory contains the database initialization scripts and schemas for the Shop application.

## Structure

*   `init.sql`: The primary initialization script. It sets up the PostgreSQL schema, including tables, indexes, and constraints. It may also include initial seed data.

## How it works

When the PostgreSQL container starts (via Docker Compose), it mounts this folder to `/docker-entrypoint-initdb.d/`. Any `.sql` files in this directory are automatically executed in alphabetical order to initialize the database.

## Usage

*   **Modify Schema**: Edit `init.sql` to add tables or change structures.
*   **Reset Data**: To reset the database, you typically need to delete the `postgres_data` volume and restart the container:
    ```bash
    docker-compose down -v
    docker-compose up -d
    ```
