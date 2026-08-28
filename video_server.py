#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASTRA Video Generation Server
Text-to-Video using AnimateDiff + DreamShaper 8
Port: 8891
Optimized for 4GB VRAM (float16 + CPU offload)
"""

import os, uuid, asyncio, time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional

import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, DDIMScheduler

OUTPUT_DIR = "f:\\ASTRA\\video_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global pipeline — loaded once on first use
pipeline = None
pipeline_loading = False
jobs: dict = {}   # job_id → {"status", "filename", "error", "progress"}


# ─── Pipeline Loader ─────────────────────────────────────────────────────────

def load_pipeline():
    global pipeline, pipeline_loading
    if pipeline is not None:
        return pipeline
    pipeline_loading = True
    print("[ASTRA VIDEO] Loading AnimateDiff pipeline (this may take a minute)...")
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32

        adapter = MotionAdapter.from_pretrained(
            "guoyww/animatediff-motion-adapter-v1-5-2",
            torch_dtype=dtype,
        )
        local_sd = r"f:\ASTRA\ComfyUI\models\checkpoints\v1-5-pruned-emaonly.safetensors"
        if os.path.exists(local_sd):
            try:
                pipe = AnimateDiffPipeline.from_single_file(
                    local_sd,
                    motion_adapter=adapter,
                    torch_dtype=dtype,
                )
            except Exception:
                pipe = AnimateDiffPipeline.from_pretrained(
                    "Lykon/dreamshaper-8",
                    motion_adapter=adapter,
                    torch_dtype=dtype,
                )
        else:
            pipe = AnimateDiffPipeline.from_pretrained(
                "Lykon/dreamshaper-8",
                motion_adapter=adapter,
                torch_dtype=dtype,
            )
        pipe.scheduler = DDIMScheduler.from_config(
            pipe.scheduler.config,
            beta_schedule="linear",
            clip_sample=False,
            timestep_spacing="linspace",
            steps_offset=1,
        )
        if device == "cuda":
            pipe.enable_model_cpu_offload()
        pipeline = pipe
        print("[ASTRA VIDEO] Pipeline ready!")
    except Exception as e:
        print(f"[ASTRA VIDEO] Failed to load pipeline: {e}")
    finally:
        pipeline_loading = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context: kick off model loading in background thread on startup."""
    import threading
    threading.Thread(target=load_pipeline, daemon=True).start()
    yield  # server runs while yielded


app = FastAPI(title="ASTRA Video Server", version="1.0.0", lifespan=lifespan)


# ─── Request Model ────────────────────────────────────────────────────────────

class VideoRequest(BaseModel):
    prompt: str
    negative_prompt: str = "blurry, bad quality, distorted, watermark, text, ugly"
    frames: int = 10        # Fast animation rendering
    fps: int = 8
    steps: int = 12         # Fast DDIM / DPMSolver 12 steps
    guidance: float = 7.0
    width: int = 512
    height: int = 512
    seed: Optional[int] = None


# ─── Background Job ───────────────────────────────────────────────────────────

def run_generation(job_id: str, req: VideoRequest):
    global pipeline
    jobs[job_id]["status"] = "generating"
    jobs[job_id]["progress"] = "Loading model into GPU..."

    try:
        import torch
        from diffusers.utils import export_to_gif

        if pipeline is None:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = "Pipeline not loaded yet. Please wait a moment and retry."
            return

        with torch.inference_mode():
            generator = None
            if req.seed is not None:
                generator = torch.Generator().manual_seed(req.seed)

            jobs[job_id]["progress"] = "Generating frames..."

        result = pipeline(
            prompt=req.prompt,
            negative_prompt=req.negative_prompt,
            num_frames=req.frames,
            num_inference_steps=req.steps,
            guidance_scale=req.guidance,
            width=req.width,
            height=req.height,
            generator=generator,
        )

        jobs[job_id]["progress"] = "Exporting video..."

        frames = result.frames[0]
        filename = f"astra_{job_id[:8]}.gif"
        out_path = os.path.join(OUTPUT_DIR, filename)
        export_to_gif(frames, out_path, fps=req.fps)

        jobs[job_id]["status"] = "done"
        jobs[job_id]["filename"] = filename
        jobs[job_id]["progress"] = "Complete!"
        print(f"[ASTRA VIDEO] Done: {filename}")

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        print(f"[ASTRA VIDEO] Error in job {job_id}: {e}")


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/generate")
async def generate(req: VideoRequest, background: BackgroundTasks):
    if pipeline_loading:
        raise HTTPException(status_code=503, detail="Pipeline is still loading. Please wait a moment.")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "queued",
        "filename": None,
        "error": None,
        "progress": "Queued...",
        "prompt": req.prompt,
        "created": time.time(),
    }
    background.add_task(run_generation, job_id, req)
    return {"job_id": job_id, "status": "queued"}


@app.get("/status/{job_id}")
async def status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found.")
    return jobs[job_id]


@app.get("/download/{filename}")
async def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path, media_type="image/gif", filename=filename)


@app.get("/health")
async def health():
    return {
        "status": "online",
        "pipeline": "ready" if pipeline else ("loading" if pipeline_loading else "not loaded"),
        "jobs": len(jobs),
    }


@app.get("/web", response_class=HTMLResponse)
async def web_ui():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASTRA Video Generator</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050810;color:#e0e6f0;font-family:'Outfit',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(167,139,250,0.2);border-radius:20px;padding:2.5rem;width:100%;max-width:720px;backdrop-filter:blur(20px);box-shadow:0 0 60px rgba(120,80,255,0.08)}
h1{font-size:2rem;font-weight:700;color:#a78bfa;text-align:center;margin-bottom:.3rem}
.sub{text-align:center;color:#7a8ba0;font-size:.9rem;margin-bottom:2rem}
label{display:block;font-size:.75rem;color:#7a8ba0;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.4rem}
input,textarea,select{width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(167,139,250,0.2);border-radius:12px;color:#e0e6f0;font-family:'Outfit',sans-serif;font-size:1rem;padding:.8rem 1rem;outline:none;transition:border-color .2s;margin-bottom:1.2rem}
textarea{height:100px;resize:vertical}
input:focus,textarea:focus{border-color:#a78bfa}
.row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem}
.btn{width:100%;padding:.9rem;background:linear-gradient(135deg,#a78bfa,#ec4899);border:none;border-radius:12px;color:#fff;font-family:'Outfit',sans-serif;font-size:1rem;font-weight:700;cursor:pointer;transition:opacity .2s,transform .1s;margin-top:.5rem}
.btn:hover{opacity:.9;transform:translateY(-1px)}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none}
.status-box{background:rgba(255,255,255,0.04);border:1px solid rgba(167,139,250,0.15);border-radius:12px;padding:1rem;margin-top:1.2rem;display:none;text-align:center}
.status-box img{max-width:100%;border-radius:12px;margin-top:1rem}
.badge{display:inline-block;background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.3);color:#a78bfa;padding:.2rem .7rem;border-radius:999px;font-size:.75rem}
.warn{color:#f59e0b;font-size:.8rem;text-align:center;margin-bottom:1.2rem}
</style>
</head>
<body>
<div class="card">
  <h1>🎬 ASTRA Video Generator</h1>
  <p class="sub">Text-to-Video powered by AnimateDiff + DreamShaper 8</p>
  <p class="warn">⚠️ Generation takes 2–5 minutes on 4GB VRAM. Be patient!</p>

  <label>Prompt</label>
  <textarea id="prompt" placeholder="A futuristic city at night, neon lights, rain, cinematic, 4k..."></textarea>

  <label>Negative Prompt</label>
  <textarea id="neg" style="height:60px" placeholder="blurry, watermark, bad quality...">blurry, bad quality, distorted, watermark, text, ugly, worst quality</textarea>

  <div class="row">
    <div><label>Frames</label><input id="frames" type="number" value="16" min="8" max="24"></div>
    <div><label>FPS</label><input id="fps" type="number" value="8" min="4" max="16"></div>
    <div><label>Steps</label><input id="steps" type="number" value="20" min="10" max="30"></div>
  </div>

  <button class="btn" id="btn" onclick="generate()">🎬 Generate Video</button>

  <div class="status-box" id="statusBox">
    <p id="statusText">Processing...</p>
    <img id="result" style="display:none">
    <a id="dlLink" style="display:none;margin-top:.8rem;display:none;color:#a78bfa">⬇ Download GIF</a>
  </div>
</div>
<script>
let pollInterval = null;
async function generate(){
  const btn=document.getElementById('btn');
  const prompt=document.getElementById('prompt').value.trim();
  if(!prompt){alert('Enter a prompt!');return;}
  btn.disabled=true; btn.textContent='⏳ Submitting...';
  document.getElementById('statusBox').style.display='block';
  document.getElementById('statusText').textContent='Queued — waiting for GPU...';
  document.getElementById('result').style.display='none';
  document.getElementById('dlLink').style.display='none';
  try{
    const r=await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({prompt,negative_prompt:document.getElementById('neg').value,
        frames:parseInt(document.getElementById('frames').value),
        fps:parseInt(document.getElementById('fps').value),
        steps:parseInt(document.getElementById('steps').value)})});
    const {job_id}=await r.json();
    btn.textContent='⏳ Generating...';
    pollInterval=setInterval(()=>poll(job_id,btn),4000);
  }catch(e){alert('Error: '+e.message);btn.disabled=false;btn.textContent='🎬 Generate Video';}
}
async function poll(job_id,btn){
  try{
    const r=await fetch('/status/'+job_id);
    const d=await r.json();
    document.getElementById('statusText').textContent=d.progress||d.status;
    if(d.status==='done'){
      clearInterval(pollInterval);
      const img=document.getElementById('result');
      img.src='/download/'+d.filename+'?t='+Date.now();
      img.style.display='block';
      const dl=document.getElementById('dlLink');
      dl.href='/download/'+d.filename;
      dl.download=d.filename;
      dl.style.display='inline-block';
      btn.disabled=false; btn.textContent='🎬 Generate Video';
    } else if(d.status==='error'){
      clearInterval(pollInterval);
      document.getElementById('statusText').textContent='❌ Error: '+d.error;
      btn.disabled=false; btn.textContent='🎬 Generate Video';
    }
  }catch(e){console.error(e);}
}
</script>
</body></html>"""


if __name__ == "__main__":
    import uvicorn
    print("[ASTRA VIDEO] Starting on port 8891...")
    uvicorn.run(app, host="0.0.0.0", port=8891, log_level="warning")
