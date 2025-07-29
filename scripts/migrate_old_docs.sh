#!/usr/bin/env bash
# Migrate documentation from the old d0tTino repository.
#
# This script clones the old repo and uses git filter-repo to keep only
# documentation related paths. The filtered history is then fetched into the
# current repository as the branch `d0tTino-import`.
#
# Usage: ./scripts/migrate_old_docs.sh

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# Ensure git-filter-repo is installed before proceeding
if ! command -v git-filter-repo >/dev/null; then
    echo "git-filter-repo is required. Install it and retry." >&2
    exit 1
fi

# Clone the legacy repo
git clone https://github.com/d0tTino/d0tTino.git "$TMP_DIR"

# Filter to just documentation paths and rewrite under old_docs/d0tTino/
git -C "$TMP_DIR" filter-repo --force \
  --path README.md \
  --path dotfiles \
  --path llm \
  --path oh-my-posh \
  --path vscode \
  --path windows-terminal \
  --to-subdirectory-filter old_docs/d0tTino

# Import the filtered history as a local branch
git -C "$REPO_ROOT" fetch "$TMP_DIR" +HEAD:d0tTino-import

echo "Filtered history available on branch 'd0tTino-import'." >&2
echo "Merge it with: git merge d0tTino-import --allow-unrelated-histories" >&2

rm -rf "$TMP_DIR"
