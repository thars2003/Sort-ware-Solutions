@echo off
set "PATH_DIR=%~dp0"
cd /d "%PATH_DIR%"

echo Starting Sort-ware Solutions...
start "Running Sort-ware Solutions" cmd /k C:\Python313\python.exe -m User_Interface.webapp

timeout /t 2 >nul

REM Open default browser
start "Opening the website" http://127.0.0.1:5000

pause