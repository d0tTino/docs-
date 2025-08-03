# Versioning API

The document service supports optimistic concurrency control. Updating a
revision with a `base_version` that differs from the latest version returns
`409 Conflict` with a unified diff and metadata describing conflicting line
ranges:

```json
{
  "diff": "...",
  "latest": 3,
  "conflicts": [
    {"base": [1,2], "incoming": [1,2], "current": [1,2]}
  ]
}
```

After resolving the conflicts locally, submit the merged content using
`POST /docs/{doc_id}/resolve`:

```bash
curl -X POST /docs/mydoc/resolve \
  -H "Authorization: Bearer <token>" \
  -d '{
        "content": "final text",
        "author_id": "agent1",
        "summary": "merge",
        "base_version": 3
      }'
```

If `base_version` is stale the same conflict structure is returned. A
successful call creates a new revision and dispatches the usual notifications.

## Python Client

Use the bundled ``DocsClient`` for authenticated interactions with the API:

```python
from versioning.client import DocsClient

client = DocsClient("http://localhost:8000", token="secrettoken")
client.create_comment("doc1", "L1", "user1", "Nice!", correlation_id="c-1")
client.update_document(
    "doc1", " more text", author_id="agent1", summary="edit", correlation_id="c-2"
)
```
