from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lint_research_docs.py"


def run_linter(path: Path, fix: bool = False) -> subprocess.CompletedProcess:
    cmd = ["python", str(SCRIPT)]
    if fix:
        cmd.append("--fix")
    cmd.append(str(path))
    return subprocess.run(cmd, capture_output=True, text=True)


def test_linter_detects_split(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    (target / "sample.md").write_text("mod\nel\n")

    result = run_linter(target)
    assert result.returncode == 1
    assert "sample.md:1" in result.stdout


def test_linter_passes_clean_file(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    (target / "sample.md").write_text("model\n\nworks\n")

    result = run_linter(target)
    assert result.returncode == 0
    assert result.stdout == ""


def test_linter_fixes_split(tmp_path):
    target = tmp_path / "docs" / "ai-research"
    target.mkdir(parents=True)
    sample = target / "sample.md"
    sample.write_text("mod\nel\n")

    result = run_linter(target, fix=True)
    assert result.returncode == 0
    assert sample.read_text() == "model\n"

    result = run_linter(target)
    assert result.returncode == 0
