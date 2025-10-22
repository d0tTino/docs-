---
title: "Tino Docs Hub"
tags: [docs]
project: docs-hub
updated: 2025-07-29
---

--8<-- "_snippets/disclaimer.md"

# Tino Docs Hub

**Abstract:** The Tino Docs Hub centralizes project documentation with MkDocs and Git submodules,
aggregating research across multiple projects. Pre-commit hooks, helper scripts, and consistent
directory conventions keep artifacts easy to browse and maintain.

## Quick Links

Access the most frequently used resources at a glance.

- 🚀 **Getting Started**
  - [Quickstart Guide](quickstart.md)
  - [Threat Model](security/threat-model.md)

- 📚 **Research**
  - [AI Research Hub](ai-research/index.md)
  - [Non-AI Research Hub](non-ai-research/index.md)
  - [Gaze Research Overview](gaze-research/index.md)
  - [Security Guidance](security/index.md)

- ⚙️ **Playbooks**
  - [Terminal Workflow Playbook](terminal-workflow/index.md)
  - [GitHub Actions Workflows](playbooks/github-actions-workflows.md)
  - [Local Docker Build Guide](playbooks/local-docker-build.md)

## Getting Started
Guides for setting up the docs hub and exploring resources.

!!! info "Get Started"
    Build the docs with the [Quickstart guide](quickstart.md).

- Review the [threat model](security/threat-model.md) for security considerations.
- Explore [research docs](#research-docs).

For contribution guidelines, see the [Contributing section](https://github.com/d0tTino/docs-/blob/main/README.md#contributing) of the main
README.
## Directory Structure
Overview of key directories and their purposes.

![Site map diagram illustrating the flow from the landing page through section directories and project submodules](img/site-map.svg)

*Figure: Documentation flow showing relationships between the landing page, section directories, and project submodules.*

| Location | Description |
| --- | --- |
| `ai-research/` | AI and machine learning notes (e.g., transformer experiments) |
| `non-ai-research/` | Research outside the AI domain (e.g., cognitive science reviews) |
| `arduino/` | Hardware and firmware references (e.g., microcontroller pinouts) |
| `terminal-workflow/` | Command-line tips and workflows (e.g., alias bundles) |
| `culture-project/` | Organizational culture project (e.g., case studies) |
| `_project-docs/` | Submodule mounts for individual projects (e.g., docs for internal tools) |
| `scripts/` | Helper scripts including ingest utilities (e.g., `ingest.py`) |
| `playbooks/` | Workflow and container playbooks (e.g., dev container setups) |
| `img/` | Static images used across docs (e.g., site map diagram) |
| `security/` | Security guidelines and threat models (e.g., `threat-model.md`) |

## Research Docs
Highlights the main research categories, including AI, non-AI, gaze, and security topics.

### Research Highlights

- [AI Research](ai-research/index.md) – design notes and technical dossiers for ongoing experiments.
- [Non-AI Research](non-ai-research/index.md) – cross-disciplinary investigations outside the AI domain.
- [Gaze Research](gaze-research/index.md) – analyses on gaze tracking and related methodologies.
- [Security](security/index.md) – threat models and guidance on secure development practices.

## Project Documentation Submodules
Explains how to manage project-specific documentation with git submodules.

Project documentation lives in separate repositories added to `_project-docs/` as git submodules.
Add a new project by running:

```bash
git submodule add <repository-url> _project-docs/<project-folder>
```

After cloning the docs hub or when new submodules are added, initialize them with:

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
Steps to configure tools and hooks immediately after cloning the repository.

Enable Git LFS for large assets, configure Git to use the repository's hook directory, and install the standard `pre-commit` hooks:

```bash
git lfs install
scripts/setup_hooks.sh
npm install  # requires Node 18+
pip install pre-commit  # or use `py -m pip install pre-commit` on Windows
pre-commit install
```

The hook setup configures both the `.githooks/pre-commit` path and the `pre-commit` managed hooks so that Markdownlint,
flake8, and other checks run automatically before each commit.

## Building the Docs
Instructions for installing dependencies and previewing the documentation site.

Install Python packages from `requirements.txt` to ensure all dependencies (MkDocs, pytest, flake8)
install consistently, then launch the dev server using the commands in the
[Quickstart](quickstart.md) guide.

Visit the local server at <http://127.0.0.1:8000> to preview the site locally. For portable options,
see the [MkDocs preview instructions][mkdocs-preview].

The site automatically deploys via GitHub Actions whenever you push updates to Markdown files or
`mkdocs.yml`.

[mkdocs-preview]:
  https://www.mkdocs.org/user-guide/deploying-your-docs/#preview-your-site

## Invoking the Migration Script
Procedure for importing legacy documentation using the migration script.

You can import configuration and prompt snippets from the old
[`d0tTino/d0tTino`](https://github.com/d0tTino/d0tTino) repository. Ensure `git-filter-repo` is
installed (for example via `pip install git-filter-repo` or your package manager) before running the
script.

Run the migration script from the repository root:

```bash
scripts/migrate_old_docs.sh
```

The script clones the legacy repo, filters only the documentation files using `git filter-repo`, and
fetches the result as a local branch called `d0tTino-import`. Merge that branch to incorporate the
history:

```bash
git merge d0tTino-import --allow-unrelated-histories
```

## Appendix A: Resource Checklist

Refer to the [Quick Links](#quick-links) grid above for the consolidated Getting Started, Research, and Playbooks resources.

## Ingesting and Querying Markdown
Use the ingestion utility to store and search markdown snippets from existing guides.

For example, the `scripts/ingest.py` helper can store chunks from `docs/quickstart.md` in a simple
vector database and retrieve them later:

!!! note "Install script dependencies"
    Install the Python requirements first (e.g., `pip install -r requirements.txt`) so `scripts/ingest.py`
    can import its dependencies; see the [Quickstart guide](quickstart.md) for the full setup.

```bash
# Build the database
python scripts/ingest.py docs/quickstart.md --db vector_db.pkl

# Query for similar text
python - <<'EOF'
from pathlib import Path
from scripts.ingest import VectorDB
db = VectorDB(Path('vector_db.pkl'))
print(db.query('search text'))
EOF
```

## Legal
Outlines licensing terms and disclaimers.

This documentation is provided for informational purposes and comes with no warranty. See the
[LICENSE](https://github.com/d0tTino/docs-/blob/main/LICENSE) for terms and standard disclaimers.

## References
Citations for cases, APIs, and publications referenced in the docs.

### Legal cases
1. *Riley v. California*, 573 U.S. 373 (2014).
2. *Van Buren v. United States*, 593 U.S. 674 (2021).

### APIs
1. GitHub REST API v3 documentation – https://docs.github.com/en/rest
2. OpenAI API reference – https://platform.openai.com/docs/api-reference

### Publications
1. Shoshana Zuboff, *The Age of Surveillance Capitalism* (PublicAffairs, 2019).
2. James Bridle, *New Dark Age: Technology and the End of the Future* (Verso, 2018).

## Summary & Further Study

**Workflow recap.** Clone the repository, initialize or update submodules, and run
`scripts/setup_hooks.sh` to enable linting hooks. Install Python dependencies,
start the MkDocs development server to preview changes locally, and leverage the
migration and ingestion scripts when you need to pull legacy materials into the
hub.

**Top external resources.** Continue exploring the MkDocs
[preview guide][mkdocs-preview] for deployment patterns, review the GitHub REST
API documentation for automation ideas, and consult the OpenAI API reference to
integrate AI-assisted tooling into your workflows.
