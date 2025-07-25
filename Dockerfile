# Dockerfile

FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

# Install system dependencies needed for PyMuPDF
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- IMPORTANT: Download and cache models during the build ---
# This ensures no internet is needed at runtime.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
RUN python -c "import nltk; nltk.download('punkt')"

# Copy the rest of the application source code
COPY src/. .

# Create input and output directories for mounting volumes
RUN mkdir -p /app/input/documents /app/output

# Set the entrypoint to run the main script

ENTRYPOINT ["python", "main.py"]