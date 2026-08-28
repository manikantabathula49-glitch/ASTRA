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

# Execute run_webui.py which handles Open WebUI config and dynamic PORT binding
exec python run_webui.py
