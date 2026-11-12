@echo off
title Elite PLUS - Servidor Local
cd /d "%~dp0"

echo  ========================================
echo    Elite PLUS - Servidor Local
echo  ========================================
echo.

echo  Fechando servidor anterior na porta 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)
timeout /t 1 >nul

echo  Iniciando servidor com live reload em http://localhost:8000
echo  (feche esta janela para parar o servidor)
echo.

start "" http://localhost:8000/index.html

where py >nul 2>&1
if %errorlevel%==0 (
    py server.py
) else (
    python server.py
)
pause
