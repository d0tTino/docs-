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
