#!/usr/bin/env python3
# create_sqlite_db.py
import sqlite3
import json
import os
import sys
from pathlib import Path
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[0]  # current folder
DATA_DIR = PROJECT_ROOT / "data"
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = DATA_DIR / "legal_docs.db"

# -------- Extraction Helpers --------
def _collect_text(node):
    """Recursively collect textual content from dict/list/str nodes."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node.strip()
    if isinstance(node, dict):
        parts = []
        for k, v in node.items():
            txt = _collect_text(v)
            if txt:
                parts.append(txt)
        return "\n".join(parts)
    if isinstance(node, list):
        return "\n".join([_collect_text(x) for x in node])
    return str(node)

def extract_title_and_content(item):
    """Try to guess title and content from various JSON shapes."""
    title = item.get("title") or item.get("ArtNo") or item.get("Name") \
        or item.get("Article") or item.get("Section")

    content = item.get("content") or item.get("ArtDesc") \
        or item.get("ClauseDesc") or item.get("Clause")

    # If no title, try combining known keys
    if not title:
        if item.get("ArtNo") and item.get("Name"):
            title = f"Article {item['ArtNo']} - {item['Name']}"
        elif item.get("Section") and item.get("Name"):
            title = f"Section {item['Section']} - {item['Name']}"
        else:
            title = str(item)[:80]

    # Flatten lists
    if isinstance(content, list):
        content = "\n".join(map(str, content))

    if not content:
        content = _collect_text(item)

    return title.strip(), content.strip()

# -------- Load & Parse JSONs --------
def load_all_json_entries():
    entries = []
    for json_file in DATA_DIR.glob("*.json"):
        print(f"📄 Loading {json_file.name} ...")
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ Skipping {json_file.name} (read error: {e})")
            continue

        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    entries.append({"title": k, "content": v, "source": json_file.name})
                elif isinstance(v, dict):
                    t = v.get("title") or k
                    c = v.get("content") or _collect_text(v)
                    entries.append({"title": t, "content": c, "source": json_file.name})
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    t, c = extract_title_and_content(item)
                    entries.append({"title": t, "content": c, "source": json_file.name})
        else:
            print(f"⚠️ Unsupported JSON format in {json_file.name}")
    return entries

# -------- Database Creation --------
def create_db(db_path):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            source TEXT
        )
    """)
    try:
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(title, content, content='documents', content_rowid='id')")
        conn.commit()
        fts_enabled = True
    except sqlite3.OperationalError:
        print("⚠️ FTS5 not available, will use LIKE queries instead.")
        fts_enabled = False
    return conn, fts_enabled

def ingest_entries(conn, entries, fts_enabled):
    cur = conn.cursor()
    cur.execute("DELETE FROM documents")
    if fts_enabled:
        cur.execute("DELETE FROM documents_fts")
    conn.commit()

    for e in tqdm(entries, desc="Inserting entries"):
        t, c, s = e.get("title", "").strip(), e.get("content", "").strip(), e.get("source", "json")
        cur.execute("INSERT INTO documents (title, content, source) VALUES (?, ?, ?)", (t, c, s))
        rowid = cur.lastrowid
        if fts_enabled:
            cur.execute("INSERT INTO documents_fts(rowid, title, content) VALUES (?, ?, ?)", (rowid, t, c))
    conn.commit()

def main():
    entries = load_all_json_entries()
    print(f"✅ Loaded {len(entries)} entries from {DATA_DIR}")
    if not entries:
        print("❌ No entries found. Place your legal JSON files in the 'data' folder.")
        sys.exit(1)
    conn, fts_enabled = create_db(DB_PATH)
    ingest_entries(conn, entries, fts_enabled)
    conn.close()
    print(f"📂 Database created at {DB_PATH}")

if __name__ == "__main__":
    main()
