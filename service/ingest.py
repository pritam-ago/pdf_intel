import os
import json
import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
INDEX_FILE = os.path.join(DATA_DIR, "faiss.index")
META_FILE = os.path.join(DATA_DIR, "metadata.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load sentence transformer model (downloads automatically)
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def load_or_create_index():
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(META_FILE, "r") as f:
            metadata = json.load(f)
    else:
        index = faiss.IndexFlatL2(384)  # embedding dim for all-MiniLM-L6-v2
        metadata = []
    return index, metadata

def save_index(index, metadata):
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

def ingest_pdf(filepath):
    text = extract_text_from_pdf(filepath)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    index, metadata = load_or_create_index()
    start_id = len(metadata)
    ids = list(range(start_id, start_id + len(chunks)))
    index.add(embeddings)
    for i, chunk in zip(ids, chunks):
        metadata.append({"id": i, "text": chunk, "source": os.path.basename(filepath)})
    save_index(index, metadata)
    return len(chunks)

def search(query, k=5):
    index, metadata = load_or_create_index()
    if len(metadata) == 0:
        return []
    query_vec = model.encode([query]).astype("float32")
    D, I = index.search(query_vec, k)
    results = []
    for idx, dist in zip(I[0], D[0]):
        if idx < len(metadata):
            item = metadata[idx]
            item["score"] = float(dist)
            results.append(item)
    return results
