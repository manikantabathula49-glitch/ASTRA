#!/usr/bin/env python3
"""
ASTRA Ecosystem Process Supervisor
Manages and keeps all ASTRA microservices and WebUI alive in persistent background processes.
"""

import os
import sys
import time
import socket
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMFY_PY = os.path.join(BASE_DIR, "comfy_env", "Scripts", "python.exe")
WEBUI_PY = os.path.join(BASE_DIR, "webui_env", "Scripts", "python.exe")

SERVICES = {
    "WebUI": {
        "cmd": [WEBUI_PY, os.path.join(BASE_DIR, "run_webui.py")],
        "port": 8080,
    },
    "ImageEngine": {
        "cmd": [COMFY_PY, os.path.join(BASE_DIR, "image_server.py")],
        "port": 8892,
    },
    "VideoEngine": {
        "cmd": [COMFY_PY, os.path.join(BASE_DIR, "video_server.py")],
        "port": 8891,
    },
    "PDFEngine": {
        "cmd": [COMFY_PY, os.path.join(BASE_DIR, "pdf_server.py")],
        "port": 8890,
    },
    "VoiceEngine": {
        "cmd": [COMFY_PY, os.path.join(BASE_DIR, "voice_server.py")],
        "port": 8880,
    },
    "WhisperEngine": {
        "cmd": [COMFY_PY, os.path.join(BASE_DIR, "whisper_server.py")],
        "port": 8885,
    },
    "ComfyUI": {
        "cmd": [COMFY_PY, os.path.join(BASE_DIR, "ComfyUI", "main.py"), "--listen", "0.0.0.0", "--cpu"],
        "port": 8188,
    },
}

running_procs = {}

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_service(name):
    conf = SERVICES[name]
    port = conf["port"]

    if is_port_in_use(port):
        print(f"[OK] {name} is already active on Port {port}.")
        return None

    log_dir = os.path.join(BASE_DIR, "service_logs")
    os.makedirs(log_dir, exist_ok=True)
    out_file = open(os.path.join(log_dir, f"{name.lower()}.log"), "a", encoding="utf-8", errors="replace")
    
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    
    print(f"[*] Starting {name} (Port {port})...")
    proc = subprocess.Popen(
        conf["cmd"],
        cwd=BASE_DIR,
        stdout=out_file,
        stderr=out_file,
        env=env
    )
    running_procs[name] = (proc, out_file)
    return proc

def monitor():
    # Initial startup of all services
    for name in SERVICES:
        start_service(name)
        time.sleep(1)

    print("\n====================================================")
    print(" [OK] ASTRA Ecosystem Supervisor Online")
    print(" Monitoring ports: 8080, 8188, 8880, 8885, 8890, 8891, 8892")
    print("====================================================\n")

    while True:
        time.sleep(5)
        for name in list(SERVICES.keys()):
            conf = SERVICES[name]
            port = conf["port"]
            if not is_port_in_use(port):
                print(f"[!] Warning: {name} on port {port} is not responding. Starting/Restarting...")
                start_service(name)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nStopping all supervised ASTRA services...")
        for name, (proc, out_file) in running_procs.items():
            try:
                proc.terminate()
                out_file.close()
            except Exception:
                pass
        sys.exit(0)
