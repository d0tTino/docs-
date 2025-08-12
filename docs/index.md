---
title: "Tino Docs Hub"
tags: [docs]
project: docs-hub
updated: 2025-07-29
---

# Tino Docs Hub

**Abstract:** The Tino Docs Hub employs a modular architecture built on MkDocs with Git submodules to centralize project documentation. Pre-commit hooks, helper scripts, and clear directory conventions standardize contributions and workflows. This methodology streamlines ingestion and browsing while preserving versioned histories. The hub ultimately enhances collaboration and ensures research artifacts remain accessible and maintainable.

This repository aggregates documentation and research across multiple projects.

## Table of Contents

- [Quickstart](quickstart.md)
- [Directory Structure](#directory-structure)
- [Research Docs](#research-docs)
- [Project Documentation Submodules](#project-documentation-submodules)
- [After Cloning](#after-cloning)
- [Building the Docs](#building-the-docs)
- [Setting Up Git Hooks](#setting-up-git-hooks)
- [Invoking the Migration Script](#invoking-the-migration-script)
- [Ingesting and Querying Markdown](#ingesting-and-querying-markdown)
- [Legal](#legal)
- [References](#references)
## Directory Structure

![Site Map](img/site-map.svg)

- `ai-research/` – AI and machine learning notes
- `arduino/` – hardware and firmware references
- `terminal-workflow/` – command-line tips and workflows
- `culture-project/` – organizational culture project
- `_project-docs/` – submodule mounts for individual projects
- `scripts/` – helper scripts including ingest utilities
- `playbooks/` – workflow and container playbooks
- [`security/threat-model.md`](security/threat-model.md) – threat model for docs and scripts

## Research Docs

Explore focused research collections:

- [AI Research](ai-research/index.md) – design notes and technical dossiers for ongoing experiments.
- [Non-AI Research](non-ai-research/index.md) – cross-disciplinary investigations outside the AI domain.

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
git submodule update --remote --recursive
```

Alternatively run the helper script:

```bash
scripts/bulk_submodule_update.sh
```

## After Cloning

Set up Git LFS and repository hooks after cloning:

```bash
git lfs install
scripts/setup_hooks.sh
```

The hooks enforce Markdown and Python linting via the `.githooks/pre-commit` script,
which runs `markdownlint-cli` and `flake8`.

## Building the Docs

Install Python packages from `requirements.txt` to ensure all dependencies (MkDocs,
pytest, flake8) install consistently, then launch the dev server using the commands in the [Quickstart](quickstart.md) guide.

Visit the local server at <http://127.0.0.1:8000> to preview the site locally. For portable options, see the [MkDocs preview instructions](https://www.mkdocs.org/user-guide/deploying-your-docs/#preview-your-site).

The site automatically deploys via GitHub Actions whenever you push updates to Markdown files or `mkdocs.yml`.

## Setting Up Git Hooks

Configure git to use the repository's hooks by running the helper script:

```bash
scripts/setup_hooks.sh
```

## Invoking the Migration Script

You can import configuration and prompt snippets from the old
[`d0tTino/d0tTino`](https://github.com/d0tTino/d0tTino) repository. Ensure
`git-filter-repo` is installed (for example via `pip install git-filter-repo` or
your package manager) before running the script.

Run the migration script from the repository root:

```bash
scripts/migrate_old_docs.sh
```

The script clones the legacy repo, filters only the documentation files using
`git filter-repo`, and fetches the result as a local branch called
`d0tTino-import`. Merge that branch to incorporate the history:

```bash
git merge d0tTino-import --allow-unrelated-histories
```

## Ingesting and Querying Markdown

The `scripts/ingest.py` helper can store markdown chunks in a simple
vector database and retrieve them later:

```bash
# Build the database
python scripts/ingest.py docs/example.md --db vector_db.pkl

# Query for similar text
python - <<'EOF'
from pathlib import Path
from scripts.ingest import VectorDB
db = VectorDB(Path('vector_db.pkl'))
print(db.query('search text'))
EOF
```

## Legal

This documentation is provided for informational purposes and comes with no
warranty. See the [LICENSE](../LICENSE) for terms and standard disclaimers.

## References

### Legal cases
1. *Riley v. California*, 573 U.S. 373 (2014).
2. *Van Buren v. United States*, 593 U.S. 674 (2021).

### APIs
1. GitHub REST API v3 documentation – https://docs.github.com/en/rest
2. OpenAI API reference – https://platform.openai.com/docs/api-reference

### Publications
1. Shoshana Zuboff, *The Age of Surveillance Capitalism* (PublicAffairs, 2019).
2. James Bridle, *New Dark Age: Technology and the End of the Future* (Verso, 2018).
