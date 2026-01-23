FROM python:3.10-slim

LABEL maintainer="Ministria e Shëndetësisë - Albania"
LABEL description="MRI Analysis Web Application with AI"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV TOTALSEG_WEIGHTS_PATH=/app/models

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p /tmp/uploads /app/models

# Download TotalSegmentator models on first run (optional - can be done at runtime)
# Uncomment to pre-download models (increases image size but faster first run)
# RUN python -c "from totalsegmentator.python_api import totalsegmentator; print('Models will download on first use')"

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "app.py"]
