from __future__ import annotations

from typing import List, Dict

from .store import RevisionStore
from comments.store import CommentStore


def render_document(
    doc_id: str, rev_store: RevisionStore, comment_store: CommentStore
) -> Dict[str, str | List[Dict]]:
    """Return document content with comment anchors."""
    content = rev_store._latest_content(doc_id)
    comments = comment_store.list_comments(doc_id)
    lines = content.splitlines()
    for c in comments:
        ref = c["section_ref"]
        unresolved = c.get("status") != "resolved"
        anchor = f"[comment:{c['comment_id']}{'!' if unresolved else ''}]"
        c["unresolved"] = unresolved
        if ref.startswith("L"):
            try:
                _, end = ref[1:].split("-")
                idx = int(end)
                lines.insert(idx, anchor)
                continue
            except Exception:  # pragma: no cover - best effort
                pass
        for i, line in enumerate(lines):
            if line.strip() == ref.strip():
                lines.insert(i + 1, anchor)
                break
        else:
            lines.append(anchor)
    rendered = "\n".join(lines)
    return {"content": rendered, "comments": comments}
