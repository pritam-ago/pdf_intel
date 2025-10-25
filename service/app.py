from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from ingest import ingest_pdf, search, UPLOAD_DIR
import uvicorn

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
    try:
        if not file.filename or not file.filename.endswith(".pdf"):
            return {"error": "Only PDF files allowed"}
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        chunks = ingest_pdf(file_path)
        return {"status": "success", "filename": file.filename, "chunks_added": chunks}
    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}

@app.get("/search")
def query_pdf(q: str = Query(..., description="Your question"), k: int = 5):
    try:
        if not q.strip():
            return {"error": "Query cannot be empty"}
        results = search(q, k)
        return {"query": q, "results": results}
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}


if __name__ == "__main__":
    # Allow running this module directly with `python app.py` (start script uses that)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
