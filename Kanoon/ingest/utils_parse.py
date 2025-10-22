# utils_parse.py
from typing import List, Tuple, Any

def _collect_text(node: Any) -> str:
    """Recursively collect textual fields from dict/list/str nodes."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node.strip()
    if isinstance(node, dict):
        parts = []
        for k, v in node.items():
            # skip metadata keys that are empty
            if isinstance(v, (dict, list, str)):
                txt = _collect_text(v)
                if txt:
                    parts.append(f"{k}: {txt}" if k.lower() in ("artdesc", "artdesc", "artdesc") else txt)
        return "\n".join([p for p in parts if p])
    if isinstance(node, list):
        return "\n".join([_collect_text(item) for item in node if item])
    return str(node)

def extract_documents_from_json(obj: Any, source="unknown") -> List[Tuple[str, str]]:
    """
    Return list of (title, content) extracted from JSON object.
    Works for COI.json and common IPC JSON shapes.
    """
    docs = []

    # If top-level is a list of articles (COI-like)
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                # common keys
                title = item.get("ArtNo") or item.get("title") or item.get("Section") or item.get("section") or item.get("name")
                name = item.get("Name") or item.get("title") or item.get("name")
                # prefer combined title
                full_title = None
                if name and title:
                    full_title = f"{name} ({title})"
                elif name:
                    full_title = name
                elif title:
                    full_title = str(title)
                else:
                    # fallback: maybe this is a nested list (e.g., parts list)
                    full_title = item.get("title", f"{source}-item")

                # collect description
                desc = item.get("ArtDesc") or item.get("content") or item.get("ClauseDesc") or item.get("description") or item.get("section_text")
                if not desc:
                    # flatten whole dict
                    desc = _collect_text(item)
                if desc and full_title:
                    docs.append((full_title, desc))
    # If top-level is dict keyed by section numbers
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                docs.append((k, v))
            else:
                text = _collect_text(v)
                docs.append((str(k), text))
    return docs
