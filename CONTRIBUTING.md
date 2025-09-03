# Contributing Guidelines

Thank you for your interest in improving the Tino Docs Hub.

1. Create a branch from `main` for your work.
2. Run `scripts/setup_hooks.sh` to install Git hooks and linters.
3. Make your changes and ensure documentation builds locally.
4. Commit your work and open a Pull Request for review.

Please follow these steps to keep contributions consistent and easy to review.

## Commit Message Conventions

- Use the present tense and imperative mood (e.g., "add feature" not "added" or "adds").
- Begin the subject with an optional scope such as `docs:`, `feat:`, or `fix:` when it helps clarify the change.
- Keep the subject line to 72 characters or fewer.

Example:

```
docs(quickstart): add Git LFS instructions
```

## Code Style Expectations

- Match the surrounding code and documentation style.
- Run linters and formatters before committing to avoid style issues.

## Documentation Style

- Each Markdown file must begin with front matter containing `title`, `tags`, `project`, and `updated` fields.
- Reuse common content with snippets using `--8<-- "path/to/snippet.md"` syntax.
- All images require descriptive alt text to aid accessibility.

## Running pre-commit locally

`scripts/setup_hooks.sh` installs the repository's pre-commit hooks. After installation, run:

```bash
pre-commit run --files <path/to/file>
```

Use `pre-commit run --all-files` to check the entire repository.
