import os
import sys

# Ensure UTF-8 streams to prevent Windows charmap encoding crashes on emojis / banners
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 1. Set environment variables FIRST before importing open_webui
os.environ["WEBUI_SECRET_KEY"] = os.environ.get("WEBUI_SECRET_KEY", "p0/6YLuw3mv6mLiP")
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["OLLAMA_BASE_URL"] = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
os.environ["DEFAULT_MODELS"] = os.environ.get("DEFAULT_MODELS", "astra")
os.environ["FROM_INIT_PY"] = "true"

# Native Open WebUI Image Generation via ASTRA Image Server
os.environ["ENABLE_IMAGE_GENERATION"] = "True"
os.environ["IMAGE_GENERATION_ENGINE"] = "openai"
os.environ["IMAGES_OPENAI_API_BASE_URL"] = "http://127.0.0.1:8892/v1"
os.environ["IMAGES_OPENAI_API_KEY"] = "astra"
os.environ["IMAGE_GENERATION_MODEL"] = "dreamshaper-8"
os.environ["IMAGE_SIZE"] = "512x512"
os.environ["IMAGE_STEPS"] = "25"
os.environ["AUTOMATIC1111_BASE_URL"] = "http://127.0.0.1:8892"

# Disable telemetry, external analytics, and redundant migrations for instant boot
os.environ["ENABLE_DB_MIGRATIONS"] = "False"
os.environ["OFFLINE_MODE"] = "True"
os.environ["ENABLE_VERSION_UPDATE_CHECK"] = "False"
os.environ["ENABLE_ADMIN_ANALYTICS"] = "False"
os.environ["ENABLE_OTEL"] = "False"
os.environ["ENABLE_BASE_MODELS_CACHE"] = "False"
os.environ["ENABLE_OPENAI_API"] = "False"
os.environ["OPENAI_API_BASE_URLS"] = ""
os.environ["OPENAI_API_KEYS"] = ""
os.environ["ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS"] = "False"
os.environ["USER_AGENT"] = "ASTRA-AI"
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["SCARF_NO_ANALYTICS"] = "True"
os.environ["DO_NOT_TRACK"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# Ultra-Low Latency Instant Startup for Cloud Deployment
os.environ["RAG_EMBEDDING_ENGINE"] = ""
os.environ["AUDIO_STT_ENGINE"] = ""
os.environ["AUDIO_TTS_ENGINE"] = ""
os.environ["ENABLE_RAG_LOCAL_WEB_FETCH"] = "False"
os.environ["ENABLE_SEARCH_QUERY_GENERATION"] = "False"
os.environ["ENABLE_RETRIEVAL_QUERY_GENERATION"] = "False"
os.environ["ENABLE_FOLLOW_UP_GENERATION"] = "True"
os.environ["ENABLE_TAGS_GENERATION"] = "True"
os.environ["ENABLE_TITLE_GENERATION"] = "True"
os.environ["ENABLE_AUTOCOMPLETE_GENERATION"] = "True"
os.environ["ENABLE_MEMORIES"] = "False"
os.environ["ENABLE_RAG_HYBRID_SEARCH"] = "False"
os.environ["ENABLE_WEB_SEARCH"] = "False"
os.environ["OLLAMA_KEEP_ALIVE"] = "-1"

# 2. Add local site-packages if present
base_dir = os.path.abspath(os.path.dirname(__file__))
site_packages_dir = os.path.join(base_dir, "webui_env", "Lib", "site-packages")
if os.path.exists(site_packages_dir) and site_packages_dir not in sys.path:
    sys.path.insert(0, site_packages_dir)

# 3. Import open_webui after environment configuration
try:
    import open_webui
    open_webui_dir = os.path.dirname(open_webui.__file__)
except ImportError:
    open_webui_dir = os.path.join(site_packages_dir, "open_webui")

data_dir = os.environ.get("DATA_DIR", os.path.join(open_webui_dir, "data"))
os.makedirs(data_dir, exist_ok=True)
os.environ["DATA_DIR"] = data_dir

frontend_dir = os.environ.get("FRONTEND_BUILD_DIR", os.path.join(open_webui_dir, "frontend"))
os.environ["FRONTEND_BUILD_DIR"] = frontend_dir

def _create_app():
    from open_webui.main import app as _webui_app

    @_webui_app.get("/health", include_in_schema=False)
    async def render_health_check():
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=200,
            content={"status": "ok", "service": "astra-ai-ecosystem", "healthy": True},
        )

    return _webui_app


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Launching Uvicorn web server on 0.0.0.0:{port}...", flush=True)
    uvicorn.run("run_webui:_create_app", host="0.0.0.0", port=port, reload=False, factory=True)
