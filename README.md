# Tino Docs Hub

This repository aggregates documentation and research across multiple projects.

## Directory Structure

- `ai-research/` – AI and machine learning notes
- `arduino/` – hardware and firmware references
- `terminal-workflow/` – command-line tips and workflows
- `culture-project/` – organizational culture project
- `_project-docs/` – submodule mounts for individual projects
- `scripts/` – helper scripts including ingest utilities

## Building the Docs

Install dependencies and build the site with [MkDocs](https://www.mkdocs.org/):

```bash
pip install mkdocs mkdocs-material mkdocs-monorepo-plugin
mkdocs serve
```

The site is deployed via GitHub Actions on every push that modifies docs.
