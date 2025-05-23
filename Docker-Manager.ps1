# Docker management script for Azure Architecture Diagram Generator
param(
    [switch]$Build,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Logs,
    [switch]$Check,
    [switch]$OpenClient,
    [switch]$Help
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        $null = docker info 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Function to print help
function Show-Help {
    Write-Host "Azure Architecture Diagram Generator Docker Management Script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\Docker-Manager.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Build        Build the Docker image" -ForegroundColor Gray
    Write-Host "  -Start        Start the Docker container" -ForegroundColor Gray
    Write-Host "  -Stop         Stop the Docker container" -ForegroundColor Gray
    Write-Host "  -Restart      Restart the Docker container" -ForegroundColor Gray
    Write-Host "  -Logs         Show container logs" -ForegroundColor Gray
    Write-Host "  -Check        Run health check" -ForegroundColor Gray
    Write-Host "  -OpenClient   Open the web client" -ForegroundColor Gray
    Write-Host "  -Help         Show this help message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\Docker-Manager.ps1 -Build -Start    # Build and start the container" -ForegroundColor Gray
    Write-Host "  .\Docker-Manager.ps1 -Logs            # Show container logs" -ForegroundColor Gray
    Write-Host "  .\Docker-Manager.ps1 -Restart         # Restart the container" -ForegroundColor Gray
    Write-Host ""
}

# Show help if no parameters are provided or -Help is specified
if (($PSBoundParameters.Count -eq 0) -or $Help) {
    Show-Help
    exit 0
}

# Check if Docker is running
if (-not (Test-DockerRunning)) {
    Write-Host "Error: Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Build the Docker image
if ($Build) {
    Write-Host "Building Docker image..." -ForegroundColor Cyan
    docker-compose build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error building Docker image" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Docker image built successfully" -ForegroundColor Green
}

# Start the Docker container
if ($Start) {
    Write-Host "Starting Docker container..." -ForegroundColor Cyan
    docker-compose up -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error starting Docker container" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Docker container started successfully" -ForegroundColor Green
    Write-Host "API server available at: http://localhost:8000" -ForegroundColor Cyan
}

# Stop the Docker container
if ($Stop) {
    Write-Host "Stopping Docker container..." -ForegroundColor Cyan
    docker-compose down
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error stopping Docker container" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Docker container stopped successfully" -ForegroundColor Green
}

# Restart the Docker container
if ($Restart) {
    Write-Host "Restarting Docker container..." -ForegroundColor Cyan
    docker-compose down
    docker-compose up -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error restarting Docker container" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Docker container restarted successfully" -ForegroundColor Green
    Write-Host "API server available at: http://localhost:8000" -ForegroundColor Cyan
}

# Show container logs
if ($Logs) {
    Write-Host "Showing container logs (press Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f
}

# Run health check
if ($Check) {
    Write-Host "Running health check..." -ForegroundColor Cyan
    python check_docker.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Health check failed" -ForegroundColor Red
    } else {
        Write-Host "Health check passed" -ForegroundColor Green
    }
}

# Open the web client
if ($OpenClient) {
    Write-Host "Opening web client..." -ForegroundColor Cyan
    Start-Process "index.html"
}
