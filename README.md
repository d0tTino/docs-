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

## After Cloning

Set up Git LFS and repository hooks after cloning:

```bash
git lfs install
scripts/setup_hooks.sh
```

The hooks enforce Markdown linting with `pre-commit`.

## Building the Docs

Install Python packages and build the site with [MkDocs](https://www.mkdocs.org/):

```bash
pip install mkdocs mkdocs-material mkdocs-monorepo-plugin
mkdocs serve
```

The site is deployed via GitHub Actions on every push that modifies docs.

## Installing Node Dependencies

Install Node packages for optional tooling such as markdown linting:

```bash
npm install
```

This installs development dependencies defined in `package.json`.

## Setting Up Git Hooks

Configure git to use the repository's hooks by running the helper script:

```bash
scripts/setup_hooks.sh
```

## Invoking the Migration Script

You can import configuration and prompt snippets from the old
[`d0tTino/d0tTino`](https://github.com/d0tTino/d0tTino) repository.
Ensure `git-filter-repo` is installed (for example via `pip install git-filter-repo` or your package manager) before running the script.

Run the migration script from the repository root:

```bash
scripts/migrate_old_docs.sh
```

The script clones the legacy repo, filters only the documentation
files using `git filter-repo`, and fetches the result as a local branch
called `d0tTino-import`. Merge that branch to incorporate the history:

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
