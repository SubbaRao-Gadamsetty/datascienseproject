FROM python:3.9-slim

WORKDIR /app

# Install system dependencies efficiently
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copy application code
COPY . .

# Add health check endpoint support
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || curl -f http://localhost:8080/ || exit 1

# Expose the port your app runs on
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]