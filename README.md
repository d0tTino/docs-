# Tino Docs Hub

Central hub for project documentation and research across Tino initiatives.

**Abstract:** The Tino Docs Hub employs a modular architecture built on MkDocs with
Git submodules to centralize project documentation. Pre-commit hooks, helper
scripts, and clear directory conventions standardize contributions and
workflows. This methodology streamlines ingestion and browsing while preserving
versioned histories. The hub ultimately enhances collaboration and ensures
research artifacts remain accessible and maintainable.

This repository aggregates documentation and research across multiple projects.

For setup instructions, directory overview, and detailed research listings, see
[docs/index.md](docs/index.md). For a quick start, read the [Quickstart
guide](docs/quickstart.md) and review the [documentation threat
model](docs/security/threat-model.md).

## Development

### Pre-commit

Install [pre-commit](https://pre-commit.com/) hooks to automatically expand snippets and lint Markdown files:

```bash
pip install pre-commit
pre-commit install
```

Run `npm run preexpand <file>` to manually expand `--8<--` markers when needed.

The hook runs `scripts/expand_snippets.py` to inline snippet references and
`scripts/lint_research_docs.py` to catch mid-word line splits.

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

## Contributing

1. Create a branch from `main` for your work.
2. Run `scripts/setup_hooks.sh` to install Git hooks and linters.
3. Commit your changes and open a Pull Request for review.

## Resources

- [Documentation](docs/index.md)
- [Issue Tracker](../../issues)
- [Community Discussions](../../discussions)

