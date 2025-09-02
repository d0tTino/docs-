# Architecture Decision Records

This directory contains architecture decision records (ADRs) for the project.

## Existing ADRs

| Number | Title | Summary |
| ------ | ----- | ------- |
| [0001](0001-use-mkdocs.md) | Use MkDocs for Documentation | Standardize on MkDocs with the Material theme and monorepo plugin for building docs |

## Creating a New ADR

1. Determine the next sequential ADR number. Numbers are zero-padded to four
   digits (e.g. `0002`). Numbers are never reused, even if an ADR is
   superseded.
2. Create a new file named `<number>-<short-name>.md` using the next number
   and a concise hyphenated title, for example `0002-add-search-plugin.md`.
3. Start the file with a heading in the form `# <number>: <Title>` and include
   sections for Status, Context, Decision, and Consequences.
4. Commit the new ADR to version control.

Existing ADRs are listed above for quick reference.
