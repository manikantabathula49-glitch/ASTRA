#!/bin/bash
# ==========================================
# ASTRA AI Ecosystem — Render Entrypoint Script
# ==========================================

export PORT="${PORT:-10000}"
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

echo "===================================================="
echo " 🚀 Booting ASTRA Ecosystem on Render (Port $PORT)"
echo "===================================================="

# Start Web UI bound to Render PORT
exec python -m uvicorn open_webui.main:app --host 0.0.0.0 --port "$PORT"
