# Health Data Analyst Agent - Production Docker Image
# Optimized for faster builds

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (faster layer caching)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with timeout and retries
# Split installation for better error handling
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --timeout 100 \
    streamlit==1.31.1 \
    pandas==2.2.0 \
    python-dotenv==1.0.1 && \
    pip install --no-cache-dir --timeout 100 \
    fastapi==0.109.0 \
    "uvicorn[standard]==0.27.0" \
    pydantic==2.5.3 && \
    pip install --no-cache-dir --timeout 100 \
    plotly==5.18.0 \
    matplotlib==3.8.2 && \
    pip install --no-cache-dir --timeout 100 \
    groq \
    pytest \
    pyyaml \
    python-docx \
    pandasql \
    rouge-score

COPY src ./src
COPY config ./config
COPY data ./data
COPY app.py .

# Create data directory
RUN mkdir -p data reports

# Expose ports
EXPOSE 8501 8000

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Default command (Streamlit for demo)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

