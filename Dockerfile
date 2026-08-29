# ==========================================
# ASTRA AI Ecosystem — Render Dockerfile (RAM & Speed Optimized)
# ==========================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    PORT=10000 \
    MALLOC_TRIM_THRESHOLD_=100000

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    sqlite3 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy repository contents into container
COPY . /app

# 1. Pre-install CPU-only PyTorch to save 1.5GB disk & avoid CUDA RAM overload on Render
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 2. Install open-webui and core microservice dependencies
RUN pip install --no-cache-dir \
    open-webui \
    fastapi \
    uvicorn \
    requests \
    pydantic \
    fpdf2 \
    httpx \
    duckduckgo-search

# Fix line endings & permissions for Linux execution
RUN sed -i 's/\r$//' /app/render_entrypoint.sh && \
    chmod +x /app/render_entrypoint.sh

# Expose port (Render automatically maps PORT)
EXPOSE 10000

# Launch Render deployment entrypoint
CMD ["/app/render_entrypoint.sh"]
