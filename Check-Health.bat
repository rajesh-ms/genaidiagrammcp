@echo off
echo Running health check for Azure Architecture Diagram Generator...
echo.

echo Checking if API server is running...
curl -s http://127.0.0.1:8000 > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: API server is not running or not responding!
    echo Starting API server...
    start "API Server" cmd.exe /k "python api_server.py"
    timeout /t 3
    curl -s http://127.0.0.1:8000 > nul
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to start API server!
        echo Please check the following:
        echo - Make sure you have installed all dependencies (pip install -r requirements.txt)
        echo - Make sure port 8000 is not being used by another application
        echo - Check for errors in the API server console
    ) else (
        echo API server started successfully!
    )
) else (
    echo API server is running correctly!
)

echo.
echo Running full health check script...
python check_health.py
if %ERRORLEVEL% NEQ 0 (
    echo Health check failed. Please check the recommendations above.
    echo.
    echo For more detailed troubleshooting:
    echo 1. Use .\Stop-Services.bat to stop all services
    echo 2. Use .\Start-Services.bat to start all services fresh
    echo 3. Check both API Server and MCP Server console windows for errors
    echo 4. Try accessing http://127.0.0.1:8000 directly in your browser
    pause
) else (
    echo Health check passed! The system is ready.
    timeout /t 3
)
