#!/bin/bash
# ==========================================
# ASTRA AI Ecosystem — Render Entrypoint Script
# ==========================================

export PORT="${PORT:-10000}"
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export PYTHONUNBUFFERED=1

echo "===================================================="
echo " 🚀 Booting ASTRA Ecosystem on Render (Port $PORT)"
echo "===================================================="

# Execute run_webui.py with unbuffered logs for instant port binding
exec python -u run_webui.py
