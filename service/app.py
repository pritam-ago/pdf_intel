from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from ingest import ingest_pdf, search, UPLOAD_DIR

app = FastAPI(title="PDF Intelligence System")

# Allow frontend (React/Java) CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "PDF Intelligence System API is running 🚀"}

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files allowed"}
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    chunks = ingest_pdf(file_path)
    return {"status": "success", "filename": file.filename, "chunks_added": chunks}

@app.get("/search")
def query_pdf(q: str = Query(..., description="Your question"), k: int = 5):
    results = search(q, k)
    return {"query": q, "results": results}
