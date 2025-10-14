# Python Service

Lightweight FastAPI service to upload PDFs and extract text. Quick start:

1. Create a virtualenv and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run the service:

```powershell
uvicorn app:app --reload
```

3. Upload a PDF to POST /upload using curl, Postman, or the React client.
