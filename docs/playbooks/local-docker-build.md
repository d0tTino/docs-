---
title: "Local Docker Build"
tags: [productivity, playbook]
project: docs-hub
updated: 2025-08-18
---

--8<-- "_snippets/disclaimer.md"

# Local Build

This repository no longer provides a Dockerfile. Instead you can run MkDocs
directly after installing the Python dependencies.

1. Ensure Python 3.11 or higher is available on your system.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Launch the development server:

   ```bash
   mkdocs serve
   ```

4. Open `http://127.0.0.1:8000` to preview the site.

Running MkDocs locally mirrors the commands used in the CI workflow.

## Common Errors & Fixes

### "ModuleNotFoundError: No module named 'mkdocs'"
Ensure the dependencies are installed by running `pip install -r requirements.txt`.

### "OSError: [Errno 98] Address already in use"
Another process is using port 8000. Stop the process or launch MkDocs on a different port, e.g. `mkdocs serve -a 127.0.0.1:8001`.

### "PermissionError: [Errno 13] Permission denied" when installing packages
Install the packages in a virtual environment or add the `--user` flag to the `pip install` command.
