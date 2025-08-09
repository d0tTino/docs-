# Tino Docs Hub

This repository aggregates documentation and research across multiple projects.

For setup instructions, directory overview, and detailed research listings, see [docs/index.md](docs/index.md).

## Lint research docs

Use `scripts/lint_research_docs.py` to scan Markdown files for mid-word line
splits. Run the script with file or directory paths to check; add `--fix` to
rewrite files in place and automatically join detected splits.
