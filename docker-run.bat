@echo off
REM Run Docker Compose in different modes

IF "%1"=="" (
    echo Usage: docker-run.bat [development^|production]
    echo.
    echo Examples:
    echo   docker-run.bat development  - Run in development mode
    echo   docker-run.bat production   - Run in production mode
    exit /b 1
)

IF /I "%1"=="development" (
    echo Running in development mode...
    set DEPLOYMENT_MODE=development
    set LOG_LEVEL=DEBUG
    set ENABLE_REQUEST_LOGGING=true
) ELSE IF /I "%1"=="production" (
    echo Running in production mode...
    set DEPLOYMENT_MODE=production
    set LOG_LEVEL=INFO
    set ENABLE_REQUEST_LOGGING=true
) ELSE (
    echo Unknown mode: %1
    echo Valid modes are: development, production
    exit /b 1
)

echo Starting Docker container in %DEPLOYMENT_MODE% mode...
docker-compose up -d
