@echo off
set PYTHONUTF8=1
title ASTRA Video Engine Installer
color 0b

echo.
echo ==============================================
echo      ASTRA VIDEO ENGINE INSTALLER
echo      AnimateDiff + DreamShaper Setup
echo ==============================================
echo.
echo NOTE: This will download ~4GB of AI models on first run.
echo       Make sure you have a stable internet connection.
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo [1/5] Creating Video environment...
python -m venv f:\ASTRA\video_env
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo       Done: f:\ASTRA\video_env created.
echo.

echo [2/5] Activating environment...
call f:\ASTRA\video_env\Scripts\activate.bat
echo       Done.
echo.

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo       Done.
echo.

echo [4/5] Installing PyTorch + Diffusers...
echo       (This is a large install — may take 5-10 minutes)
echo.
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate fastapi "uvicorn[standard]" imageio[ffmpeg]
if errorlevel 1 (
    echo [ERROR] Installation failed. Check your internet connection.
    pause
    exit /b 1
)
echo.
echo       Done.
echo.

echo [5/5] Verifying installation...
python -c "import torch; print(f'PyTorch {torch.__version__} — CUDA: {torch.cuda.is_available()}')"
python -c "import diffusers; print(f'Diffusers {diffusers.__version__} OK')"
python -c "import fastapi, uvicorn; print('Server deps OK')"
echo.

echo ==============================================
echo  ASTRA Video Engine installed!
echo.
echo  NOTE: AI Models (~4GB) will be downloaded
echo        automatically on FIRST video generation.
echo        (DreamShaper 8 + AnimateDiff v1.5)
echo.
echo  Port:  8891
echo  UI:    http://localhost:8891/web
echo.
echo  Run Start-ASTRA.bat to launch everything!
echo ==============================================
echo.
pause
