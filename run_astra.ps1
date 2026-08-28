# Set Permanent Environment Variables for Windows Ollama Background Service
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "-1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_NUM_PARALLEL", "2", "User")

$env:DATA_DIR="f:\ASTRA\webui_env\Lib\site-packages\open_webui\data"
$env:FRONTEND_BUILD_DIR="f:\ASTRA\webui_env\Lib\site-packages\open_webui\frontend"
$env:FROM_INIT_PY="true"
$env:WEBUI_SECRET_KEY="p0/6YLuw3mv6mLiP"
$env:OLLAMA_HOST="0.0.0.0"
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434"
$env:OLLAMA_KEEP_ALIVE="-1"
$env:OLLAMA_NUM_PARALLEL="2"
$env:ENABLE_IMAGE_GENERATION="True"
$env:IMAGE_GENERATION_ENGINE="openai"
$env:IMAGES_OPENAI_API_BASE_URL="http://127.0.0.1:8892/v1"
$env:IMAGES_OPENAI_API_KEY="astra"
$env:IMAGE_GENERATION_MODEL="dreamshaper-8"
$env:IMAGE_SIZE="512x512"
$env:IMAGE_STEPS="25"
$env:AUTOMATIC1111_BASE_URL="http://127.0.0.1:8892"
$env:DEFAULT_MODELS="astra"
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"

# Disable telemetry, external analytics, and DB migrations for instant boot
$env:ENABLE_DB_MIGRATIONS="False"
$env:OFFLINE_MODE="True"
$env:ENABLE_VERSION_UPDATE_CHECK="False"
$env:ENABLE_ADMIN_ANALYTICS="False"
$env:ENABLE_OTEL="False"
$env:ENABLE_BASE_MODELS_CACHE="True"
$env:ANONYMIZED_TELEMETRY="False"
$env:CHROMA_TELEMETRY="False"
$env:POSTHOG_DISABLED="1"
$env:SCARF_NO_ANALYTICS="True"
$env:DO_NOT_TRACK="1"
$env:HF_HUB_DISABLE_TELEMETRY="1"

# Ultra-Low Latency Settings (Chat Suggestions Enabled)
$env:ENABLE_SEARCH_QUERY_GENERATION="False"
$env:ENABLE_RETRIEVAL_QUERY_GENERATION="False"
$env:ENABLE_FOLLOW_UP_GENERATION="True"
$env:ENABLE_TAGS_GENERATION="True"
$env:ENABLE_TITLE_GENERATION="True"
$env:ENABLE_AUTOCOMPLETE_GENERATION="True"
$env:ENABLE_MEMORIES="False"
$env:ENABLE_WEB_SEARCH="False"
$env:AIOHTTP_CLIENT_TIMEOUT="60"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "    A S T R A   A I   E C O S Y S T E M  (Ultra-Speed)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "[1/9] Ensuring Ollama Brain is Running & Preloaded in GPU VRAM..."
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Warmup model into GPU VRAM for instant responses
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/generate" -Method Post -Body '{"model": "astra", "keep_alive": -1}' -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue | Out-Null
    Write-Host "       ASTRA Model warmed up in GPU VRAM (Keep-Alive: Forever active)" -ForegroundColor Green
} catch {}

Write-Host "[2/9] Synchronizing Open WebUI High-Speed Settings..."
& "f:\ASTRA\webui_env\Scripts\python.exe" "f:\ASTRA\sync_webui_db.py"

Write-Host "[3/9] Starting Open WebUI Chat (Port 8080)..."
Start-Process -FilePath "f:\ASTRA\webui_env\Scripts\python.exe" -ArgumentList "run_webui.py" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden

Write-Host "[4/9] Starting ComfyUI (Port 8188)..."
Start-Process -FilePath "f:\ASTRA\comfy_env\Scripts\python.exe" -ArgumentList ".\ComfyUI\main.py", "--listen", "0.0.0.0", "--cpu" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden
Start-Sleep -Seconds 1

Write-Host "[5/9] Starting Voice Agent (Port 8880)..."
Start-Process -FilePath "f:\ASTRA\comfy_env\Scripts\python.exe" -ArgumentList ".\voice_server.py" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden

Write-Host "[6/9] Starting Whisper Transcriber (Port 8885)..."
Start-Process -FilePath "f:\ASTRA\comfy_env\Scripts\python.exe" -ArgumentList ".\whisper_server.py" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden

Write-Host "[7/9] Starting PDF Engine (Port 8890)..."
Start-Process -FilePath "f:\ASTRA\comfy_env\Scripts\python.exe" -ArgumentList ".\pdf_server.py" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden

Write-Host "[8/9] Starting Video Engine (Port 8891)..."
Start-Process -FilePath "f:\ASTRA\comfy_env\Scripts\python.exe" -ArgumentList ".\video_server.py" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden

Write-Host "[9/9] Starting Image Engine (Port 8892)..."
Start-Process -FilePath "f:\ASTRA\comfy_env\Scripts\python.exe" -ArgumentList ".\image_server.py" -WorkingDirectory "f:\ASTRA" -WindowStyle Hidden

Write-Host "`nWaiting for Open WebUI to complete initialization..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 45; $i++) {
    Write-Host -NoNewline "."
    try {
        $res = Invoke-RestMethod -Uri "http://127.0.0.1:8080/health" -Method Get -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($res.status -eq $true -or $res -ne $null) {
            $ready = $true
            break
        }
    } catch {}
    Start-Sleep -Seconds 1
}

Write-Host ""
$chromeCandidates = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chromePath = $null
foreach ($cand in $chromeCandidates) {
    if (Test-Path $cand) {
        $chromePath = $cand
        break
    }
}

if ($ready) {
    Write-Host "ASTRA AI Ecosystem services are ONLINE! Opening interfaces in Google Chrome..." -ForegroundColor Green
} else {
    Write-Host "ASTRA services launched. Opening interfaces in Google Chrome..." -ForegroundColor Yellow
}

if ($chromePath) {
    Start-Process $chromePath -ArgumentList "http://localhost:8080"
    Start-Process $chromePath -ArgumentList "http://localhost:8188"
} else {
    Start-Process "http://localhost:8080"
    Start-Process "http://localhost:8188"
}
