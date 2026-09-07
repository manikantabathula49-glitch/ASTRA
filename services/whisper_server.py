#!/usr/bin/env python3
"""
ASTRA Whisper Transcription Server
Local Speech-to-Text using OpenAI Whisper (Tiny Model)
Port: 8885
Optimized for low resource footprint (~70MB model)
"""

import os
import uuid
import shutil
import tempfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

TEMP_DIR = os.path.join(tempfile.gettempdir(), "astra_whisper")
os.makedirs(TEMP_DIR, exist_ok=True)

# Global model state
model = None
model_loading = False

def load_model():
    global model, model_loading
    model_loading = True
    print("[ASTRA WHISPER] Loading Whisper tiny model (this may take a moment on first run)...")
    try:
        import whisper
        # Load the tiny model locally (~70MB download)
        model = whisper.load_model("tiny")
        print("[ASTRA WHISPER] Model ready!")
    except Exception as e:
        print(f"[ASTRA WHISPER] Failed to load model: {e}")
    finally:
        model_loading = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context: load the model on startup."""
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, load_model)
    yield


app = FastAPI(title="ASTRA Whisper Server", version="1.0.0", lifespan=lifespan)


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    global model, model_loading
    if model_loading:
        raise HTTPException(status_code=503, detail="Model is still loading. Please wait a moment.")
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Try restarting the server.")

    # Save uploaded file temporarily
    file_ext = os.path.splitext(file.filename)[1] or ".wav"
    temp_path = os.path.join(TEMP_DIR, f"audio_{uuid.uuid4().hex}{file_ext}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"[ASTRA WHISPER] Transcribing temporary file: {temp_path}...")
        
        # Transcribe audio file
        result = model.transcribe(temp_path)
        transcription = result.get("text", "").strip()
        
        print(f"[ASTRA WHISPER] Done! Transcribed: '{transcription[:60]}...'")
        
        return JSONResponse({
            "status": "success",
            "text": transcription,
            "language": result.get("language", "unknown")
        })
        
    except Exception as e:
        print(f"[ASTRA WHISPER] Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.get("/health")
async def health():
    return {
        "status": "online",
        "model": "ready" if model else ("loading" if model_loading else "not loaded")
    }


@app.get("/web", response_class=HTMLResponse)
async def web_ui():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASTRA Whisper Transcriber</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050810;color:#e0e6f0;font-family:'Outfit',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(139,92,246,0.2);border-radius:20px;padding:2.5rem;width:100%;max-width:720px;backdrop-filter:blur(20px);box-shadow:0 0 60px rgba(139,92,246,0.08)}
h1{font-size:2rem;font-weight:700;color:#8b5cf6;text-align:center;margin-bottom:.3rem}
.sub{text-align:center;color:#7a8ba0;font-size:.9rem;margin-bottom:2rem}
label{display:block;font-size:.75rem;color:#7a8ba0;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.4rem}
textarea{width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(139,92,246,0.2);border-radius:12px;color:#e0e6f0;font-family:'Outfit',sans-serif;font-size:1.05rem;padding:1rem;outline:none;transition:border-color .2s;margin-bottom:1.2rem;height:160px;resize:vertical}
textarea:focus{border-color:#8b5cf6}

/* Controls & Panels */
.panels{display:grid;grid-template-columns:1fr;gap:1.5rem;margin-bottom:1.5rem}
@media (min-width: 600px) { .panels{grid-template-columns:1fr 1fr} }
.panel{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:160px}

/* Audio Recording Controls */
.record-btn{width:70px;height:70px;border-radius:50%;background:#ef4444;border:4px solid rgba(255,255,255,0.1);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .3s ease;box-shadow:0 0 20px rgba(239,68,68,0.4);position:relative}
.record-btn:hover{transform:scale(1.05);box-shadow:0 0 30px rgba(239,68,68,0.6)}
.record-btn.recording{background:#fff;animation:pulse-red 1.5s infinite;box-shadow:0 0 30px rgba(239,68,68,0.8)}
.record-btn.recording::after{content:'';width:24px;height:24px;background:#ef4444;border-radius:4px}
.record-btn:not(.recording)::after{content:'';width:24px;height:24px;background:#fff;border-radius:50%}
.timer{margin-top:.8rem;font-size:1.1rem;font-weight:600;color:#cbd5e1}

/* File Upload Controls */
.dropzone{border:2px dashed rgba(139,92,246,0.3);width:100%;height:100%;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all .2s;color:#94a3b8;padding:1rem}
.dropzone:hover{border-color:#8b5cf6;background:rgba(139,92,246,0.03);color:#cbd5e1}
.dropzone input{display:none}
.dropzone svg{margin-bottom:.5rem;color:#8b5cf6}

/* Buttons */
.btn-group{display:flex;gap:1rem}
.btn{flex:1;padding:.9rem;background:linear-gradient(135deg,#8b5cf6,#ec4899);border:none;border-radius:12px;color:#fff;font-family:'Outfit',sans-serif;font-size:1rem;font-weight:700;cursor:pointer;transition:opacity .2s,transform .1s}
.btn:hover{opacity:.9;transform:translateY(-1px)}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none}
.btn-secondary{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#cbd5e1}
.btn-secondary:hover{background:rgba(255,255,255,0.1);color:#fff}

.audio-preview{width:100%;margin-top:1rem;border-radius:8px;outline:none}
.status-box{background:rgba(255,255,255,0.04);border:1px solid rgba(139,92,246,0.15);border-radius:12px;padding:1rem;margin-top:1.2rem;display:none;text-align:center}
.warn{color:#a78bfa;font-size:.8rem;text-align:center;margin-bottom:1.2rem}

@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(239,68,68,0.7)}70%{box-shadow:0 0 0 15px rgba(239,68,68,0)}100%{box-shadow:0 0 0 0 rgba(239,68,68,0)}}
</style>
</head>
<body>
<div class="card">
  <h1>🎙️ ASTRA Whisper Transcriber</h1>
  <p class="sub">Local Speech-to-Text powered by OpenAI Whisper</p>
  <p class="warn">🔒 Processing runs 100% locally. Audio remains strictly private.</p>

  <div class="panels">
    <!-- Voice Recording Panel -->
    <div class="panel">
      <label style="margin-bottom:1rem">Record Microphone</label>
      <button class="record-btn" id="recordBtn" onclick="toggleRecording()"></button>
      <div class="timer" id="timer">00:00</div>
      <audio id="audioPlayback" class="audio-preview" style="display:none" controls></audio>
    </div>

    <!-- File Upload Panel -->
    <div class="panel">
      <label style="margin-bottom:1rem">Upload Audio File</label>
      <div class="dropzone" onclick="document.getElementById('fileInput').click()">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        <span id="fileName">Drop WAV / MP3 / M4A or click to browse</span>
        <input type="file" id="fileInput" accept="audio/*" onchange="handleFileSelect(event)">
      </div>
    </div>
  </div>

  <div class="btn-group">
    <button class="btn btn-secondary" id="copyBtn" onclick="copyText()" disabled>📋 Copy Transcription</button>
    <button class="btn" id="transcribeBtn" onclick="submitTranscription()" disabled>🎙️ Transcribe Audio</button>
  </div>

  <div class="status-box" id="statusBox">
    <p id="statusText">Awaiting input...</p>
  </div>

  <label style="margin-top:1.5rem">Transcription Output</label>
  <textarea id="output" placeholder="Transcription text will appear here..." readonly></textarea>
</div>

<script>
let mediaRecorder;
let audioChunks = [];
let recordInterval;
let startTime;
let audioBlob = null;
let audioFile = null;

function toggleRecording() {
  const btn = document.getElementById('recordBtn');
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    btn.classList.remove('recording');
    clearInterval(recordInterval);
  } else {
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = event => { audioChunks.push(event.data); };
        mediaRecorder.onstop = () => {
          audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          audioFile = null; // Clear uploaded file
          const audioUrl = URL.createObjectURL(audioBlob);
          const player = document.getElementById('audioPlayback');
          player.src = audioUrl;
          player.style.display = 'block';
          document.getElementById('transcribeBtn').disabled = false;
        };
        
        mediaRecorder.start();
        btn.classList.add('recording');
        startTime = Date.now();
        recordInterval = setInterval(updateTimer, 500);
        document.getElementById('audioPlayback').style.display = 'none';
      })
      .catch(e => {
        alert("Microphone access denied: " + e.message);
      });
  }
}

function updateTimer() {
  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
  const s = String(elapsed % 60).padStart(2, '0');
  document.getElementById('timer').textContent = `${m}:${s}`;
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    audioFile = file;
    audioBlob = null; // Clear recorded blob
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('transcribeBtn').disabled = false;
    document.getElementById('audioPlayback').style.display = 'none';
  }
}

async function submitTranscription() {
  const btn = document.getElementById('transcribeBtn');
  const copyBtn = document.getElementById('copyBtn');
  const statusBox = document.getElementById('statusBox');
  const statusText = document.getElementById('statusText');
  
  btn.disabled = true;
  btn.textContent = "⏳ Transcribing...";
  statusBox.style.display = 'block';
  statusText.textContent = "Processing audio locally using Whisper...";
  
  const formData = new FormData();
  if (audioBlob) {
    formData.append("file", audioBlob, "recording.wav");
  } else if (audioFile) {
    formData.append("file", audioFile, audioFile.name);
  } else {
    alert("Please record audio or upload a file first!");
    btn.disabled = false;
    btn.textContent = "🎙️ Transcribe Audio";
    return;
  }
  
  try {
    const r = await fetch('/transcribe', { method: 'POST', body: formData });
    if (!r.ok) {
      const err = await r.json();
      throw new Error(err.detail || "Transcription request failed");
    }
    const data = await r.json();
    document.getElementById('output').value = data.text;
    statusText.textContent = `✅ Transcription Complete! (Language: ${data.language.toUpperCase()})`;
    copyBtn.disabled = false;
  } catch (e) {
    statusText.textContent = "❌ Error: " + e.message;
    console.error(e);
  } finally {
    btn.disabled = false;
    btn.textContent = "🎙️ Transcribe Audio";
  }
}

function copyText() {
  const output = document.getElementById('output');
  output.select();
  document.execCommand('copy');
  alert("Transcribed text copied to clipboard!");
}
</script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn
    print("[ASTRA WHISPER] Starting Whisper transcriber server on port 8885...")
    uvicorn.run(app, host="0.0.0.0", port=8885, log_level="warning")
