---
title: "Tino Docs Hub"
tags: [docs]
project: docs-hub
updated: 2025-07-29
---

--8<-- "_snippets/disclaimer.md"

# Tino Docs Hub

**Abstract:** The Tino Docs Hub centralizes project documentation with MkDocs and Git submodules. Pre-commit hooks, helper scripts, and consistent directory conventions streamline contributions, keeping research artifacts easy to browse and maintain.

This repository aggregates documentation and research across multiple projects.

## Getting Started

!!! info "Get Started"
    Build the docs with the [Quickstart guide](quickstart.md).

- Review the [threat model](security/threat-model.md) for security
  considerations.
- Explore [research docs](#research-docs).

For contribution guidelines, see the [Contributing section](../README.md#contributing) of the main README.

## Table of Contents

- **Getting Started**
  - [Quickstart](quickstart.md)
  - [Directory Structure](#directory-structure)
  - [After Cloning](#after-cloning)
  - [Building the Docs](#building-the-docs)
  - [Setting Up Git Hooks](#setting-up-git-hooks)
- **Projects and Research**
  - [Research Docs](#research-docs)
  - [Project Documentation Submodules](#project-documentation-submodules)
- **Utilities**
  - [Invoking the Migration Script](#invoking-the-migration-script)
  - [Ingesting and Querying Markdown](#ingesting-and-querying-markdown)
- **Reference & Legal**
  - [Legal](#legal)
  - [References](#references)
## Directory Structure

![Site Map](img/site-map.svg)

| Location | Description | Example |
| --- | --- | --- |
| `ai-research/` | AI and machine learning notes | transformer experiments |
| `non-ai-research/` | Research outside the AI domain | cognitive science reviews |
| `arduino/` | Hardware and firmware references | microcontroller pinouts |
| `terminal-workflow/` | Command-line tips and workflows | alias bundles |
| `culture-project/` | Organizational culture project | case studies |
| `_project-docs/` | Submodule mounts for individual projects | docs for internal tools |
| `scripts/` | Helper scripts including ingest utilities | `ingest.py` |
| `playbooks/` | Workflow and container playbooks | dev container setups |
| `img/` | Static images used across docs | site map diagram |
| `security/` | Security guidelines and threat models | `threat-model.md` |

## Research Docs

### Research Highlights

- [AI Research](ai-research/) – design notes and technical dossiers for ongoing experiments.
- [Non-AI Research](non-ai-research/) – cross-disciplinary investigations outside the AI domain.
- [Gaze Research](gaze-research/) – analyses on gaze tracking and related methodologies.
- [Security](security/) – threat models and guidance on secure development practices.

## Project Documentation Submodules

Project documentation lives in separate repositories added to `_project-docs/`
as git submodules. Add a new project by running:

```bash
git submodule add <repository-url> _project-docs/<project-folder>
```

After cloning the docs hub or when new submodules are added, initialize them
with:

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

The hooks enforce Markdown and Python linting via the `.githooks/pre-commit`
script, which runs `markdownlint-cli` and `flake8`.

## Building the Docs

Install Python packages from `requirements.txt` to ensure all dependencies
(MkDocs, pytest, flake8) install consistently, then launch the dev server using
the commands in the [Quickstart](quickstart.md) guide.

Visit the local server at <http://127.0.0.1:8000> to preview the site locally.
For portable options, see the [MkDocs preview instructions][mkdocs-preview].

The site automatically deploys via GitHub Actions whenever you push updates to
Markdown files or `mkdocs.yml`.

[mkdocs-preview]:
  https://www.mkdocs.org/user-guide/deploying-your-docs/#preview-your-site

## Setting Up Git Hooks

Configure git to use the repository's hooks by running the helper script:

```bash
scripts/setup_hooks.sh
```

## Invoking the Migration Script

You can import configuration and prompt snippets from the old
[`d0tTino/d0tTino`](https://github.com/d0tTino/d0tTino) repository. Ensure `git-
filter-repo` is installed (for example via `pip install git-filter-repo` or your
package manager) before running the script.

Run the migration script from the repository root:

```bash
scripts/migrate_old_docs.sh
```

The script clones the legacy repo, filters only the documentation files using
`git filter-repo`, and fetches the result as a local branch called `d0tTino-
import`. Merge that branch to incorporate the history:

```bash
git merge d0tTino-import --allow-unrelated-histories
```

## Ingesting and Querying Markdown

The `scripts/ingest.py` helper can store markdown chunks in a simple vector
database and retrieve them later:

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
2. James Bridle, *New Dark Age: Technology and the End of the Future* (Verso,
   2018).
