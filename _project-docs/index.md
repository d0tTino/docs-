---
title: "Project Docs Index"
tags: [sample, docs]
project: sample-project
updated: 2025-01-01
---

# Project Documentation

This directory organizes project-specific docs as git submodules. Add a new
project with `git submodule add <repository-url> _project-docs/<project-folder>`
or see the [main README](../README.md#project-documentation-submodules) for
details.

## Current Submodules

No project submodules are currently registered. After adding one, list it here
using a short description and a link to its `README.md`.

## Updating Submodules

Pull the latest commits for all project docs with:

```bash
git submodule update --remote --recursive
```

## Removing a Submodule

1. Deinitialize the submodule:
   `git submodule deinit -f _project-docs/<project-folder>`
2. Remove the submodule from the index:
   `git rm -f _project-docs/<project-folder>`
3. Delete leftover metadata:
   `rm -rf .git/modules/_project-docs/<project-folder>`
4. Commit the changes.

