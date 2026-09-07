import requests
import json

endpoints = [
    ("Ollama Brain (11434)", "http://localhost:11434/api/tags"),
    ("Open WebUI Chat (8080)", "http://localhost:8080/health"),
    ("ASTRA Image Server (8892)", "http://localhost:8892/health"),
    ("ASTRA PDF Server (8890)", "http://localhost:8890/health"),
    ("ASTRA Voice Server (8880)", "http://localhost:8880/health"),
    ("ASTRA Whisper Server (8885)", "http://localhost:8885/health"),
    ("ComfyUI Visual Engine (8188)", "http://localhost:8188/system_stats"),
]

print("\n--- ASTRA SERVICE HEALTH CHECKS ---")
for name, url in endpoints:
    try:
        r = requests.get(url, timeout=3)
        print(f"[OK] {name}: Status {r.status_code}")
        try:
            print(f"     Response: {json.dumps(r.json(), indent=2)[:200]}...")
        except Exception:
            print(f"     Text: {r.text[:100]}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
