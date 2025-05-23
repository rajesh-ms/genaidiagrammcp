@echo off
echo Running health check for Azure Architecture Diagram Generator Docker deployment...
python check_docker.py
if %ERRORLEVEL% NEQ 0 (
    echo Health check failed. Please check the recommendations above.
    pause
) else (
    echo Health check passed! The Docker deployment is working correctly.
    timeout /t 3
)
