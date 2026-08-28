# ==========================================
# ASTRA AI Ecosystem — Render Dockerfile
# ==========================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    PORT=10000

# Install essential system dependencies (FFmpeg, Git, SQLite3, build tools)
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

# Install open-webui and core Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
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
