---
title: "GitHub Actions Workflows"
tags: [ci, automation, workflows]
project: docs-hub
updated: 2025-02-21
---

--8<-- "_snippets/disclaimer.md"

# GitHub Actions Workflows

This playbook summarizes the automated workflows that run in this repository.

```mermaid
flowchart LR
    B[Build] --> T[Test]
    T --> D[Deploy]
```

*Figure: Build, test, and deploy stages.*

## Docs Deployment

- Defined in `.github/workflows/docs.yml`.
- Builds the MkDocs site and deploys it to GitHub Pages on every push that updates markdown files.

## Linting

- `markdownlint.yml` checks all Markdown files using `markdownlint-cli`.
- `python-lint.yml` runs `flake8` against Python sources.

## Docs Lint

- `docs-lint.yml` runs `markdownlint` on the `docs/` directory when related files change.
- Installs repository Python requirements and executes `scripts/lint_research_docs.py` for additional checks.

## Pre-commit

- `pre-commit.yml` triggers on Markdown and `.pre-commit-config.yml` updates to enforce pre-commit hooks.
- Uses the official `pre-commit` GitHub Action with Python 3.x to run the configured hooks.

## Tests

- `tests.yml` executes the test suite with `pytest` when Python files change.

These workflows keep the documentation site and helper scripts healthy.
