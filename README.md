# 🚀 ASTRA AI Ecosystem

ASTRA is an all-in-one local AI ecosystem powered completely by **Open WebUI**, **ComfyUI**, and **Ollama**.
Everything runs 100% locally on your machine with absolutely zero cloud dependency.

## ✨ Interfaces:
- 💬 **Open WebUI Chat (Port 8080)**: Centralized chat interface for interacting with LLM agents, generating images, videos, voice, and documents.
- ⚙️ **ComfyUI Visual Engine (Port 8188)**: Node-based creative pipeline with native ASTRA custom nodes for high-quality Image & Video generation.

## 🎨 Generation Capabilities:
- 🎨 **Image Generation**: Powered by Stable Diffusion (DreamShaper 8) via ComfyUI & Open WebUI Chat.
- 🎬 **Video Generation**: Powered by AnimateDiff + DreamShaper 8 via ComfyUI & Open WebUI Chat.
- 🎙️ **Voice Generator**: High-quality local Text-to-Speech standalone engine.
- 📄 **PDF Generator**: Styled PDF document compiler.

---

## 🛠️ How to Launch ASTRA

Double-click `Start-ASTRA.bat`.
This script will boot up all necessary background components and open both interfaces in your browser:
1. **Open WebUI Chat**: `http://localhost:8080`
2. **ComfyUI Engine**: `http://localhost:8188`

---

## 🧠 Importing & Customizing the ASTRA Model

You can easily build, import, or switch the ASTRA AI model using the interactive importer:

1. Double-click `Import-ASTRA-Model.bat`.
2. Choose your base model:
   - **Option [1]**: **Llama 3.2** *(Recommended — Fast, lightweight 3B with 4096 context)*
   - **Option [2]**: **Mistral 7B** *(High reasoning power, already local)*
   - **Option [3]**: **Custom Base Model** *(e.g. `deepseek-r1:7b`, `llama3.1`, `qwen2.5`)*
   - **Option [4]**: **Local GGUF Model** *(Import any downloaded `.gguf` file)*
3. Or manually build directly in the terminal:
   ```bash
   ollama create astra -f Modelfile
   ```

---

## 💡 Using Image & Video Generation in Open WebUI Chat
1. Open `http://localhost:8080` in your browser.
2. **Generate Image**: Ask the AI: *"Generate an image of a futuristic city with neon lights"*. The image will render directly inside your chat.
3. **Generate Video**: Ask the AI: *"Generate a video of rain falling over a cyberpunk street"*. The animated clip will display inline.
4. **ComfyUI Workflows**: Open `http://localhost:8188` to build visual pipelines using `ASTRA 🎨 Image Generator` and `ASTRA 🎬 Video Generator` nodes.

Enjoy your local AI creator ecosystem!

