# 0001: Use MkDocs for Documentation

## Status

Accepted

## Context

We need a static site generator for publishing project documentation. The
team is familiar with Markdown and wants a simple workflow for hosting docs
on GitHub Pages.

## Decision

We will build the documentation site using [MkDocs](https://www.mkdocs.org/).
The `mkdocs-material` theme and `mkdocs-monorepo-plugin` plugin are included
for styling and multi-repository support.

## Consequences

Documentation can be built locally with `mkdocs serve` and deployed via the
existing GitHub Actions workflow. Contributors must have Python installed to
build the site.
