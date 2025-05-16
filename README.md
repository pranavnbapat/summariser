# 📄 EUF Summariser – FastAPI-based Document Summarisation Service

This project provides an intelligent document summarisation service via a FastAPI API. It supports multiple document types (PDF, DOCX, TXT), uses traditional transformer-based summarisation (e.g., BART, T5), and can optionally leverage an external LLM (e.g., Mistral via Ollama on RunPod) for richer summaries.

---

## 🚀 Features

- ✅ Summarise text from **PDF**, **DOCX**, and **TXT** files
- 🧠 Two summarisation modes:
  - **Concise**: One-paragraph output
  - **Hierarchical**: Per-chunk summaries
- 🤖 Supports:
  - Pre-trained HuggingFace models (`facebook/bart-large-cnn`, `t5-base`, etc.)
  - Remote LLM (e.g. **Mistral**) via **RunPod** + **Ollama**
- 📝 Handles OCR for scanned PDFs (via Tesseract)
- 🧼 Preprocessing includes cleaning, formula/table tagging, and smart chunking

---

## 🧩 File Structure

```text
.
├── config.py           # Environment-based config loader
├── deploy.sh           # Docker image build and push script
├── extractor.py        # File parsers for PDF, DOCX, TXT (OCR included)
├── llm_summariser.py   # RunPod + Ollama-based LLM summariser client
├── main.py             # FastAPI application
├── preprocessor.py     # Text cleaner, formula/table tagger, chunker
├── summariser.py       # Core summarisation logic
├── .env.sample         # Sample environment configuration
├── requirements.txt    # Dependencies
```


---

## ⚙️ Installation

### Prerequisites

- Python 3.9+
- Tesseract OCR (for scanned PDF support)
- Docker (for deployment)
- Optional: [RunPod](https://www.runpod.io/) account with pod access and Ollama setup

### Local Setup

```shell
# Clone the repository
git clone https://github.com/pranavnbapat/summariser.git
cd euf-summariser

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.sample .env
```


## 📡 API Usage

### ▶️ Run the API locally
```shell
uvicorn main:app --reload
```

### 📨 Endpoint: /summarise
The server will start at: `http://localhost:8000`

### 🔧 Query Parameters

| Name  | Type   | Required | Description                               |
| ----- | ------ | -------- | ----------------------------------------- |
| mode  | string | ❌        | `"concise"` (default) or `"hierarchical"` |
| style | string | ❌        | `"default"`, `"abstract"`, or `"bullet"`  |


### 📦 Form Fields
| Name     | Type       | Required | Description                                 |
| -------- | ---------- | -------- | ------------------------------------------- |
| file     | UploadFile | ✅        | PDF, DOCX, or TXT file                      |
| use\_llm | boolean    | ❌        | Whether to use remote LLM (default: `true`) |


## 🧠 LLM Integration (via RunPod + Ollama)
To enable summarisation using a remote LLM (like **Mistral** via **Ollama** on RunPod):

1. Add the following to your `.env` file:
   - `RUNPOD_API_KEY`
   - `RUNPOD_POD_ID`
   - `OLLAMA_RUNPOD_HOST`

2. Set `use_llm=true` in your API call to:
   - 🔄 Automatically start the pod
   - 📤 Send a summarisation prompt with extracted document text
   - ✅ Receive a plain-text summary
   - 🛑 Shut down the pod after completion

The LLM prompt is designed to elicit **natural, human-like summaries** using available metadata and document content.


## 🐳 Docker Deployment

### Build & Push (from local)
```shell
./deploy.sh
```

### Pull & Run (on server)
```shell
docker compose pull euf_summariser
docker compose up -d
```
Make sure euf_summariser service is defined in your docker-compose.yml


## 📦 Supported Formats

### The API currently supports the following file types:

- ✅ **`.pdf`** — includes OCR fallback for scanned documents
- ✅ **`.docx`** — standard Microsoft Word documents
- ✅ **`.txt`** — plain text files

Other file types are **not supported** and will result in a `400 Bad Request` error.


## 🔧 Environment Variables

### You can configure the system behaviour via .env:

| Variable           | Default                   | Description                        |
|--------------------|---------------------------|------------------------------------|
| MODEL_NAME         | `facebook/bart-large-cnn` | HuggingFace model name             |
| CHUNK_SIZE         | `700`                     | Max words per chunk                |
| CHUNK_OVERLAP      | `80`                      | Words overlapping across chunks    |
| OCR_LANG           | `eng`                     | Tesseract OCR language             |
| UPLOAD_DIR         | `uploads`                 | Directory to store uploads         |
| MAX_SUMMARY_LENGTH | `350`                     | Max words for summary              |
| MIN_SUMMARY_LENGTH | `120`                     | Min words for summary              |
| LLM_MODEL_NAME     | `mistral`                 | LLM model for remote inference     |
| RUNPOD_API_KEY     | -                         | Required for RunPod pod management |
| RUNPOD_POD_ID      | -                         | Pod ID on RunPod                   |
| OLLAMA_RUNPOD_HOST | -                         | Ollama host URL on RunPod          |



## 📚 Example Output

```shell
{
  "summary": "This document presents a detailed overview of..."
}

```

