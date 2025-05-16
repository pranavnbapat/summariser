# summariser.py

import os

from config import MODEL_NAME, MAX_SUMMARY_LENGTH, MIN_SUMMARY_LENGTH
from extractor import extract_text_from_file
from llm_summariser import summarise_with_llm
from preprocessor import preprocess
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Detect model type (BART or T5) based on name
MODEL_TYPE = "t5" if "t5" in MODEL_NAME.lower() else "bart"

if MODEL_TYPE == "t5":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
else:
    summariser = pipeline("summarization", model=MODEL_NAME, device=-1)


def summarise_chunks(chunks, style="default"):
    summaries = []
    for chunk in chunks:
        input_length = len(chunk.split())

        # Dynamically adjust max_length
        dynamic_max = min(MAX_SUMMARY_LENGTH, int(input_length * 1.2))
        dynamic_min = min(MIN_SUMMARY_LENGTH, int(input_length * 0.6))

        prompt = chunk
        if style == "abstract":
            prompt = "Summarise this text:\n" + chunk
        elif style == "bullet":
            prompt = "Summarise this in bullet points:\n" + chunk

        if MODEL_TYPE == "t5":
            t5_input = f"summarise: {prompt}"
            inputs = tokenizer(t5_input, return_tensors="pt", max_length=512, truncation=True)
            summary_ids = model.generate(inputs["input_ids"], max_length=dynamic_max, min_length=dynamic_min)
            output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(output)
        else:
            result = summariser(prompt, max_length=dynamic_max, min_length=dynamic_min, do_sample=False)
            summaries.append(result[0]['summary_text'])
    return summaries


def summarise_document(filepath, mode="concise", style="default", use_llm=False, metadata=None):
    text = extract_text_from_file(filepath)

    if use_llm:
        return summarise_with_llm(text, filename=os.path.basename(filepath), metadata=metadata)

    chunks = preprocess(text)
    chunk_summaries = summarise_chunks(chunks, style=style)

    if mode == "concise":
        if len(chunk_summaries) == 1:
            return chunk_summaries[0]
        merged_text = " ".join(chunk_summaries)
        final_summary = summariser(merged_text, max_length=MAX_SUMMARY_LENGTH, min_length=MIN_SUMMARY_LENGTH, do_sample=False)
        return final_summary[0]['summary_text']
    elif mode == "hierarchical":
        return "\n\n".join([f"Chunk {i+1}: {s}" for i, s in enumerate(chunk_summaries)])
    else:
        return "Unknown summarisation mode."

