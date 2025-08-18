# Tino Docs Hub

[![Build Status](https://github.com/d0tTino/docs-/actions/workflows/tests.yml/badge.svg)](https://github.com/d0tTino/docs-/actions/workflows/tests.yml) [![License](https://img.shields.io/github/license/d0tTino/docs-)](LICENSE)

Central hub for project documentation and research across Tino initiatives.

**Abstract:** The Tino Docs Hub employs a modular architecture built on MkDocs
with Git submodules to centralize project documentation. Pre-commit hooks,
helper scripts, and clear directory conventions standardize contributions and
workflows. This methodology streamlines ingestion and browsing while preserving
versioned histories. The hub ultimately enhances collaboration and ensures
research artifacts remain accessible and maintainable.

![Repository site map showing documentation flow](docs/img/site-map.svg)

This repository aggregates documentation and research across multiple projects.

For setup instructions, directory overview, and detailed research listings,
see [docs/index.md](docs/index.md). For a quick start, read the [Quickstart
guide](docs/quickstart.md) and review the [documentation threat
model](docs/security/threat-model.md).

## Table of Contents

- [Development](#development)
  - [Pre-commit](#pre-commit)
  - [Preview Docs Locally](#preview-docs-locally)
  - [Update Submodules](#update-submodules)
  - [Update Research Indexes](#update-research-indexes)
- [Contributing](#contributing)
- [Resources](#resources)

## Development

### Pre-commit

Install [pre-commit](https://pre-commit.com/) hooks to automatically expand
snippets and lint Markdown files:

```bash
pip install pre-commit
pre-commit install
```

Run `npm run preexpand <file>` to manually expand `--8<--` markers when
needed.

The hook runs `scripts/expand_snippets.py` to inline snippet references and
`scripts/lint_research_docs.py` to catch mid-word line splits.

### Preview Docs Locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Install Python dependencies and serve the docs at
<http://127.0.0.1:8000>.

### Update Submodules

```bash
git submodule update --init --recursive
```

Fetch documentation submodules to ensure project docs are available.

### Update Research Indexes

Rebuild research index pages after adding or renaming documents:

```bash
python scripts/update_ai_research_index.py
python scripts/update_non_ai_research_index.py
```

## Contributing

1. Create a branch from `main` for your work.
2. Run `scripts/setup_hooks.sh` to install Git hooks and linters.
3. Commit your changes and open a Pull Request for review.

## Resources

- [Documentation](docs/index.md)
- [Issue Tracker](../../issues)
- [Community Discussions](../../discussions)

