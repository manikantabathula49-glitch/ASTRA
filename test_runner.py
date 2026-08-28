import subprocess
import os
import sys
import time

base_dir = r"f:\ASTRA"
comfy_python = os.path.join(base_dir, "comfy_env", "Scripts", "python.exe")

# Test starting image_server and logging to file
log_out = open(os.path.join(base_dir, "image_server.log"), "w", encoding="utf-8")
log_err = open(os.path.join(base_dir, "image_server_err.log"), "w", encoding="utf-8")

proc = subprocess.Popen(
    [comfy_python, os.path.join(base_dir, "image_server.py")],
    cwd=base_dir,
    stdout=log_out,
    stderr=log_err
)

print(f"Started image_server with PID {proc.pid}")
time.sleep(5)

# Check if process is still alive
poll = proc.poll()
print(f"Process poll status: {poll} (None means running)")

# Read log files
log_out.flush()
log_err.flush()
with open(os.path.join(base_dir, "image_server.log"), "r", encoding="utf-8") as f:
    print("STDOUT:", f.read())
with open(os.path.join(base_dir, "image_server_err.log"), "r", encoding="utf-8") as f:
    print("STDERR:", f.read())
