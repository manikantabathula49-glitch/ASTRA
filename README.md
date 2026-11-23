# 🚀 ASTRA AI Ecosystem
> **Unified Autonomous Local AI Creator** — Powered by Open WebUI, ComfyUI, Ollama, PyTorch & FastAPI.
> 100% Local. Zero Cloud Dependency. Zero Subscription Fees.

---

## ✨ System Architecture & Microservices

ASTRA operates as a high-performance local microservices ecosystem managed by a background supervisor daemon (`astra_supervisor.py`).

| Service Component | Port | Backend Engine | Capabilities |
| :--- | :---: | :--- | :--- |
| **Open WebUI Chat** | `8080` | WebUI Engine + Pipe API | Centralized Chat, In-Chat Image/Audio/PDF Rendering |
| **ComfyUI Visual Engine** | `8188` | ComfyUI + Custom ASTRA Nodes | Node-Based Creative Pipelines & Workflow Editor |
| **Image Engine** | `8892` | Stable Diffusion 1.5 (DreamShaper 8) | Text-to-Image Generation (4GB VRAM FP16 Optimized) |
| **PDF Engine** | `8890` | FPDF2 Compiler | Styled PDF Document Generation & Web Downloads |
| **Voice Engine** | `8880` | Kokoro TTS | High-Quality Text-to-Speech (Multiple Voices) |
| **Whisper STT Engine** | `8885` | OpenAI Whisper | Local Voice-to-Text Transcription |

---

## 🎨 Core Features & Capabilities

- 💬 **In-Chat Media Rendering**: Generate images, audio, and documents inline directly inside your Open WebUI chat conversation without switching apps.
- 📄 **Styled PDF Document Compiler**: Generate and download publication-ready PDF documents formatted with customizable templates directly in chat.
- 🎨 **Stable Diffusion Image Studio**: High-res image generation with dynamic DPMSolverMultistepScheduler and Karras sigmas.
- 🎙️ **Kokoro Text-to-Speech**: Crystal-clear speech synthesis with configurable voice profiles (`af_bella`, `af_sky`, `am_adam`).
- 🧠 **Autonomous Model Importer**: Seamlessly switch or import GGUF / Ollama models (`Llama 3.2`, `Mistral 7B`, `DeepSeek-R1`, `Qwen 2.5`).
- 🧩 **Native ComfyUI Custom Nodes**: Build node graphs using custom `ASTRA_Suite` nodes (`AstraBrain`, `AstraVoice`, `AstraPDF`, `AstraWebSearch`).

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
Double-click `scripts\Import-ASTRA-Model.bat` or run:
```bash
ollama create astra -f Modelfile
```

### 3. In-Chat Usage Examples
Open `http://localhost:8080` and try prompting:
- **Generate Image**: *"Generate an image of a futuristic cyberpunk city lit by neon lights"*
- **Generate PDF**: *"Generate a PDF report on the Architecture of Local Multi-Agent AI Systems"*
- **Voice Synthesis**: *"Speak: Welcome to the ASTRA AI local ecosystem"*

---

## 📁 Repository Structure

```text
ASTRA\                             # (any folder/drive — paths are resolved automatically)
├── Start-ASTRA.bat                  # Primary 1-click startup launcher
├── run_astra.ps1                    # PowerShell startup script
├── Modelfile                        # Root Ollama model configuration
├── README.md                        # Project documentation
│
├── services\                        # 🚀 Backend FastAPI Microservices
│   ├── image_server.py              # DreamShaper 8 Stable Diffusion (Port 8892)
│   ├── pdf_server.py                # FPDF2 Document Compiler (Port 8890)
│   ├── voice_server.py              # Kokoro TTS Engine (Port 8880)
│   ├── whisper_server.py            # Whisper STT Transcription (Port 8885)
│   └── run_webui.py                 # Open WebUI Server Runner (Port 8080)
│
├── core\                            # ⚙️ Orchestration, Supervisor & DB
│   ├── astra_supervisor.py          # Background process manager & auto-restart daemon
│   ├── launch_all.py                # Universal background launcher
│   └── sync_webui_db.py             # Open WebUI DB syncer & pipeline config
│
├── tools\                           # 🧩 WebUI & Chat Integrations
│   ├── astra_webui_tool.py          # Open WebUI In-Chat Tool definition
│   └── create_astra_pipe.py         # Open WebUI Pipe Function registration
│
├── workflows\                       # 🎨 ComfyUI & AI Pipelines
│   ├── ASTRA_Master_Workflow.json   # ComfyUI Master Creative Workflow
│   ├── create_workflow.py           # ComfyUI Workflow Generator
│   └── download_model.py            # HuggingFace Model Downloader
│
├── scripts\                         # 🛠️ Setup & Maintenance Batch Files
│   ├── Import-ASTRA-Model.bat       # Ollama model build/import
│   ├── Install-ASTRA-Nodes.bat      # ComfyUI custom nodes installer
│   ├── Install-PDF.bat              # PDF engine virtualenv installer
│   └── Install-Voice.bat            # Voice engine virtualenv installer
│
├── tests\                           # 🧪 Diagnostics & Health Tests
│   ├── test_all_services.py         # Multi-service health & port check
│   ├── test_image_gen.py            # Image generation validation
│   ├── test_pipe.py                 # Open WebUI Pipe validation
│   ├── test_runner.py               # Process runner diagnostic
│   ├── test_pdf_offline.py          # Offline PDF engine regression tests (no services needed)
│   └── inspect_astra.py             # SQLite DB inspector
│
└── deployment\                      # ☁️ Docker & Cloud Configurations
    ├── Dockerfile                   # Render / Docker container specification
    ├── render.yaml                  # Render cloud blueprint
    └── render_entrypoint.sh         # Linux container boot script
```

---

## 🏗️ Technical Obstacles & Architectural Solutions

### 1. VRAM & Hardware Optimization (4GB VRAM Capable)
* **Challenge:** Running LLMs, Stable Diffusion, TTS, and STT simultaneously caused GPU Out-Of-Memory (OOM) errors.
* **Solution:** Applied standard FP16 (`torch.float16`) precision, dynamic CPU offloading, model weight recycling, and on-demand microservice loading to keep VRAM footprint under 4GB during inference.

### 2. Microservice Orchestration Daemon
* **Challenge:** Managing independent Python servers across dual virtual environments (`comfy_env` and `webui_env`) created process collisions and encoding issues.
* **Solution:** Engineered `core/astra_supervisor.py`, a background process manager that continuously monitors ports, auto-restarts crashed services, and enforces UTF-8 encoding.

### 3. Open WebUI Pipe Integration & Database Sync
* **Challenge:** Open WebUI is natively text-focused and does not support real-time inline document/audio rendering or dynamic tool triggers by default.
* **Solution:** Created a custom Pipe Function (`tools/create_astra_pipe.py`) and SQLite database sync script (`core/sync_webui_db.py`) that captures prompt intents and renders base64 images and PDF download cards directly in chat streams.

---

### 4. Portable Paths & Security
* **Run from any folder/drive:** scripts locate the project from their own location (override with the `ASTRA_HOME` env var). `DATA_DIR` is honoured when locating `webui.db`.
* **Per-install secret key:** `WEBUI_SECRET_KEY` is no longer hardcoded. If it isn't set, a random key is generated once and saved to `<DATA_DIR>/.webui_secret_key`.
* **Safe downloads:** the Image and PDF `/download/{filename}` endpoints reject path-traversal filenames.

---

## 📄 License & Credits
- **License**: [MIT License](LICENSE)
- **Author**: PANIMANIKANTA
- Built with **Open WebUI**, **ComfyUI**, **Ollama**, **PyTorch**, **Diffusers**, **FastAPI**, and **Kokoro TTS**.
