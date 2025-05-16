# main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Form
from fastapi.responses import JSONResponse
from summariser import summarise_document
from typing import Optional
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/summarise")
async def summarise(
    file: UploadFile = File(...),
    mode: str = Query("concise", enum=["concise", "hierarchical"]),
    style: str = Query("default", enum=["default", "abstract", "bullet"]),
    use_llm: Optional[bool] = Form(True)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        summary = summarise_document(file_path, mode=mode, style=style, use_llm=use_llm)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
