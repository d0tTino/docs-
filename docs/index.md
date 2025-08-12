---
title: "Tino Docs Hub"
tags: [docs]
project: docs-hub
updated: 2025-07-29
---

# Tino Docs Hub

This repository aggregates documentation and research across multiple projects.

## Quickstart

```bash
pip install -r requirements.txt
mkdocs serve
```
Then visit the local server at <http://127.0.0.1:8000> to preview the site locally.

## Directory Structure

- `ai-research/` – AI and machine learning notes
- `arduino/` – hardware and firmware references
- `terminal-workflow/` – command-line tips and workflows
- `culture-project/` – organizational culture project
- `_project-docs/` – submodule mounts for individual projects
- `scripts/` – helper scripts including ingest utilities
- `playbooks/` – workflow and container playbooks
- [`security/threat-model.md`](security/threat-model.md) – threat model for docs and scripts

## Research Docs

The `ai-research/` folder collects design notes and technical dossiers for
ongoing experiments. Key documents include:

- [Strategic R&D Roadmap for DeepThought-ReThought](ai-research/strategic-roadmap-deepthought.md)
- [Reverse-Engineering OpenAI Codex](ai-research/reverse-engineering-codex.md)
- [Reverse-Engineering Design Report: OpenAI ChatGPT Agent System](ai-research/reverse-engineering-chatgpt-agent-system.md)
- [Seed-Factory Feasibility Dossier](ai-research/seed-factory-feasibility-dossier.md)
- [Agentic SWE Discontinuity Forecast](ai-research/agentic-swe-discontinuity-forecast.md)
- [Energy-Efficient Swarm](ai-research/energy-efficient-swarm.md)
- [Neurosymbolic Reasoning Dossier](ai-research/neurosymbolic-reasoning-dossier.md)
- [Friend or Foe PRD](ai-research/discord-friend-foe-prd.md)
- [Logical Chunking Strategies](ai-research/logical-chunking.md)
- [Peaks and Freezes](ai-research/peaks-and-freezes.md)
- [Thick Band of 21st-Century Possibilities](ai-research/thick-band-of-21st-century-possibilities.md)
- [You Weren't Supposed to Invent Infinite Jest](ai-research/you-werent-supposed-to-invent-infinite-jest.md)

See [ai-research/index.md](ai-research/index.md) for additional context and any
newly added reports.

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
pytest, flake8) install consistently, then launch the dev server:

```bash
pip install -r requirements.txt
mkdocs serve
```

Visit the local server at <http://127.0.0.1:8000> to preview the site locally. For portable options, see the [MkDocs preview instructions](https://www.mkdocs.org/user-guide/deploying-your-docs/#preview-your-site).

The site automatically deploys via GitHub Actions whenever you push updates to Markdown files or `mkdocs.yml`.

## Installing Node Dependencies

Install Node packages for optional tooling such as markdown linting:

```bash
npm install
```

This installs development dependencies defined in `package.json`, such as `markdownlint-cli` for linting.

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
