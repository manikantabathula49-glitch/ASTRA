import requests
import json
import time

print("[1] Submitting prompt to ASTRA Image Server...")
url = "http://localhost:8892/generate"
payload = {
    "prompt": "a glowing neon futuristic cyberpunk robot, masterpiece, 8k, highly detailed",
    "steps": 20,
    "width": 512,
    "height": 512
}

res = requests.post(url, json=payload, timeout=10)
print(f"Status Code: {res.status_code}")
data = res.json()
print("Response:", data)

job_id = data.get("job_id")
print(f"[2] Polling job ID {job_id}...")

start = time.time()
while time.time() - start < 120:
    time.sleep(2)
    try:
        r = requests.get(f"http://localhost:8892/status/{job_id}", timeout=5)
        st = r.json()
        print(f"  -> Status: {st.get('status')}, Progress: {st.get('progress')}")
        if st.get("status") == "done":
            print(f"[OK] Image generation complete! Filename: {st.get('filename')}")
            print(f"Download URL: http://localhost:8892/download/{st.get('filename')}")
            break
        elif st.get("status") == "error":
            print(f"[ERROR] Generation failed: {st.get('error')}")
            break
    except Exception as e:
        print("Polling error:", e)

print("Test finished.")
