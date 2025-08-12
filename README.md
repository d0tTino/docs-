# Tino Docs Hub

This repository aggregates documentation and research across multiple projects.

For setup instructions, directory overview, and detailed research listings, see [docs/index.md](docs/index.md).

## Development

Install [pre-commit](https://pre-commit.com/) hooks to automatically lint Markdown files:

```bash
pip install pre-commit
pre-commit install
```

The hook runs `scripts/lint_research_docs.py` to catch mid-word line splits.

### Preview Docs Locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Install Python dependencies and serve the docs at <http://127.0.0.1:8000>.

### Update Submodules

```bash
git submodule update --init --recursive
```

Fetch documentation submodules to ensure project docs are available.

