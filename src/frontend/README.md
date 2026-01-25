# Frontend Component

This directory contains the React + TypeScript frontend application.

## Structure

*   `src/`: Source code for React components and pages.
    *   `pages/`: Application pages (Home, Catalog, Cart, etc.).
    *   `components/`: Reusable UI components.
    *   `api/`: API client configuration.
*   `Dockerfile`: Multi-stage Dockerfile for building the app and serving it with Nginx.
*   `nginx.conf`: Nginx configuration for serving the SPA and proxying API requests.

## How it works

The frontend is a Single Page Application (SPA) built with Vite.

*   **In Docker**: It is built into static files (`dist/`) and served by Nginx on port 80. Nginx is configured to proxy `/api/v1/` requests to the backend service.
*   **Locally**: Runs via `npm run dev` on port 5173.

## Usage

*   **Build**: `npm run build`
*   **Dev Server**: `npm run dev`
