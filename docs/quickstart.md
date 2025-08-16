---
title: "Quickstart"
tags: [docs]
project: docs-hub
updated: 2025-08-13
---

--8<-- "_snippets/disclaimer.md"

# Quickstart

## Set Up Git LFS and pre-commit

Initialize large-file support and install the local hooks:

```bash
git lfs install
pip install pre-commit
pre-commit install
```

## Run the Docs Locally

```bash
pip install -r requirements.txt
npm install
mkdocs serve
```

Then visit the local server at <http://127.0.0.1:8000> to preview the site
locally.

## Build the Static Site

Generate a local build to check for broken links or other issues:

```bash
mkdocs build
```

## Troubleshooting

### Environment Issues

- `mkdocs: command not found` – install it with `pip install mkdocs`.
- `npm: command not found` – ensure Node.js is installed.
- Port 8000 already in use – stop the other process or run `mkdocs serve -a
  127.0.0.1:8001`.

### Common MkDocs Build Errors

- `ModuleNotFoundError: No module named 'mkdocs_material'` – install the
  missing theme with `pip install mkdocs-material`.
- `yaml.parser.ParserError` – check `mkdocs.yml` for indentation or syntax
  issues.
- `ERROR   -  Config file 'mkdocs.yml' does not exist` – run `mkdocs` from the
  repository root or specify the file with `-f`.

