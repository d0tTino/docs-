# Tino Docs Hub

This repository aggregates documentation and research across multiple projects.

## Directory Structure

- `ai-research/` – AI and machine learning notes
- `arduino/` – hardware and firmware references
- `terminal-workflow/` – command-line tips and workflows
- `culture-project/` – organizational culture project
- `_project-docs/` – submodule mounts for individual projects
- `scripts/` – helper scripts including ingest utilities

## Project Documentation Submodules

Project documentation lives in separate repositories added to
`_project-docs/` as git submodules. Add a new project by running:

```bash
git submodule add <repository-url> _project-docs/<project-folder>
```

After cloning the docs hub or when new submodules are added, initialize
them with:

```bash
git submodule update --init --recursive
```

To fetch updates from all submodules later on, run:

```bash
git submodule update --remote
```

## Building the Docs

Install dependencies and build the site with [MkDocs](https://www.mkdocs.org/):

```bash
pip install mkdocs mkdocs-material mkdocs-monorepo-plugin
mkdocs serve
```

The site is deployed via GitHub Actions on every push that modifies docs.

## Development Setup

Configure git to use the repository's hooks:

```bash
scripts/setup_hooks.sh
```
