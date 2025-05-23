@echo off
echo Stopping any running Python processes...
taskkill /f /im python.exe 2>nul

echo.
echo Starting MCP Server...
start "MCP Server" cmd.exe /k "python azure_diagram_server.py"
timeout /t 2

echo Starting API Server...
start "API Server" cmd.exe /k "python api_server.py"
timeout /t 2

echo Verifying services...
curl -s http://127.0.0.1:8000 > nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: API Server may not be running correctly!
    echo Please check the API Server console window for errors.
) else (
    echo API Server verified - Running OK!
)

echo Starting Web Client...
start "" index.html

echo.
echo Servers started successfully!
echo.
echo If you have problems connecting:
echo 1. Make sure you have installed all dependencies (pip install -r requirements.txt)
echo 2. Make sure port 8000 is not being used by another application
echo 3. Try running services individually using the VS Code tasks
echo 4. Run Check-Health.bat to verify the servers are running correctly
echo.
