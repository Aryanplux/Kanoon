# translator/legal_index.py
import os
import sqlite3
import re
import numpy as np
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = str(DATA_DIR / "legal_docs.db")
EMB_PATH = str(DATA_DIR / "embeddings.npy")
FAISS_INDEX_PATH = str(DATA_DIR / "faiss.index")
NN_INDEX_PATH = str(DATA_DIR / "nn_index.joblib")

# lazy imports
_model = None
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

try:
    import faiss
    _have_faiss = True
except Exception:
    _have_faiss = False
    try:
        import joblib
        from sklearn.neighbors import NearestNeighbors
    except Exception:
        joblib = None

_conn = None

def connect_db():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH)
        _conn.row_factory = sqlite3.Row
    return _conn

def normalize_title(s: str) -> str:
    return re.sub(r'[^0-9a-zA-Z]+', ' ', s).strip().lower()

def title_match(query: str, max_results=5):
    """Try to detect explicit Article/Section reference and match titles exactly"""
    conn = connect_db()
    cur = conn.cursor()
    q_norm = normalize_title(query)
    m = re.search(r'(article|section|sec|art)?\s*[:#]?\s*([0-9]+[A-Za-z\-]*)', q_norm)
    if m:
        token = m.group(2)
        cur.execute("SELECT id,title,content FROM documents WHERE lower(title) LIKE ? LIMIT ?", ('%'+token+'%', max_results))
        rows = cur.fetchall()
        if rows:
            return [(r['title'], r['content']) for r in rows]
    cur.execute("SELECT id,title,content FROM documents WHERE lower(title)=? LIMIT ?", (q_norm, max_results))
    rows = cur.fetchall()
    return [(r['title'], r['content']) for r in rows]

def fts_search(query: str, top_k=5):
    """Full-text search via FTS5 if available, else fallback to LIKE"""
    conn = connect_db()
    cur = conn.cursor()
    try:
        q = " ".join(re.findall(r'\w+', query))
        cur.execute("SELECT rowid, title, content FROM documents_fts WHERE documents_fts MATCH ? LIMIT ?", (q, top_k))
        rows = cur.fetchall()
        return [(r['title'], r['content']) for r in rows]
    except sqlite3.OperationalError:
        pat = f"%{query}%"
        cur.execute("SELECT id,title,content FROM documents WHERE title LIKE ? OR content LIKE ? LIMIT ?", (pat, pat, top_k))
        rows = cur.fetchall()
        return [(r['title'], r['content']) for r in rows]

# -- Semantic search helpers -------------------------------------------------
def _ensure_model():
    global _model
    if _model is None:
        if SentenceTransformer is None:
            raise RuntimeError("sentence-transformers not installed. Install it to use semantic search.")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def semantic_search(query: str, top_k=3):
    """Semantic search: uses FAISS if available; otherwise uses numpy+nearest neighbor fallback."""
    conn = connect_db()
    cur = conn.cursor()

    # If FAISS index exists, use it
    if _have_faiss and os.path.exists(FAISS_INDEX_PATH):
        model = _ensure_model()
        q_emb = model.encode([query], convert_to_numpy=True)
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
        index = faiss.read_index(FAISS_INDEX_PATH)
        D, I = index.search(q_emb, top_k)

        # Get IDs from DB instead of JSON
        cur.execute("SELECT id FROM documents ORDER BY id ASC")
        ids = [row["id"] for row in cur.fetchall()]

        results = []
        for idx in I[0]:
            if idx < 0:
                continue
            doc_id = ids[idx]
            cur.execute("SELECT title, content FROM documents WHERE id=?", (doc_id,))
            r = cur.fetchone()
            if r:
                results.append((r["title"], r["content"]))
        return results

    # fallback: numpy + sklearn nearest neighbors if embeddings saved
    if os.path.exists(EMB_PATH):
        model = _ensure_model()
        q_emb = model.encode([query], convert_to_numpy=True)
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
        embeddings = np.load(EMB_PATH)

        sims = embeddings.dot(q_emb.T).squeeze()
        top_idx = np.argsort(sims)[::-1][:top_k]

        # Get IDs from DB instead of JSON
        cur.execute("SELECT id FROM documents ORDER BY id ASC")
        ids = [row["id"] for row in cur.fetchall()]

        results = []
        for i in top_idx:
            doc_id = ids[int(i)]
            cur.execute("SELECT title, content FROM documents WHERE id=?", (doc_id,))
            r = cur.fetchone()
            if r:
                results.append((r["title"], r["content"]))
        return results

    return []

def search_similar_documents(query: str, top_k=3):
    """
    Top-level search used by legal_llm:
      1) explicit title/section match
      2) FTS keyword search
      3) semantic search (FAISS or numpy fallback)
    Returns list of "title: content" strings (or empty list).
    """
    exact = title_match(query, max_results=5)
    if exact:
        return [f"{t}: {c}" for t, c in exact]

    fts_res = fts_search(query, top_k=top_k)
    if fts_res:
        return [f"{t}: {c}" for t, c in fts_res]

    sem = semantic_search(query, top_k=top_k)
    if sem:
        return [f"{t}: {c}" for t, c in sem]

    return []
