# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for layer caching)
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    nano \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . .

# Download NLTK punkt tokenizer
RUN python -m nltk.downloader punkt punkt_tab

# Expose FastAPI port
EXPOSE 11000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "11000"]
