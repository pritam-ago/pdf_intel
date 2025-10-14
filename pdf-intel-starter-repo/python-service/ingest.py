"""Simple PDF ingestion utilities.

This module demonstrates extracting text from PDFs and saving metadata.
"""
from pathlib import Path
from typing import List
import PyPDF2


def extract_text_from_pdf(path: str) -> str:
    """Extracts text from a PDF file. Returns the concatenated text of pages."""
    text = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)


def ingest_files(paths: List[str], storage_dir: str) -> List[str]:
    """Ingest given PDF paths and write plain-text copies to storage_dir. Returns list of written files."""
    out_files = []
    storage = Path(storage_dir)
    storage.mkdir(parents=True, exist_ok=True)
    for p in paths:
        txt = extract_text_from_pdf(p)
        out_path = storage / (Path(p).stem + ".txt")
        out_path.write_text(txt, encoding="utf-8")
        out_files.append(str(out_path))
    return out_files


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python ingest.py <storage_dir> <pdf1> [pdf2 ...]")
    else:
        storage_dir = sys.argv[1]
        files = sys.argv[2:]
        written = ingest_files(files, storage_dir)
        print("Wrote:")
        for w in written:
            print(w)
