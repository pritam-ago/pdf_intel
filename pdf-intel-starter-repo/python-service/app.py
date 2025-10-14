from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
import shutil

from ingest import extract_text_from_pdf

app = FastAPI(title="pdf-intel-python-service")

STORAGE_DIR = Path(__file__).parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    dest = STORAGE_DIR / f"{uuid.uuid4().hex}_{file.filename}"
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    text = extract_text_from_pdf(str(dest))
    # For now just return some metadata and a text-snippet
    return JSONResponse({"filename": file.filename, "id": dest.name, "snippet": text[:1000]})


@app.get("/health")
def health():
    return {"status": "ok"}
