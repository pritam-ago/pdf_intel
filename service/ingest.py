import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "pdf_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
qdrant = QdrantClient(url=QDRANT_URL)

def ensure_collection():
    collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in collections:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

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

def ingest_pdf(filepath):
    ensure_collection()
    filename = os.path.basename(filepath)
    text = extract_text_from_pdf(filepath)
    chunks = chunk_text(text)

    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    points = []
    for i, chunk in enumerate(chunks):
        points.append(
            PointStruct(
                id=None,  # Let Qdrant auto-assign
                vector=embeddings[i],
                payload={"text": chunk, "source": filename, "chunk_index": i},
            )
        )

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)

def search(query, k=5):
    ensure_collection()
    query_vec = model.encode([query])[0].astype("float32")
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=k,
    )
    output = []
    for r in results:
        payload = r.payload
        payload["score"] = r.score
        output.append(payload)
    return output
