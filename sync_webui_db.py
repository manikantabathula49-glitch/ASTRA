import sqlite3
import json
import os
import time

db_path = r"f:\ASTRA\webui_env\Lib\site-packages\open_webui\data\webui.db"
tool_file = r"f:\ASTRA\astra_webui_tool.py"

with open(tool_file, "r", encoding="utf-8") as f:
    tool_content = f.read()

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Prepare tool specs
specs = [
    {
        "name": "generate_image",
        "description": "Generate a beautiful, high-quality image from a descriptive text prompt using local Stable Diffusion (DreamShaper 8).\nCall this whenever the user asks to generate, create, draw, design, or visualize an image or picture.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed visual description of the image to generate."
                }
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "generate_video",
        "description": "Generate an animated video or GIF from a descriptive text prompt using local AnimateDiff + DreamShaper 8.\nCall this when the user asks to generate a video, animation, or moving clip.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed description of the video to create."
                }
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "generate_voice",
        "description": "Convert text into high-quality spoken audio using Kokoro TTS.\nCall this when the user asks to speak text, read something aloud, or synthesize speech.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to convert to speech."
                },
                "voice": {
                    "type": "string",
                    "description": "Voice model ID (default: af_bella, options: af_bella, af_sky, am_adam, am_michael).",
                    "default": "af_bella"
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "generate_pdf",
        "description": "Generate a beautifully styled PDF document from markdown content.\nCall this when the user asks to export to PDF, save a document, compile a report, or format a document.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Document title.",
                    "default": "ASTRA Report"
                },
                "content": {
                    "type": "string",
                    "description": "Markdown content of the document."
                },
                "template": {
                    "type": "string",
                    "description": "Design template (report, technical, resume, notes, proposal).",
                    "default": "report"
                }
            },
            "required": ["content"]
        }
    },
    {
        "name": "check_system_status",
        "description": "Check the real-time operational health of all ASTRA AI ecosystem services and microservers.\nCall this when the user asks for system status, health check, or service diagnostics.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

specs_json = json.dumps(specs)
meta_json = json.dumps({
    "description": "Unified tool for local Image, Video, Voice, and PDF generation.",
    "manifest": {
        "title": "ASTRA Media Engine",
        "author": "PANIMANIKANTA",
        "description": "Unified tool for local Image, Video, Voice, and PDF generation."
    }
})

# 2. Get user_id from user table
user_row = cur.execute("SELECT id FROM user WHERE role='admin' LIMIT 1").fetchone()
admin_id = user_row[0] if user_row else "b0dac253-9aa2-4f71-9186-9cd8c10d386c"

now = int(time.time())

# 3. Update or insert astra_media_engine tool
existing_tool = cur.execute("SELECT id FROM tool WHERE id='astra_media_engine'").fetchone()
if existing_tool:
    cur.execute("""
        UPDATE tool
        SET name='ASTRA Media Engine',
            content=?,
            specs=?,
            meta=?,
            updated_at=?
        WHERE id='astra_media_engine'
    """, (tool_content, specs_json, meta_json, now))
    print("Updated tool 'astra_media_engine' in webui.db.")
else:
    cur.execute("""
        INSERT INTO tool (id, user_id, name, content, specs, meta, created_at, updated_at, valves)
        VALUES ('astra_media_engine', ?, 'ASTRA Media Engine', ?, ?, ?, ?, ?, 'null')
    """, (admin_id, tool_content, specs_json, meta_json, now, now))
    print("Inserted tool 'astra_media_engine' into webui.db.")

# 4. Update or insert 'astra' model (Optimized for Instant Response & GPU Acceleration)
model_meta = {
    "profile_image_url": "/static/favicon.png",
    "description": "Ultra-fast local ASTRA AI Ecosystem with native chat, image generation, video animation, voice synthesis, and document compilation.",
    "capabilities": {
        "file_context": True,
        "vision": True,
        "file_upload": True,
        "web_search": False,
        "image_generation": True,
        "code_interpreter": False,
        "terminal": False,
        "citations": False,
        "status_updates": True,
        "usage": False,
        "builtin_tools": True
    },
    "suggestion_prompts": [
        {"title": ["🎨 Generate Image", "Futuristic City"], "content": "Generate a futuristic cyberpunk city with vibrant violet neon lights"},
        {"title": ["🎬 Generate Video", "Sunset Ocean Beach"], "content": "Generate a video of waves gently crashing on a sunset beach"},
        {"title": ["🎙️ Synthesize Voice", "Local Text-to-Speech"], "content": "Speak this message: Welcome to ASTRA, your local AI creator ecosystem."},
        {"title": ["📄 Create PDF Report", "Document Compiler"], "content": "Generate a PDF report on the Architecture of Local Multi-Agent AI Systems"},
        {"title": ["⚡ Check Status", "System Diagnostics"], "content": "Check the status of all ASTRA system services"}
    ],
    "tags": ["astra", "gpu", "fast", "media-engine"],
    "toolIds": ["astra_media_engine"],
    "defaultFeatureIds": []  # Empty by default to eliminate redundant pre-inference planning latency
}

system_prompt = (
    "You are ASTRA, a state-of-the-art AI assistant, developer, and creator engineered by PANIMANIKANTA.\n\n"
    "Core Capabilities:\n"
    "You have BUILT-IN, fully active local tools for generating multimedia content:\n"
    "1. Video Generation: You can generate videos and animated clips using the local AnimateDiff engine (`generate_video`).\n"
    "2. Image Generation: You can generate high-resolution images using the local Stable Diffusion DreamShaper engine (`generate_image`).\n"
    "3. Voice Synthesis: You can convert text to speech using the local Kokoro TTS engine (`generate_voice`).\n"
    "4. PDF Generation: You can compile styled documents to PDF (`generate_pdf`).\n\n"
    "CRITICAL RULES:\n"
    "- When a user asks you to generate, create, make, or design a video, animation, image, drawing, voice audio, or PDF document:\n"
    "  ALWAYS invoke the appropriate tool (`generate_video`, `generate_image`, `generate_voice`, `generate_pdf`) or execute the generation immediately.\n"
    "- NEVER say \"I don't have the capability to generate videos/images/audio\" or \"As an AI language model, I cannot create videos\". You DO have these capabilities integrated.\n"
    "- NEVER suggest third-party video editors like Premiere Pro, Final Cut, or Python OpenCV scripts when the user asks you to generate a video.\n"
    "- DISPLAYING MEDIA (CRITICAL): When an image or media generation tool returns results, ALWAYS display the generated media directly to the user.\n"
    "  NEVER enclose markdown image tags (![...](...)), HTML <img> tags, or download links inside code blocks or triple backticks (```).\n"
    "  Always output the raw markdown and HTML directly in your text so the user's browser renders the visual image immediately.\n"
    "- Fast & Concise: Deliver clear, concise, and structured answers immediately.\n"
    "- Identity: Maintain a confident, smart, futuristic, and helpful engineering tone."
)

model_params = {
    "system": system_prompt,
    "temperature": 0.6,
    "top_p": 0.9,
    "num_ctx": 2048,
    "num_predict": 256,
    "num_batch": 512,
    "num_gpu": 99,
    "num_thread": 8,
    "repeat_penalty": 1.1,
    "keep_alive": -1,
    "stream": True
}

existing_model = cur.execute("SELECT id FROM model WHERE id='astra'").fetchone()
if existing_model:
    cur.execute("""
        UPDATE model
        SET name='ASTRA',
            base_model_id='astra:latest',
            meta=?,
            params=?,
            updated_at=?,
            is_active=1
        WHERE id='astra'
    """, (json.dumps(model_meta), json.dumps(model_params), now))
    print("Updated model 'astra' in webui.db with high-speed GPU settings.")
else:
    cur.execute("""
        INSERT INTO model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, is_active)
        VALUES ('astra', ?, 'astra:latest', 'ASTRA', ?, ?, ?, ?, 1)
    """, (admin_id, json.dumps(model_meta), json.dumps(model_params), now, now))
    print("Inserted model 'astra' into webui.db.")

# Register Llama 3.2
llama_meta = {
    "profile_image_url": "/static/favicon.png",
    "description": "Meta Llama 3.2 3B Base Model",
    "capabilities": {"file_context": True, "vision": True, "file_upload": True},
    "suggestion_prompts": model_meta["suggestion_prompts"],
    "tags": ["llama3.2", "meta"]
}
existing_llama = cur.execute("SELECT id FROM model WHERE id='llama3.2:latest'").fetchone()
if existing_llama:
    cur.execute("UPDATE model SET is_active=1, updated_at=? WHERE id='llama3.2:latest'", (now,))
else:
    cur.execute("""
        INSERT INTO model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, is_active)
        VALUES ('llama3.2:latest', ?, 'llama3.2:latest', 'Llama 3.2 (3B)', ?, '{}', ?, ?, 1)
    """, (admin_id, json.dumps(llama_meta), now, now))

# Register Qwen 2.5 0.5B
qwen_meta = {
    "profile_image_url": "/static/favicon.png",
    "description": "Alibaba Qwen 2.5 0.5B Ultra-Fast Model",
    "capabilities": {"file_context": True, "vision": False, "file_upload": True},
    "suggestion_prompts": model_meta["suggestion_prompts"],
    "tags": ["qwen2.5", "ultra-fast"]
}
existing_qwen = cur.execute("SELECT id FROM model WHERE id='qwen2.5:0.5b'").fetchone()
if existing_qwen:
    cur.execute("UPDATE model SET is_active=1, updated_at=? WHERE id='qwen2.5:0.5b'", (now,))
else:
    cur.execute("""
        INSERT INTO model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, is_active)
        VALUES ('qwen2.5:0.5b', ?, 'qwen2.5:0.5b', 'Qwen 2.5 (0.5B Fast)', ?, '{}', ?, ?, 1)
    """, (admin_id, json.dumps(qwen_meta), now, now))

# Register ASTRA Creator Pipe Model
creator_meta = {
    "profile_image_url": "/static/favicon.png",
    "description": "Autonomous AI Creator — Generates Videos, Images, Voice Audio, and PDFs directly in chat",
    "capabilities": {"file_context": True, "vision": True, "file_upload": True, "image_generation": True},
    "suggestion_prompts": model_meta["suggestion_prompts"],
    "tags": ["astra", "creator", "video", "image"]
}
existing_creator = cur.execute("SELECT id FROM model WHERE id='astra_creator'").fetchone()
if existing_creator:
    cur.execute("UPDATE model SET is_active=1, updated_at=? WHERE id='astra_creator'", (now,))
else:
    cur.execute("""
        INSERT INTO model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, is_active)
        VALUES ('astra_creator', ?, 'astra_creator', 'ASTRA (In-Chat Video & Image)', ?, '{}', ?, ?, 1)
    """, (admin_id, json.dumps(creator_meta), now, now))

# 5. Enable & Configure Open WebUI Native Image Generation, Task Suggestions, and Prompt Suggestions in config table
config_row = cur.execute("SELECT id, data FROM config WHERE id=1").fetchone()
if config_row and config_row[1]:
    try:
        cfg_data = json.loads(config_row[1])
    except Exception:
        cfg_data = {}
else:
    cfg_data = {}

cfg_data["image_generation"] = {
    "enable": True,
    "engine": "openai",
    "openai": {
        "api_base_url": "http://127.0.0.1:8892/v1",
        "api_key": "astra",
        "model": "dreamshaper-8"
    },
    "size": "512x512",
    "steps": 25
}

if "ui" not in cfg_data or not isinstance(cfg_data["ui"], dict):
    cfg_data["ui"] = {}

cfg_data["ui"]["prompt_suggestions"] = model_meta["suggestion_prompts"]

if "task" not in cfg_data or not isinstance(cfg_data["task"], dict):
    cfg_data["task"] = {}

cfg_data["task"]["follow_up"] = {"enable": True}
cfg_data["task"]["autocomplete"] = {"enable": True}
cfg_data["task"]["title"] = {"enable": True}
cfg_data["task"]["tags"] = {"enable": True}

cfg_data["rag"] = {
    "embedding_engine": "ollama",
    "ollama": {
        "url": "http://127.0.0.1:11434",
        "model": "astra"
    }
}

if config_row:
    cur.execute("UPDATE config SET data=? WHERE id=1", (json.dumps(cfg_data),))
else:
    cur.execute("INSERT INTO config (id, data, version) VALUES (1, ?, 0)", (json.dumps(cfg_data),))
print("Configured Open WebUI Native Image Engine in webui.db.")

conn.commit()
conn.close()
print("Database sync completed successfully!")

