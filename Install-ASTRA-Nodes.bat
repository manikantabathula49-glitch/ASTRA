@echo off
set PYTHONUTF8=1
title ASTRA Suite Node Installer
color 0b

echo.
echo  ====================================================
echo       ASTRA SUITE — COMFYUI NODE INSTALLER
echo       Installing all node dependencies
echo  ====================================================
echo.

set PYTHON="%~dp0comfy_env\Scripts\python.exe"

if not exist "%~dp0comfy_env" (
    echo [ERROR] comfy_env not found at %~dp0comfy_env
    echo         Make sure ComfyUI is installed first.
    pause
    exit /b 1
)

echo [1/7] Upgrading pip in comfy_env...
%PYTHON% -m pip install --upgrade pip --quiet
echo       Done.
echo.

echo [2/7] Installing Kokoro TTS (Voice Node)...
%PYTHON% -m pip install "kokoro>=0.9.4" "misaki[en]" soundfile
if errorlevel 1 (
    echo [WARNING] Kokoro install had issues. Voice node may not work.
) else (
    echo       Done.
)
echo.

echo [3/7] Installing fpdf2 (PDF Node)...
%PYTHON% -m pip install fpdf2
if errorlevel 1 (
    echo [WARNING] fpdf2 install had issues. PDF node may not work.
) else (
    echo       Done.
)
echo.

echo [4/7] Installing PyTorch + Diffusers (Video Node)...
echo       (Large download — may take 5-10 minutes)
%PYTHON% -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 --quiet
%PYTHON% -m pip install diffusers transformers accelerate imageio[ffmpeg]
if errorlevel 1 (
    echo [WARNING] Diffusers install had issues. Video node may not work.
) else (
    echo       Done.
)
echo.

echo [5/7] Installing httpx (for API calls)...
%PYTHON% -m pip install httpx --quiet
echo       Done.
echo.

echo [6/7] Installing duckduckgo-search (Web Search Node)...
%PYTHON% -m pip install duckduckgo-search --quiet
echo       Done.
echo.

echo [7/7] Verifying ASTRA Nodes...
%PYTHON% -c "from kokoro import KPipeline; print('  [OK] Voice Node')" 2>nul || echo   [FAIL] Voice Node — check kokoro install
%PYTHON% -c "from fpdf import FPDF; print('  [OK] PDF Node')" 2>nul || echo   [FAIL] PDF Node — check fpdf2 install
%PYTHON% -c "import diffusers, torch; print('  [OK] Video Node')" 2>nul || echo   [FAIL] Video Node — check diffusers install
%PYTHON% -c "import urllib.request; print('  [OK] Brain Node (built-in)')"
%PYTHON% -c "from duckduckgo_search import DDGS; print('  [OK] Web Search Node')" 2>nul || echo   [FAIL] Web Search Node — check duckduckgo-search install
%PYTHON% -c "print('  [OK] Prompt Node (no deps needed)')"
echo.

echo  ====================================================
echo   ASTRA Suite installed in ComfyUI!
echo.
echo   Nodes available under ASTRA/ in ComfyUI:
echo.
echo     ASTRA/AI         ^> ASTRA Brain (Ollama)
echo     ASTRA/AI         ^> ASTRA Web Search
echo     ASTRA/Generation ^> ASTRA Prompt Builder
echo     ASTRA/Generation ^> ASTRA Voice Generator
echo     ASTRA/Generation ^> ASTRA PDF Generator
echo     ASTRA/Generation ^> ASTRA Video Generator
echo.
echo   Restart ComfyUI to load the new nodes.
echo  ====================================================
echo.
pause
