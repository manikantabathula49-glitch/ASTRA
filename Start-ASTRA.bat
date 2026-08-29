@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set OLLAMA_HOST=0.0.0.0
set OLLAMA_KEEP_ALIVE=-1
set OLLAMA_NUM_PARALLEL=2
set ENABLE_IMAGE_GENERATION=True
set IMAGE_GENERATION_ENGINE=openai
set IMAGES_OPENAI_API_BASE_URL=http://127.0.0.1:8892/v1
set IMAGES_OPENAI_API_KEY=astra
set IMAGE_GENERATION_MODEL=dreamshaper-8
set AUTOMATIC1111_BASE_URL=http://127.0.0.1:8892

:: Disable analytics & telemetry network stalls
set ENABLE_DB_MIGRATIONS=False
set OFFLINE_MODE=True
set ENABLE_VERSION_UPDATE_CHECK=False
set ENABLE_ADMIN_ANALYTICS=False
set ENABLE_OTEL=False
set ENABLE_BASE_MODELS_CACHE=True
set ANONYMIZED_TELEMETRY=False
set CHROMA_TELEMETRY=False
set POSTHOG_DISABLED=1
set SCARF_NO_ANALYTICS=True
set DO_NOT_TRACK=1
set HF_HUB_DISABLE_TELEMETRY=1

:: Open WebUI Chat Suggestions Enabled
set ENABLE_SEARCH_QUERY_GENERATION=False
set ENABLE_RETRIEVAL_QUERY_GENERATION=False
set ENABLE_FOLLOW_UP_GENERATION=True
set ENABLE_TAGS_GENERATION=True
set ENABLE_TITLE_GENERATION=True
set ENABLE_AUTOCOMPLETE_GENERATION=True
set ENABLE_MEMORIES=False
set ENABLE_WEB_SEARCH=False
set AIOHTTP_CLIENT_TIMEOUT=60

title ASTRA AI Ecosystem (Ultra-Speed)
color 0b

echo.
echo  ====================================================
echo      A S T R A   A I   E C O S Y S T E M  (Ultra-Speed)
echo      Booting ComfyUI ^& Open WebUI...
echo  ====================================================
echo.

echo [0/8] Verifying ASTRA Brain (Ollama) ^& Preloading in GPU VRAM...
curl -s -m 2 http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo       Starting Ollama daemon...
    START /B ollama serve >nul 2>&1
    ping -n 3 127.0.0.1 >nul
) else (
    echo       Ollama Brain is already active.
)

REM Warmup model into GPU VRAM for instant sub-second responses
curl -s -m 10 -X POST http://127.0.0.1:11434/api/generate -d "{\"model\":\"astra\",\"keep_alive\":-1}" >nul 2>&1

echo [1/8] Synchronizing Open WebUI High-Speed Settings...
"%~dp0webui_env\Scripts\python.exe" "%~dp0sync_webui_db.py" >nul 2>&1

echo [2/8] Starting Open WebUI Chat (Port 8080)
set DATA_DIR=%~dp0webui_env\Lib\site-packages\open_webui\data
set FRONTEND_BUILD_DIR=%~dp0webui_env\Lib\site-packages\open_webui\frontend
set FROM_INIT_PY=true
set WEBUI_SECRET_KEY=p0/6YLuw3mv6mLiP
set OLLAMA_BASE_URL=http://127.0.0.1:11434
set DEFAULT_MODELS=astra
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set ENABLE_IMAGE_GENERATION=True
START "ASTRA CHAT" /MIN cmd /k "cd /d "%~dp0" && chcp 65001 >nul && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && "%~dp0webui_env\Scripts\python.exe" "run_webui.py""
ping -n 2 127.0.0.1 >nul

echo [3/8] Launching ComfyUI Backend Engine (Port 8188)
START "ASTRA ENGINE" /MIN cmd /k "cd /d "%~dp0" && chcp 65001 >nul && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && "%~dp0comfy_env\Scripts\python.exe" ".\ComfyUI\main.py" --listen 0.0.0.0 --cpu"
ping -n 2 127.0.0.1 >nul

echo [4/8] Launching ASTRA Voice Agent (Port 8880)
START "ASTRA VOICE" /MIN cmd /k "cd /d "%~dp0" && chcp 65001 >nul && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && "%~dp0comfy_env\Scripts\python.exe" ".\voice_server.py""
ping -n 2 127.0.0.1 >nul

echo [5/8] Launching ASTRA Whisper Transcriber (Port 8885)
START "ASTRA WHISPER" /MIN cmd /k "cd /d "%~dp0" && chcp 65001 >nul && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && "%~dp0comfy_env\Scripts\python.exe" ".\whisper_server.py""
ping -n 2 127.0.0.1 >nul

echo [6/7] Launching ASTRA PDF Engine (Port 8890)
START "ASTRA PDF" /MIN cmd /k "cd /d "%~dp0" && chcp 65001 >nul && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && "%~dp0comfy_env\Scripts\python.exe" ".\pdf_server.py""
ping -n 2 127.0.0.1 >nul

echo [7/7] Launching ASTRA Image Engine (Port 8892)
START "ASTRA IMAGE" /MIN cmd /k "cd /d "%~dp0" && chcp 65001 >nul && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && "%~dp0comfy_env\Scripts\python.exe" ".\image_server.py""
ping -n 2 127.0.0.1 >nul

echo.
<nul set /p =" Waiting for Open WebUI server to finish booting"
set WAIT_COUNT=0

:WAIT_LOOP
set /a WAIT_COUNT+=1
curl -s -m 1 http://127.0.0.1:8080/health >nul 2>&1
if %errorlevel% neq 0 (
    <nul set /p =.
    if %WAIT_COUNT% geq 60 goto LAUNCH_BROWSER
    ping -n 2 127.0.0.1 >nul
    goto WAIT_LOOP
)

:LAUNCH_BROWSER
echo.
echo  Opening Open WebUI and ComfyUI in Google Chrome...

set "CHROME_EXE="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not defined CHROME_EXE if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "CHROME_EXE=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if not defined CHROME_EXE if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if defined CHROME_EXE (
    start "" "%CHROME_EXE%" "http://localhost:8080"
    start "" "%CHROME_EXE%" "http://localhost:8188"
) else (
    start "" "http://localhost:8080"
    start "" "http://localhost:8188"
)

echo.
echo  ====================================================
echo   ASTRA IS ONLINE (Ultra-Speed Streaming Active).
echo.
echo   OPEN WEBUI CHAT:  http://localhost:8080
echo   COMFYUI ENGINE:   http://localhost:8188
echo   MEDIA SERVICES:   Image(8892), Voice(8880), PDF(8890)
echo  ====================================================
echo.
