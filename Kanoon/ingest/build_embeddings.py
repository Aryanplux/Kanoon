#!/usr/bin/env python3
# build_embeddings.py
import os
import sqlite3
import numpy as np
from tqdm import tqdm

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "legal_docs.db")
EMB_PATH = os.path.join(DATA_DIR, "embeddings.npy")
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
NN_INDEX_PATH = os.path.join(DATA_DIR, "nn_index.joblib")

# try imports
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    raise SystemExit("Install sentence-transformers first: pip install sentence-transformers")

try:
    import faiss
    have_faiss = True
except Exception:
    have_faiss = False
    from sklearn.neighbors import NearestNeighbors
    import joblib

def fetch_docs():
    """Fetch IDs and concatenated title+content from the DB."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM documents ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    ids = [r["id"] for r in rows]
    texts = [(r["title"] + "\n\n" + (r["content"] or "")) for r in rows]
    return ids, texts

def main():
    ids, texts = fetch_docs()
    print(f"Found {len(ids)} documents. Computing embeddings...")

    # Load model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    embeddings = embeddings / norms

    # Save embeddings
    np.save(EMB_PATH, embeddings.astype(np.float32))
    print(f"✅ Embeddings saved to {EMB_PATH}")

    # Save index
    if have_faiss:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # inner-product = cosine on normalized vectors
        index.add(embeddings)
        faiss.write_index(index, FAISS_INDEX_PATH)
        print(f"✅ FAISS index written to {FAISS_INDEX_PATH}")
    else:
        nn = NearestNeighbors(n_neighbors=10, metric="cosine")
        nn.fit(embeddings)
        joblib.dump(nn, NN_INDEX_PATH)
        print(f"⚠️ FAISS not available. Saved sklearn NN index to {NN_INDEX_PATH}")

if __name__ == "__main__":
    main()