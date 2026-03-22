FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend_requirements.txt

# Copy application
COPY backend_main.py .

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "backend_main:app", "--host", "0.0.0.0", "--port", "8000"]
