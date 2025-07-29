#!/bin/sh
# Configure git to use repository-specific hooks

# Resolve the repository root in case the script is run from a subdirectory.
REPO_ROOT=$(git rev-parse --show-toplevel)

# Configure git to look for hooks in the .githooks directory at the repo root.
git config core.hooksPath "$REPO_ROOT/.githooks"
