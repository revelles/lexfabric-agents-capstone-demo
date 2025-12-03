# Base Image: Lightweight Python
FROM python:3.11-slim

# Environment Settings
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Ensures logs are streamed to console (critical for Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set Working Directory
WORKDIR /app

# Install System Dependencies (Minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
# We copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Code
COPY . .

# Set Python Path so src modules are discoverable
ENV PYTHONPATH=/app/src

# Expose Port 8000
EXPOSE 8000

# Start the Application
# Uses Uvicorn: An ASGI web server implementation for Python
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]