# 🚀 ASTRA AI Ecosystem
> **Unified Autonomous Local AI Creator** — Powered by Open WebUI, ComfyUI, Ollama, PyTorch & FastAPI.
> 100% Local. Zero Cloud Dependency. Zero Subscription Fees.

---

## ✨ System Architecture & Microservices

ASTRA operates as a high-performance local microservices ecosystem managed by a background supervisor daemon (`astra_supervisor.py`).

| Service Component | Port | Backend Engine | Capabilities |
| :--- | :---: | :--- | :--- |
| **Open WebUI Chat** | `8080` | WebUI Engine + Pipe API | Centralized Chat, In-Chat Video/Image/Audio/PDF Rendering |
| **ComfyUI Visual Engine** | `8188` | ComfyUI + Custom ASTRA Nodes | Node-Based Creative Pipelines & Workflow Editor |
| **Image Engine** | `8892` | Stable Diffusion 1.5 (DreamShaper 8) | Text-to-Image Generation (4GB VRAM FP16 Optimized) |
| **Video Engine** | `8891` | AnimateDiff + SD 1.5 | Text-to-Video Animation & GIF Rendering |
| **Voice Engine** | `8880` | Kokoro TTS | High-Quality Text-to-Speech (Multiple Voices) |
| **Whisper STT Engine** | `8885` | OpenAI Whisper | Local Voice-to-Text Transcription |
| **PDF Engine** | `8890` | FPDF2 Compiler | Styled PDF Document Generation |

---

## 🎨 Core Features & Capabilities

- 💬 **In-Chat Media Rendering**: Generate images, videos, audio, and documents inline directly inside your Open WebUI chat conversation without switching apps.
- 🎨 **Stable Diffusion Image Studio**: High-res image generation with dynamic DPMSolverMultistepScheduler and Karras sigmas.
- 🎬 **AnimateDiff Video Renderer**: Generate fluid animated clips directly from natural language prompts.
- 🎙️ **Kokoro Text-to-Speech**: Crystal-clear speech synthesis with configurable voice profiles (`af_bella`, `af_sky`, `am_adam`).
- 🧠 **Autonomous Model Importer**: Seamlessly switch or import GGUF / Ollama models (`Llama 3.2`, `Mistral 7B`, `DeepSeek-R1`, `Qwen 2.5`).
- 🧩 **Native ComfyUI Custom Nodes**: Build node graphs using custom `ASTRA_Suite` nodes (`AstraBrain`, `AstraVideo`, `AstraVoice`, `AstraPDF`, `AstraWebSearch`).

---

## 🛠️ Quickstart Guide

### 1. Launch Everything in One Click
Double-click `Start-ASTRA.bat` or run in PowerShell:
```powershell
.\run_astra.ps1
```
This script automatically starts all background microservices, checks health ports, and opens your browser:
- **Open WebUI Chat**: `http://localhost:8080`
- **ComfyUI Engine**: `http://localhost:8188`

### 2. Import / Switch AI Models
Double-click `Import-ASTRA-Model.bat` or run:
```bash
ollama create astra -f Modelfile
```

### 3. In-Chat Usage Examples
Open `http://localhost:8080` and try prompting:
- **Generate Image**: *"Generate an image of a futuristic cyberpunk city lit by neon lights"*
- **Generate Video**: *"Generate a video of rain falling on a rainy neon street"*
- **Voice Synthesis**: *"Speak: Welcome to the ASTRA AI local ecosystem"*

---

## 🏗️ Technical Obstacles & Architectural Solutions

### 1. VRAM & Hardware Optimization (4GB VRAM Capable)
* **Challenge:** Running LLMs, Stable Diffusion, AnimateDiff, TTS, and STT simultaneously caused GPU Out-Of-Memory (OOM) errors.
* **Solution:** Applied standard FP16 (`torch.float16`) precision, dynamic CPU offloading, model weight recycling, and on-demand microservice loading to keep VRAM footprint under 4GB during inference.

### 2. Microservice Orchestration Daemon
* **Challenge:** Managing 7 independent Python servers across dual virtual environments (`comfy_env` and `webui_env`) created process collisions and encoding issues.
* **Solution:** Engineered `astra_supervisor.py`, a background process manager that continuously monitors ports, auto-restarts crashed services, and enforces UTF-8 encoding.

### 3. Open WebUI Pipe Integration & Database Sync
* **Challenge:** Open WebUI is natively text-focused and does not support real-time inline video/audio streaming or dynamic tool triggers by default.
* **Solution:** Created a custom Pipe Function (`create_astra_pipe.py`) and SQLite database sync script (`sync_webui_db.py`) that captures prompt intents and renders base64 images and HTML video cards directly in chat streams.

---

## 📄 License & Credits
- **License**: [MIT License](LICENSE)
- **Author**: PANIMANIKANTA
- Built with **Open WebUI**, **ComfyUI**, **Ollama**, **PyTorch**, **Diffusers**, **FastAPI**, and **Kokoro TTS**.
