# llm_summariser.py

import os
import requests
import time
import urllib3

# from ollama import Client

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama_euf_summariser:11434")
# client = Client(host=OLLAMA_HOST)

POD_ID = os.getenv("RUNPOD_POD_ID", "v9zpf5kzgkvf1r")
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

OLLAMA_RUNPOD_HOST = os.getenv("OLLAMA_RUNPOD_HOST", "https://v9zpf5kzgkvf1r-11434.proxy.runpod.net")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "mistral")

# LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "mistral")


def start_runpod_pod(pod_id, api_key):
    print(f"🔄 Starting pod {pod_id}...")
    url = "https://api.runpod.io/graphql"
    headers = {"Authorization": api_key}
    query = {
        "query": f"""
        mutation {{
            podResume(input: {{ podId: "{pod_id}" }}) {{
                id
            }}
        }}
        """
    }
    r = requests.post(url, json=query, headers=headers)
    print("✅ Pod start requested:", r.json())


def wait_until_pod_ready(url, timeout=300):
    print(f"⏳ Waiting for {url} to respond...")
    for _ in range(timeout // 5):
        try:
            if requests.get(url, timeout=5, verify=False).status_code == 200:
                print("✅ Pod is ready.")
                return True
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError("❌ Pod did not become ready in time.")


def stop_runpod_pod(pod_id, api_key):
    print(f"🛑 Stopping pod {pod_id}...")
    url = "https://api.runpod.io/graphql"
    headers = {"Authorization": api_key}
    query = {
        "query": f"""
        mutation {{
            podStop(input: {{ podId: "{pod_id}" }}) {{
                id
            }}
        }}
        """
    }
    r = requests.post(url, json=query, headers=headers)
    print("✅ Pod stop requested:", r.json())


def summarise_with_llm(text, filename="", doc_type="auto", metadata=None, model=LLM_MODEL_NAME):
    if metadata is None:
        metadata = {}

    meta_str = "\n".join([f"{k}: {v}" for k, v in metadata.items()])

    prompt = f"""
You are an intelligent assistant that analyses a wide variety of text documents — including invoices, scientific 
reports, meeting notes, technical summaries, project deliverables, and research findings.

Document filename: {filename}
Document type: {doc_type}
Additional metadata:
{meta_str}

Extracted document text:
{text}

Please do the following:
- Identify the type of document (e.g. factsheet, scientific or technical paper, summary note, project information, 
practice abstracts, etc.).
- Then, write a short paragraph (approximately five to ten sentences) that clearly summarises the document.
- Do not include bullet points, lists, or headings. Write as if you're explaining the document naturally to a colleague.
- Focus on what is clearly present in the text. Do not guess or invent details.

Return your response in plain text.
"""

    try:
        # Start and wait
        start_runpod_pod(POD_ID, RUNPOD_API_KEY)
        wait_until_pod_ready(OLLAMA_RUNPOD_HOST)

        response = requests.post(
            f"{OLLAMA_RUNPOD_HOST}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            verify=False
        )
        return response.json()['message']['content']

    except Exception as e:
        print(f"[LLM ERROR] Failed to summarise: {e}")
        return "Error: Unable to generate summary at this time."

    finally:
        stop_runpod_pod(POD_ID, RUNPOD_API_KEY)
