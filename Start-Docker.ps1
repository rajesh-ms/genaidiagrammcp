# Run Docker commands to build and start the containers
Write-Host "Building and starting Docker containers..." -ForegroundColor Cyan

# Check if Docker is installed and running
try {
    docker info | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error: Docker is not installed or not in PATH. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Build and start the containers
Write-Host "Running docker-compose up..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDocker containers started successfully!" -ForegroundColor Green
    Write-Host "`nAPI Server is available at: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "To view the logs, run: docker-compose logs -f" -ForegroundColor Cyan
    Write-Host "To stop the containers, run: .\Stop-Docker.ps1" -ForegroundColor Cyan
    
    # Ask if user wants to open the web client
    $openClient = Read-Host "`nDo you want to open the web client now? (y/n)"
    if ($openClient -eq "y" -or $openClient -eq "Y") {
        Write-Host "Opening web client..." -ForegroundColor Yellow
        Start-Process "index.html"
    }
} else {
    Write-Host "`nError starting Docker containers. Please check the error messages above." -ForegroundColor Red
}
