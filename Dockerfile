# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including Graphviz
RUN apt-get update && apt-get install -y \
    graphviz \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and wheel file, then install Python dependencies
COPY requirements.txt .
COPY mcp-1.6.0-py3-none-any.whl .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Remove the Docker-optimized API server overwrite so the local api_server.py is used
# COPY api_server_docker.py api_server.py

# Expose the API server port
EXPOSE 8000

# Create a healthcheck to ensure the API is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
