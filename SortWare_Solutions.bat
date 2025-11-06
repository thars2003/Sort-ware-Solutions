@echo off
set "PATH_DIR=%~dp0"
cd /d "%PATH_DIR%User_Interface"


start "Running Sort-ware Solutions" cmd /k python webapp.py
timeout /t 1 >nul

REM Open default browser
start "Opening the website" http://127.0.0.1:5000

pause
