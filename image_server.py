#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASTRA Image Generation Server
Text-to-Image using Stable Diffusion 1.5 (DreamShaper 8)
Port: 8892
Optimized for 4GB VRAM (float16 + CPU offload) with CPU fallback.
Provides:
  - Native ASTRA API (/generate, /status/{id}, /download/{filename}, /web)
  - OpenAI-compatible Image API (/v1/images/generations, /v1/models)
  - Automatic1111-compatible API (/sdapi/v1/txt2img, /sdapi/v1/options, /sdapi/v1/sd-models)
"""

import os
import io
import uuid
import asyncio
import time
import base64
import logging
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

logging.basicConfig(
    level=logging.INFO,
    format="[ASTRA IMAGE] %(asctime)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ASTRA-Image")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "image_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global pipeline — loaded once on first use or on startup
pipeline = None
pipeline_loading = False
pipeline_error = None
jobs: Dict[str, Dict[str, Any]] = {}   # job_id → {"status", "filename", "error", "progress", ...}


# ─── Pipeline Loader ─────────────────────────────────────────────────────────

def load_pipeline():
    global pipeline, pipeline_loading, pipeline_error
    if pipeline is not None:
        return pipeline
    pipeline_loading = True
    pipeline_error = None
    logger.info("Loading DreamShaper 8 pipeline (this may take a moment)...")
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32

        logger.info(f"Using device: {device} ({dtype})")
        pipe = StableDiffusionPipeline.from_pretrained(
            "Lykon/dreamshaper-8",
            torch_dtype=dtype,
            safety_checker=None,
        )

        # Optimize scheduler for faster & higher quality results
        try:
            # pyrefly: ignore [missing-attribute]
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                # pyrefly: ignore [missing-attribute]
                pipe.scheduler.config,
                use_karras_sigmas=True,
                final_sigmas_type="sigma_min",
            )
        except Exception:
            pass

        if device == "cuda":
            torch.backends.cudnn.benchmark = True
            torch.backends.cuda.matmul.allow_tf32 = True
            # pyrefly: ignore [missing-attribute]
            pipe.to("cuda")
            try:
                pipe.unet.to(memory_format=torch.channels_last)
            except Exception:
                pass
        else:
            # pyrefly: ignore [missing-attribute]
            pipe.to("cpu")

        pipeline = pipe
        logger.info("ASTRA Image Pipeline ready!")
        return pipeline
    except Exception as e:
        pipeline_error = str(e)
        logger.error(f"Failed to load image pipeline: {e}")
        return None
    finally:
        pipeline_loading = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context: load pipeline in background on startup."""
    import threading
    threading.Thread(target=load_pipeline, daemon=True).start()
    yield
    logger.info("ASTRA Image Server shut down.")


app = FastAPI(title="ASTRA Image Server", version="2.0.0", lifespan=lifespan)

# Enable CORS for Open WebUI and local web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Claude Visual Prompt Enhancement Engine ──────────────────────────────────

class ClaudePromptEnhancer:
    @staticmethod
    def enhance(prompt: str, ollama_url: str = "http://127.0.0.1:11434") -> str:
        """
        Enhances a user prompt using Claude visual prompt engineering principles.
        """
        clean_p = prompt.strip()
        if not clean_p:
            return prompt

        # Fast Rule-Based Visual Expander
        lower = clean_p.lower()
        modifiers = []
        
        if not any(k in lower for k in ["lighting", "light", "sunlight", "glow", "neon", "ray"]):
            if any(k in lower for k in ["cyberpunk", "sci-fi", "futuristic"]):
                modifiers.append("vibrant magenta and cyan neon luminescence, dark rain-slick reflections")
            elif any(k in lower for k in ["portrait", "face", "person", "character"]):
                modifiers.append("soft studio key lighting, warm golden hour rim light, realistic catchlights")
            elif any(k in lower for k in ["landscape", "nature", "mountain", "forest"]):
                modifiers.append("dramatic crepuscular sun rays breaking through mist, atmospheric golden glow")
            else:
                modifiers.append("cinematic volumetric lighting, subtle rim lighting, dramatic chiaroscuro atmosphere")

        if not any(k in lower for k in ["style", "art", "render", "photo", "realistic", "painting"]):
            if any(k in lower for k in ["anime", "manga", "comic"]):
                modifiers.append("masterpiece anime key visual, highly detailed line art, dynamic framing")
            elif any(k in lower for k in ["painting", "oil", "watercolor", "canvas"]):
                modifiers.append("masterpiece fine art painting, visible brushstrokes, rich chromatic depth")
            else:
                modifiers.append("8k resolution, hyper-detailed photorealistic digital art, sharp focus, Unreal Engine 5 render")

        if not any(k in lower for k in ["camera", "lens", "mm", "shot", "view"]):
            if any(k in lower for k in ["portrait", "face", "close"]):
                modifiers.append("shot on 85mm f/1.4 lens, shallow depth of field, natural bokeh")
            elif any(k in lower for k in ["landscape", "city", "space", "panorama"]):
                modifiers.append("wide-angle 24mm lens shot, epic scale, crisp geometric precision")
            else:
                modifiers.append("cinematic 35mm composition, professional color grading, octane render depth")

        extra_spec = ", ".join(modifiers)
        return f"{clean_p}, {extra_spec}"


# ─── Request Models ───────────────────────────────────────────────────────────

class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = "blurry, bad quality, distorted, watermark, text, ugly, low quality, duplicate"
    steps: int = 15
    guidance: float = 7.0
    width: int = 512
    height: int = 512
    seed: Optional[int] = None
    enhance_with_claude: bool = True


class EnhancePromptRequest(BaseModel):
    prompt: str


class OpenAIImageGenerationRequest(BaseModel):
    prompt: str
    model: Optional[str] = "dreamshaper-8"
    n: Optional[int] = 1
    quality: Optional[str] = "standard"
    response_format: Optional[str] = "b64_json"  # "url" or "b64_json"
    size: Optional[str] = "512x512"
    style: Optional[str] = "vivid"
    user: Optional[str] = None


class A1111Txt2ImgRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = "blurry, bad quality, distorted, watermark, text, ugly, low quality, duplicate"
    steps: Optional[int] = 15
    cfg_scale: Optional[float] = 7.0
    width: Optional[int] = 512
    height: Optional[int] = 512
    batch_size: Optional[int] = 1
    n_iter: Optional[int] = 1
    seed: Optional[int] = -1


# ─── Inference Helper ─────────────────────────────────────────────────────────

@torch.inference_mode()
def generate_image_sync(prompt: str, negative_prompt: str = "", steps: int = 15, guidance: float = 7.0, width: int = 512, height: int = 512, seed: Optional[int] = None):
    global pipeline
    if pipeline is None:
        pipe = load_pipeline()
        if pipe is None:
            raise RuntimeError(f"Pipeline unavailable: {pipeline_error or 'Unknown error'}")
    else:
        pipe = pipeline

    import torch
    generator = None
    if seed is not None and seed != -1:
        generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(seed)

    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        guidance_scale=guidance,
        width=width,
        height=height,
        generator=generator,
    )
    return result.images[0]


# ─── Background Job ───────────────────────────────────────────────────────────

def run_generation(job_id: str, req: ImageRequest):
    jobs[job_id]["status"] = "generating"
    
    # Process Claude Prompt Enhancement if enabled
    original_prompt = req.prompt
    final_prompt = req.prompt
    if req.enhance_with_claude:
        jobs[job_id]["progress"] = "✨ Enhancing prompt with Claude Skill..."
        final_prompt = ClaudePromptEnhancer.enhance(original_prompt)
        jobs[job_id]["enhanced_prompt"] = final_prompt
        logger.info(f"Claude Skill Enhanced Prompt: '{original_prompt}' -> '{final_prompt}'")
    else:
        jobs[job_id]["enhanced_prompt"] = original_prompt

    jobs[job_id]["progress"] = "Running inference with DreamShaper 8..."

    try:
        image = generate_image_sync(
            prompt=final_prompt,
            negative_prompt=req.negative_prompt,
            steps=req.steps,
            guidance=req.guidance,
            width=req.width,
            height=req.height,
            seed=req.seed,
        )

        jobs[job_id]["progress"] = "Saving image..."
        filename = f"astra_{job_id[:8]}.png"
        out_path = os.path.join(OUTPUT_DIR, filename)
        image.save(out_path, format="PNG")

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        jobs[job_id]["status"] = "done"
        jobs[job_id]["filename"] = filename
        jobs[job_id]["b64_data"] = b64_str
        jobs[job_id]["original_prompt"] = original_prompt
        jobs[job_id]["final_prompt"] = final_prompt
        jobs[job_id]["progress"] = "Complete!"
        logger.info(f"Done job {job_id[:8]}: {filename}")

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        logger.error(f"Error in job {job_id}: {e}")


# ─── Core Routes ──────────────────────────────────────────────────────────────

@app.post("/generate")
async def generate(req: ImageRequest, background: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "queued",
        "filename": None,
        "b64_data": None,
        "error": None,
        "progress": "Queued...",
        "prompt": req.prompt,
        "enhanced_prompt": None,
        "created": time.time(),
    }
    background.add_task(run_generation, job_id, req)
    return {"job_id": job_id, "status": "queued"}


@app.post("/enhance-prompt")
async def enhance_prompt(req: EnhancePromptRequest):
    enhanced = ClaudePromptEnhancer.enhance(req.prompt)
    return {"original_prompt": req.prompt, "enhanced_prompt": enhanced}



@app.get("/status/{job_id}")
async def status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found.")
    return jobs[job_id]


@app.get("/download/{filename}")
@app.get("/image/{filename}")
async def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(
        path,
        media_type="image/png",
        filename=filename,
        headers={"Cache-Control": "public, max-age=31536000"}
    )


@app.get("/health")
async def health():
    return {
        "status": "online",
        "service": "ASTRA Image Server",
        "pipeline": "ready" if pipeline else ("loading" if pipeline_loading else "error" if pipeline_error else "idle"),
        "error": pipeline_error,
        "jobs": len(jobs),
        "output_dir": OUTPUT_DIR,
    }


# ─── OpenAI-Compatible Image API ──────────────────────────────────────────────

@app.post("/v1/images/generations")
async def openai_images_generations(req: OpenAIImageGenerationRequest, request: Request):
    width, height = 512, 512
    if req.size and "x" in req.size:
        try:
            w, h = req.size.split("x")
            width, height = int(w), int(h)
        except Exception:
            pass

    loop = asyncio.get_running_loop()
    try:
        image = await loop.run_in_executor(
            None,
            generate_image_sync,
            req.prompt,
            "blurry, bad quality, distorted, watermark, text, ugly, low quality",
            25,
            7.5,
            width,
            height,
            None,
        )

        job_id = str(uuid.uuid4())[:8]
        filename = f"astra_{job_id}.png"
        out_path = os.path.join(OUTPUT_DIR, filename)
        image.save(out_path, format="PNG")

        data_items = []
        if req.response_format == "url":
            base_url = str(request.base_url).rstrip("/")
            img_url = f"{base_url}/download/{filename}"
            data_items.append({"url": img_url})
        else:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            data_items.append({"b64_json": b64_str})

        return {
            "created": int(time.time()),
            "data": data_items,
        }
    except Exception as e:
        logger.error(f"OpenAI image generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "dreamshaper-8",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "astra",
            }
        ],
    }


# ─── Automatic1111-Compatible API ─────────────────────────────────────────────

@app.post("/sdapi/v1/txt2img")
async def a1111_txt2img(req: A1111Txt2ImgRequest):
    loop = asyncio.get_running_loop()
    try:
        image = await loop.run_in_executor(
            None,
            generate_image_sync,
            req.prompt,
            req.negative_prompt or "",
            req.steps or 25,
            req.cfg_scale or 7.5,
            req.width or 512,
            req.height or 512,
            req.seed if req.seed != -1 else None,
        )

        job_id = str(uuid.uuid4())[:8]
        filename = f"astra_{job_id}.png"
        out_path = os.path.join(OUTPUT_DIR, filename)
        image.save(out_path, format="PNG")

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "images": [b64_str],
            "parameters": req.model_dump(),
            "info": f'{{"prompt": "{req.prompt}", "steps": {req.steps}}}',
        }
    except Exception as e:
        logger.error(f"A1111 txt2img error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sdapi/v1/options")
async def a1111_options():
    return {
        "sd_model_checkpoint": "dreamshaper-8",
        "sd_checkpoint_hash": "astra_ds8",
    }


@app.get("/sdapi/v1/sd-models")
async def a1111_models():
    return [
        {
            "title": "DreamShaper 8 (Lykon/dreamshaper-8)",
            "model_name": "dreamshaper-8",
            "hash": "astra_ds8",
            "sha256": "astra_ds8",
            "filename": "dreamshaper-8",
            "config": None,
        }
    ]


# ─── Interactive Web UI ───────────────────────────────────────────────────────

@app.get("/web", response_class=HTMLResponse)
async def web_ui():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASTRA Image Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#070913;color:#e2e8f0;font-family:'Outfit',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem}
.card{background:rgba(18,24,38,0.75);border:1px solid rgba(217,70,239,0.25);border-radius:24px;padding:2.5rem;width:100%;max-width:760px;backdrop-filter:blur(24px);box-shadow:0 20px 60px rgba(0,0,0,0.6),0 0 40px rgba(217,70,239,0.12)}
h1{font-size:2.2rem;font-weight:700;background:linear-gradient(135deg,#f472b6,#d946ef,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:.3rem}
.sub{text-align:center;color:#94a3b8;font-size:.95rem;margin-bottom:1.5rem}
label{display:block;font-size:.78rem;color:#a78bfa;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.4rem}
input,textarea,select{width:100%;background:rgba(15,23,42,0.6);border:1px solid rgba(217,70,239,0.25);border-radius:14px;color:#f8fafc;font-family:'Outfit',sans-serif;font-size:1rem;padding:.85rem 1.1rem;outline:none;transition:all .2s ease;margin-bottom:1.2rem}
textarea{height:100px;resize:vertical}
input:focus,textarea:focus{border-color:#d946ef;box-shadow:0 0 15px rgba(217,70,239,0.3)}
.row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem}
.skill-box{background:rgba(217,70,239,0.08);border:1px solid rgba(217,70,239,0.3);border-radius:14px;padding:.9rem 1.2rem;margin-bottom:1.2rem;display:flex;align-items:center;justify-content:space-between}
.skill-box label{margin-bottom:0;color:#f472b6;font-size:.9rem;text-transform:none;letter-spacing:normal;cursor:pointer;display:flex;align-items:center;gap:.6rem}
.toggle{width:22px;height:22px;accent-color:#d946ef;cursor:pointer}
.btn{width:100%;padding:1rem;background:linear-gradient(135deg,#d946ef,#8b5cf6,#6366f1);border:none;border-radius:14px;color:#fff;font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:700;cursor:pointer;transition:all .2s ease;box-shadow:0 8px 25px rgba(217,70,239,0.3);margin-top:.5rem}
.btn:hover{opacity:.95;transform:translateY(-2px);box-shadow:0 12px 30px rgba(217,70,239,0.4)}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none;box-shadow:none}

.status-box{background:rgba(15,23,42,0.7);border:1px solid rgba(217,70,239,0.25);border-radius:18px;padding:1.5rem;margin-top:1.5rem;display:none;text-align:center;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

.prompt-diff{background:rgba(0,0,0,0.3);border:1px solid rgba(139,92,246,0.3);border-radius:12px;padding:1rem;margin:1rem 0;text-align:left;font-size:.88rem;color:#cbd5e1;line-height:1.5}
.prompt-diff span{color:#f472b6;font-weight:600}

.img-container{position:relative;margin-top:1rem;display:inline-block;max-width:100%}
.img-container img{max-width:100%;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.1);display:block}

.action-bar{display:flex;gap:1rem;justify-content:center;margin-top:1.2rem;flex-wrap:wrap}
.action-btn{display:inline-flex;align-items:center;gap:.5rem;padding:.75rem 1.4rem;border-radius:12px;font-size:.95rem;font-weight:600;text-decoration:none;cursor:pointer;transition:all .2s ease;border:none}
.btn-dl{background:linear-gradient(135deg,#10b981,#059669);color:#fff;box-shadow:0 6px 20px rgba(16,185,129,0.25)}
.btn-dl:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(16,185,129,0.4)}
.btn-retry{background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff;box-shadow:0 6px 20px rgba(139,92,246,0.25)}
.btn-retry:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(139,92,246,0.4)}
.warn{color:#a78bfa;font-size:.82rem;text-align:center;margin-bottom:1.2rem}
</style>
</head>
<body>
<div class="card">
  <h1>🎨 ASTRA Image Engine</h1>
  <p class="sub">High-Quality Text-to-Image Generation powered by DreamShaper 8</p>

  <label>Prompt</label>
  <textarea id="prompt" placeholder="Describe your image concept (e.g. 'A futuristic cyberpunk warrior in Tokyo under neon rain')..."></textarea>

  <label>Negative Prompt</label>
  <textarea id="neg" style="height:55px" placeholder="blurry, watermark, bad quality...">blurry, bad quality, distorted, watermark, text, ugly, duplicate, low quality</textarea>

  <div class="row">
    <div><label>Width</label><input id="width" type="number" value="512" min="256" max="768" step="64"></div>
    <div><label>Height</label><input id="height" type="number" value="512" min="256" max="768" step="64"></div>
    <div><label>Steps</label><input id="steps" type="number" value="25" min="10" max="50"></div>
  </div>

  <button class="btn" id="btn" onclick="generate()">🎨 Generate Image</button>

  <div class="status-box" id="statusBox">
    <p id="statusText" style="font-weight:600;font-size:1.05rem;color:#f472b6">Processing...</p>

    <div class="img-container">
      <img id="result" style="display:none">
    </div>

    <div class="action-bar" id="actionBar" style="display:none">
      <a id="dlBtn" class="action-btn btn-dl" download>📥 Download Image (PNG)</a>
      <button id="retryBtn" class="action-btn btn-retry" onclick="retryGenerate()">🔄 Retry Generation</button>
    </div>
  </div>
</div>

<script>
let pollInterval = null;
let currentJobId = null;

async function generate(overrideSeed = null){
  const btn = document.getElementById('btn');
  const prompt = document.getElementById('prompt').value.trim();
  if(!prompt){ alert('Please enter a prompt!'); return; }
  
  btn.disabled = true;
  btn.textContent = '⏳ Submitting...';
  
  const statusBox = document.getElementById('statusBox');
  statusBox.style.display = 'block';
  document.getElementById('statusText').textContent = '✨ Processing image request...';
  document.getElementById('result').style.display = 'none';
  document.getElementById('actionBar').style.display = 'none';

  try {
    const payload = {
      prompt: prompt,
      negative_prompt: document.getElementById('neg').value,
      width: parseInt(document.getElementById('width').value),
      height: parseInt(document.getElementById('height').value),
      steps: parseInt(document.getElementById('steps').value),
      enhance_with_claude: true,
      seed: overrideSeed !== null ? overrideSeed : Math.floor(Math.random() * 1000000)
    };

    const r = await fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    
    const { job_id } = await r.json();
    currentJobId = job_id;
    btn.textContent = '⏳ Generating Image...';
    if(pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(() => poll(job_id, btn), 1500);
  } catch(e) {
    alert('Error submitting generation: ' + e.message);
    btn.disabled = false;
    btn.textContent = '✨ Generate Image';
  }
}

async function poll(job_id, btn){
  try {
    const r = await fetch('/status/' + job_id);
    const d = await r.json();
    document.getElementById('statusText').textContent = d.progress || d.status;

    if (d.status === 'done') {
      clearInterval(pollInterval);
      document.getElementById('statusText').textContent = '🎨 Image Generated Successfully!';
      
      const img = document.getElementById('result');
      img.src = '/download/' + d.filename + '?t=' + Date.now();
      img.style.display = 'block';

      const dlBtn = document.getElementById('dlBtn');
      dlBtn.href = '/download/' + d.filename;
      dlBtn.download = d.filename;

      document.getElementById('actionBar').style.display = 'flex';

      btn.disabled = false;
      btn.textContent = '✨ Generate Image';
    } else if (d.status === 'error') {
      clearInterval(pollInterval);
      document.getElementById('statusText').textContent = '❌ Error: ' + d.error;
      btn.disabled = false;
      btn.textContent = '✨ Generate Image';
    }
  } catch(e) {
    console.error(e);
  }
}

function retryGenerate() {
  const newSeed = Math.floor(Math.random() * 1000000);
  generate(newSeed);
}
</script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ASTRA Image Server on port 8892...")
    uvicorn.run(app, host="0.0.0.0", port=8892, log_level="info")

