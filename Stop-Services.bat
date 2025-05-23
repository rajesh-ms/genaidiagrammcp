@echo off
echo Stopping all Python processes...
taskkill /f /im python.exe 2>nul
echo Services stopped successfully.
