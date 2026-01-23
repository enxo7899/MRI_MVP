# ============================================================================
# MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
# MONAI Label AI Engine - Dockerfile
# Medical Image AI Platform
# ============================================================================

FROM python:3.10-slim

LABEL maintainer="Ministria e Shëndetësisë - Albania <it@shendetesia.gov.al>"
LABEL description="MONAI Label AI Engine with Albanian Localization"
LABEL version="1.0.0"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MONAI_LABEL_APP=/app/apps/ministry_app
ENV MONAI_LABEL_STUDIES=http://orthanc:8042/dicom-web
ENV MONAI_LABEL_HOST=0.0.0.0
ENV MONAI_LABEL_PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY apps/ /app/apps/

# Create model directory
RUN mkdir -p /app/model && chmod 777 /app/model

# Create logs directory
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/info/ || exit 1

# Expose port
EXPOSE 8000

# Entry point
CMD ["monailabel", "start_server", \
     "--app", "/app/apps/ministry_app", \
     "--studies", "http://orthanc:8042/dicom-web", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
