@echo off
echo Running environment setup script...
python setup_environment.py
if %ERRORLEVEL% NEQ 0 (
    echo Setup failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Setup completed successfully. 
echo.
echo Next steps:
echo 1. Activate the virtual environment with .venv\Scripts\activate
echo 2. Run the health check with .\Check-Health.bat
echo 3. Run all services with .\Start-Services.bat
echo.

echo Would you like to start the services now? (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    echo Starting services...
    call .\Start-Services.bat
) else (
    echo You can start the services manually with .\Start-Services.bat when ready.
)
pause
