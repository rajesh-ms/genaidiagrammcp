# Stop Docker containers
Write-Host "Stopping Docker containers..." -ForegroundColor Yellow

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker containers stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "Error stopping Docker containers. Please check the error messages above." -ForegroundColor Red
}
