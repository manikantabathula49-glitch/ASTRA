@echo off
set PYTHONUTF8=1
title ASTRA Voice Agent Installer
color 0b

echo.
echo ==============================================
echo      ASTRA VOICE AGENT INSTALLER
echo      Kokoro TTS + FastAPI Setup
echo ==============================================
echo.

REM ── Check Python ──────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo [1/5] Python detected. Creating Voice environment...
python -m venv f:\ASTRA\voice_env
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo       Done: f:\ASTRA\voice_env created.
echo.

echo [2/5] Activating environment...
call f:\ASTRA\voice_env\Scripts\activate.bat
echo       Done.
echo.

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo       Done.
echo.

echo [4/5] Installing Kokoro TTS and server dependencies...
echo       (This may take a few minutes — downloading model files)
echo.
pip install "kokoro>=0.9.4" "misaki[en]" soundfile fastapi "uvicorn[standard]"
if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed. Check your internet connection and try again.
    pause
    exit /b 1
)
echo.
echo       Done: All dependencies installed.
echo.

echo [5/5] Verifying installation...
python -c "from kokoro import KPipeline; print('Kokoro OK')" 2>&1
python -c "import fastapi, uvicorn, soundfile; print('Server deps OK')" 2>&1
echo.

echo ==============================================
echo  ASTRA Voice Agent installed successfully!
echo.
echo  Voice: af_bella (American Female)
echo  Port:  8880
echo  Test:  http://localhost:8880/web
echo.
echo  Run Start-ASTRA.bat to launch everything!
echo ==============================================
echo.
pause
