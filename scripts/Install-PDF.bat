@echo off
set PYTHONUTF8=1
title ASTRA PDF Engine Installer
color 0b

echo.
echo ==============================================
echo      ASTRA PDF ENGINE INSTALLER
echo      fpdf2 + FastAPI Setup
echo ==============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo [1/4] Creating PDF environment...
python -m venv f:\ASTRA\pdf_env
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo       Done: f:\ASTRA\pdf_env created.
echo.

echo [2/4] Activating environment...
call f:\ASTRA\pdf_env\Scripts\activate.bat
echo       Done.
echo.

echo [3/4] Installing PDF dependencies...
python -m pip install --upgrade pip --quiet
pip install fpdf2 fastapi "uvicorn[standard]"
if errorlevel 1 (
    echo [ERROR] Installation failed. Check your internet connection.
    pause
    exit /b 1
)
echo       Done.
echo.

echo [4/4] Verifying installation...
python -c "from fpdf import FPDF; print('fpdf2 OK')"
python -c "import fastapi, uvicorn; print('Server deps OK')"
echo.

echo ==============================================
echo  ASTRA PDF Engine installed successfully!
echo.
echo  Port:  8890
echo  UI:    http://localhost:8890/web
echo.
echo  Run Start-ASTRA.bat to launch everything!
echo ==============================================
echo.
pause
