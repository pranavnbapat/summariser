# preprocessor.py

import nltk
import re

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
    nltk.download("punkt_tab")

from nltk.tokenize import sent_tokenize


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)  # collapse all whitespace
    text = re.sub(r'\n+', '\n', text)  # preserve paragraph breaks
    return text.strip()


def tag_formulas(text: str) -> str:
    formula_patterns = [
        r"\$.*?\$", r"\\\\\[.*?\\\\\]", r"\\\\\(.*?\\\\\)", r"(?<!\w)[A-Z]=[^=\n]+"
    ]
    for pattern in formula_patterns:
        text = re.sub(pattern, '[FORMULA]', text)
    return text


def tag_tables(text: str) -> str:
    table_pattern = re.compile(r"(?:\w+\s*\|\s*){2,}.*(?:\n|$)", re.MULTILINE)
    return table_pattern.sub("[TABLE]", text)


def chunk_text(text: str, max_words=850, overlap=100):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sent in sentences:
        words = sent.split()
        if current_length + len(words) <= max_words:
            current_chunk.append(sent)
            current_length += len(words)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-5:] + [sent]  # last 5 for overlap
            current_length = sum(len(s.split()) for s in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def preprocess(text: str):
    cleaned = clean_text(text)
    cleaned = tag_formulas(cleaned)
    cleaned = tag_tables(cleaned)
    return chunk_text(cleaned)