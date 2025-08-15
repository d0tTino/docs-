from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lint_research_docs.py"


def run_linter(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python", str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
    )


def test_linter_detects_split(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    content = (
        "---\n"
        "title: T\n"
        "tags: [a]\n"
        "project: T\n"
        "updated: 2024-01-01\n"
        "---\n"
        '--8<-- "_snippets/disclaimer.md"\n'
        "mod\nel\n"
    )
    (target / "sample.md").write_text(content)

    result = run_linter(target)
    assert result.returncode == 1
    assert "possible mid-word split" in result.stdout


def test_linter_passes_clean_file(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    content = (
        "---\n"
        "title: Sample\n"
        "tags: [a]\n"
        "project: Test\n"
        "updated: 2024-01-01\n"
        "---\n"
        '--8<-- "_snippets/disclaimer.md"\n'
        "model\n\nworks\n"
    )
    (target / "sample.md").write_text(content)

    result = run_linter(target)
    assert result.returncode == 0
    assert result.stdout == ""


def test_linter_detects_trailing_whitespace(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    content = (
        "---\n"
        "title: T\n"
        "tags: [a]\n"
        "project: T\n"
        "updated: 2024-01-01\n"
        "---\n"
        '--8<-- "_snippets/disclaimer.md"\n'
        "line with space \nnext\n"
    )
    (target / "sample.md").write_text(content)

    result = run_linter(target)
    assert result.returncode == 1
    assert "sample.md:" in result.stdout
    assert "trailing whitespace" in result.stdout


def test_linter_requires_disclaimer(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    content = (
        "---\n"
        "title: Sample\n"
        "tags: [a]\n"
        "project: Test\n"
        "updated: 2024-01-01\n"
        "---\n"
    )
    (target / "sample.md").write_text(content)

    result = run_linter(target)
    assert result.returncode == 1
    assert "missing disclaimer snippet" in result.stdout


def test_linter_requires_metadata(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    content = '--8<-- "_snippets/disclaimer.md"\n'
    (target / "sample.md").write_text(content)

    result = run_linter(target)
    assert result.returncode == 1
    assert "missing front matter" in result.stdout
