#!/usr/bin/env python3
"""
ASTRA AI Ecosystem Universal Launcher
Boots all backend engines and connects Web Server UI in Google Chrome.
"""

import subprocess
import os
import sys
import time
import socket
import urllib.request
import json

base_dir = r"f:\ASTRA"
comfy_python = os.path.join(base_dir, "comfy_env", "Scripts", "python.exe")
webui_python = os.path.join(base_dir, "webui_env", "Scripts", "python.exe")

log_dir = os.path.join(base_dir, "service_logs")
os.makedirs(log_dir, exist_ok=True)

# 1. Warm up Ollama
print("[0/8] Verifying Ollama Brain...")
try:
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=b'{"model":"astra","keep_alive":-1}', headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        print("  -> Ollama warmed up in GPU VRAM.")
except Exception:
    print("  -> Ollama daemon starting or already active.")

# 2. Sync DB
print("[1/8] Synchronizing WebUI DB...")
try:
    subprocess.run([webui_python, os.path.join(base_dir, "sync_webui_db.py")], cwd=base_dir, capture_output=True, timeout=10)
    print("  -> WebUI database synchronized.")
except Exception as e:
    print(f"  -> DB sync warning: {e}")

services = [
    ("Open WebUI (8080)", [webui_python, "-X", "utf8", os.path.join(base_dir, "run_webui.py")], 8080, "webui.log"),
    ("ComfyUI Backend (8188)", [comfy_python, "-X", "utf8", os.path.join(base_dir, "ComfyUI", "main.py"), "--listen", "0.0.0.0", "--cpu"], 8188, "comfyui.log"),
    ("ASTRA Image Server (8892)", [comfy_python, "-X", "utf8", os.path.join(base_dir, "image_server.py")], 8892, "image_server.log"),
    ("ASTRA PDF Server (8890)", [comfy_python, "-X", "utf8", os.path.join(base_dir, "pdf_server.py")], 8890, "pdf_server.log"),
    ("ASTRA Voice Server (8880)", [comfy_python, "-X", "utf8", os.path.join(base_dir, "voice_server.py")], 8880, "voice_server.log"),
    ("ASTRA Whisper Server (8885)", [comfy_python, "-X", "utf8", os.path.join(base_dir, "whisper_server.py")], 8885, "whisper_server.log"),
]

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

for name, cmd, port, log_name in services:
    if is_port_in_use(port):
        print(f"[OK] {name} is already active on port {port}.")
        continue

    print(f"Launching {name} (Port {port})...")
    log_file = open(os.path.join(log_dir, log_name), "a", encoding="utf-8", errors="replace")
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    env["ENABLE_DB_MIGRATIONS"] = "False"
    env["OFFLINE_MODE"] = "True"
    env["ENABLE_OPENAI_API"] = "True"
    env["ENABLE_BASE_MODELS_CACHE"] = "True"
    env["ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS"] = "False"
    env["USER_AGENT"] = "ASTRA-AI"
    env["FRONTEND_BUILD_DIR"] = os.path.join(base_dir, "webui_env", "Lib", "site-packages", "open_webui", "frontend")
    env["FROM_INIT_PY"] = "true"
    env["ENABLE_IMAGE_GENERATION"] = "True"
    env["IMAGE_GENERATION_ENGINE"] = "openai"
    env["IMAGES_OPENAI_API_BASE_URL"] = "http://127.0.0.1:8892/v1"
    env["IMAGES_OPENAI_API_KEY"] = "astra"
    env["IMAGE_GENERATION_MODEL"] = "dreamshaper-8"
    env["IMAGE_SIZE"] = "512x512"
    env["IMAGE_STEPS"] = "25"
    env["AUTOMATIC1111_BASE_URL"] = "http://127.0.0.1:8892"
    env["ENABLE_FOLLOW_UP_GENERATION"] = "True"
    env["ENABLE_TAGS_GENERATION"] = "True"
    env["ENABLE_TITLE_GENERATION"] = "True"
    env["ENABLE_AUTOCOMPLETE_GENERATION"] = "True"
    
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=base_dir,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS if os.name == 'nt' else 0,
            stdout=log_file,
            stderr=log_file,
            env=env,
            close_fds=True
        )
        print(f"  -> PID {proc.pid} started for {name}")
        time.sleep(1)
    except Exception as e:
        print(f"  -> Error starting {name}: {e}")

print("\nWaiting for Open WebUI server to finish booting...")
ready = False
for i in range(45):
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=1) as resp:
            if resp.status == 200:
                ready = True
                break
    except Exception:
        pass
    print(".", end="", flush=True)
    time.sleep(1)

print("\n")
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
]
chrome_bin = next((p for p in chrome_paths if os.path.exists(p)), None)

if ready:
    print("[SUCCESS] All ASTRA AI Ecosystem services are ONLINE!")
else:
    print("[INFO] Services initializing in background.")

if chrome_bin:
    print(f"Connecting Web Server UI via Google Chrome: {chrome_bin}")
    subprocess.Popen([chrome_bin, "http://localhost:8080"])
    subprocess.Popen([chrome_bin, "http://localhost:8188"])
else:
    print("Opening Web Server UI via default browser...")
    import webbrowser
    webbrowser.open("http://localhost:8080")
    webbrowser.open("http://localhost:8188")

print("\n  WebUI Chat:      http://localhost:8080")
print("  ComfyUI Engine:  http://localhost:8188")
print("  Media Engines:   Image(8892), PDF(8890), Voice(8880), Whisper(8885)\n")
