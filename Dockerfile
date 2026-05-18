# Stage 1: Build the Vue frontend
FROM node:20-alpine AS build-frontend
WORKDIR /app/frontend

# Install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy source and build
COPY frontend/ ./
# Use an empty base URL or relative path for production API calls
ENV VITE_API_BASE_URL="/api"
RUN npm run build


# Stage 2: Build the FastAPI backend and serve the combined app
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for psycopg2 and other python packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy built frontend assets
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

# Expose port (Render sets PORT env variable)
EXPOSE 8000

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
