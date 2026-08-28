#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASTRA Voice Server
OpenAI-compatible TTS API powered by Kokoro TTS
Default Voice: af_bella (American Female - Confident & Clear)
Port: 8880
"""

import io
import logging
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="[ASTRA VOICE] %(asctime)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ASTRA-Voice")

# Global pipeline — loaded once at startup to save memory
pipeline = None
SAMPLE_RATE = 24000
DEFAULT_VOICE = "af_bella"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context: load TTS on startup, clean up on shutdown."""
    global pipeline
    logger.info("Initializing Kokoro TTS engine...")
    try:
        from kokoro import KPipeline
        # 'a' = American English (af_* and am_* voices)
        pipeline = KPipeline(lang_code="a")
        logger.info(f"Kokoro TTS ready! Default voice: {DEFAULT_VOICE}")
    except Exception as e:
        logger.error(f"Failed to load Kokoro TTS: {e}")
        logger.error("Run Install-Voice.bat to set up the voice environment.")
    yield  # Server runs while yielded
    # Cleanup on shutdown
    pipeline = None
    logger.info("ASTRA Voice Server shut down.")


app = FastAPI(title="ASTRA Voice Server", version="1.0.0", docs_url="/docs", lifespan=lifespan)


# ─── Models ───────────────────────────────────────────────────────────────────

class TTSRequest(BaseModel):
    model: str = "kokoro"
    input: str
    voice: str = DEFAULT_VOICE
    response_format: str = "wav"
    speed: float = 1.0


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/v1/audio/speech")
async def text_to_speech(request: TTSRequest):
    """OpenAI-compatible TTS endpoint."""
    global pipeline

    if pipeline is None:
        raise HTTPException(status_code=503, detail="TTS model not loaded yet. Please wait.")

    if not request.input.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        import soundfile as sf

        logger.info(f"Generating speech | voice={request.voice} | text={request.input[:60]}...")
        audio_chunks = []

        for _, _, audio in pipeline(request.input, voice=request.voice, speed=request.speed):
            if audio is not None:
                audio_chunks.append(audio)

        if not audio_chunks:
            raise HTTPException(status_code=500, detail="No audio was generated.")

        combined = np.concatenate(audio_chunks)

        buf = io.BytesIO()
        sf.write(buf, combined, SAMPLE_RATE, format="WAV")
        buf.seek(0)

        logger.info("Speech generated successfully.")
        return StreamingResponse(
            buf,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=astra_speech.wav"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS generation error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")


@app.get("/v1/models")
async def list_models():
    """OpenAI-compatible model list."""
    return {
        "object": "list",
        "data": [
            {"id": "kokoro", "object": "model", "owned_by": "astra", "created": 1700000000}
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "online" if pipeline else "loading",
        "engine": "kokoro",
        "default_voice": DEFAULT_VOICE,
        "sample_rate": SAMPLE_RATE
    }


@app.get("/web", response_class=HTMLResponse)
async def web_ui():
    """ASTRA Voice Test UI."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASTRA Voice Server</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #050810;
            color: #e0e6f0;
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(100, 200, 255, 0.15);
            border-radius: 20px;
            padding: 2.5rem;
            width: 100%;
            max-width: 640px;
            backdrop-filter: blur(20px);
            box-shadow: 0 0 60px rgba(0, 180, 255, 0.07);
        }
        .header { text-align: center; margin-bottom: 2rem; }
        .header h1 { font-size: 2rem; font-weight: 700; color: #64c8ff; letter-spacing: -0.5px; }
        .header p { color: #7a8ba0; font-size: 0.9rem; margin-top: 0.3rem; }
        .status-dot {
            display: inline-block;
            width: 8px; height: 8px;
            border-radius: 50%;
            background: #00ff88;
            margin-right: 6px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        label { display: block; font-size: 0.8rem; color: #7a8ba0; margin-bottom: 0.4rem; letter-spacing: 0.05em; text-transform: uppercase; }
        textarea, select {
            width: 100%;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(100, 200, 255, 0.2);
            border-radius: 12px;
            color: #e0e6f0;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            padding: 0.9rem 1rem;
            outline: none;
            transition: border-color 0.2s;
            margin-bottom: 1.2rem;
        }
        textarea { height: 120px; resize: vertical; }
        textarea:focus, select:focus { border-color: #64c8ff; }
        select option { background: #0d1117; }
        .btn {
            width: 100%;
            padding: 0.9rem;
            background: linear-gradient(135deg, #64c8ff, #a78bfa);
            border: none;
            border-radius: 12px;
            color: #050810;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
            letter-spacing: 0.05em;
        }
        .btn:hover { opacity: 0.9; transform: translateY(-1px); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        audio { width: 100%; margin-top: 1.2rem; border-radius: 8px; }
        .badge {
            display: inline-block;
            background: rgba(0,255,136,0.1);
            border: 1px solid rgba(0,255,136,0.3);
            color: #00ff88;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>🎙️ ASTRA Voice</h1>
            <p><span class="status-dot"></span>Kokoro TTS Engine — Online</p>
            <span class="badge">af_bella · American Female</span>
        </div>

        <label>Text Input</label>
        <textarea id="text" placeholder="Type something for ASTRA to say...">Hello, I am ASTRA, your personal AI engineer and creator. How can I help you today?</textarea>

        <label>Voice</label>
        <select id="voice">
            <option value="af_bella" selected>af_bella — American Female (Default)</option>
            <option value="af_sky">af_sky — American Female (Soft)</option>
            <option value="af_sarah">af_sarah — American Female (Natural)</option>
            <option value="af_nicole">af_nicole — American Female (Confident)</option>
            <option value="bf_emma">bf_emma — British Female (Elegant)</option>
            <option value="bf_isabella">bf_isabella — British Female (Refined)</option>
        </select>

        <button class="btn" id="speakBtn" onclick="speak()">▶ &nbsp; Generate Speech</button>
        <audio id="audio" controls></audio>
    </div>

    <script>
        async function speak() {
            const btn = document.getElementById('speakBtn');
            const text = document.getElementById('text').value.trim();
            const voice = document.getElementById('voice').value;
            if (!text) return;
            btn.disabled = true;
            btn.textContent = '⏳  Generating...';
            try {
                const resp = await fetch('/v1/audio/speech', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model: 'kokoro', input: text, voice: voice })
                });
                if (!resp.ok) throw new Error(await resp.text());
                const blob = await resp.blob();
                const audio = document.getElementById('audio');
                audio.src = URL.createObjectURL(blob);
                audio.play();
            } catch (e) {
                alert('Error: ' + e.message);
            } finally {
                btn.disabled = false;
                btn.textContent = '▶  Generate Speech';
            }
        }
    </script>
</body>
</html>
"""


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ASTRA Voice Server on port 8880...")
    uvicorn.run(app, host="0.0.0.0", port=8880, log_level="warning")
