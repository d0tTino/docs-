# Local Docker Build

Follow these steps to build and preview the documentation site inside a container.

1. Ensure Docker is installed on your system.
2. Build the image from the repository root:
   ```bash
   docker build -t docs-site -f Dockerfile .
   ```
3. Run the container and expose port 8000:
   ```bash
   docker run --rm -p 8000:8000 docs-site
   ```
4. Open `http://localhost:8000` to preview the site served by MkDocs.

The Dockerfile installs dependencies and invokes `mkdocs serve` so you can iterate locally without affecting your host environment.
