# config.py

import os

from dotenv import load_dotenv

load_dotenv()

# Model used for summarisation
MODEL_NAME = os.getenv("MODEL_NAME", "facebook/bart-large-cnn")

# Default chunk size (in approx. words)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 700))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 80))

# Tesseract OCR language
OCR_LANG = os.getenv("OCR_LANG", "eng")

# Upload and temporary file directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# Optional future config
MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", 350))
MIN_SUMMARY_LENGTH = int(os.getenv("MIN_SUMMARY_LENGTH", 120))
