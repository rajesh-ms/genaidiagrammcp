#!/bin/bash
# entrypoint.sh - Entry point script for the Docker container

set -e

# Function to cleanup on exit
cleanup() {
    echo "Shutting down services..."
    if [ -n "$MCP_PID" ]; then
        kill -TERM "$MCP_PID" 2>/dev/null || true
    fi
    exit 0
}

# Trap SIGTERM and SIGINT
trap cleanup SIGTERM SIGINT

echo "Starting Azure Architecture Diagram Generator..."
echo "Deployment mode: ${DEPLOYMENT_MODE:-development}"

# Start the MCP server in the background
python azure_diagram_server_fixed.py &
MCP_PID=$!
echo "MCP Server started with PID: $MCP_PID"

# Sleep to allow MCP server to initialize
sleep 2

# Start the API server (this will run in the foreground)
echo "Starting API Server..."
exec python api_server.py
