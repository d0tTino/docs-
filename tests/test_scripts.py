from pathlib import Path
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_setup_hooks_sets_hooks_path(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True)

    script = ROOT / "scripts" / "setup_hooks.sh"
    subprocess.run([str(script)], cwd=repo, check=True)

    result = subprocess.check_output(
        ["git", "config", "--get", "core.hooksPath"], cwd=repo
    ).decode().strip()
    assert result == ".githooks"


def test_migrate_old_docs_git_commands(tmp_path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    log_file = tmp_path / "git.log"
    fake_git = tmp_path / "git"
    fake_git.write_text(
        "#!/bin/sh\n"
        "echo \"$@\" >> \"$LOG\"\n"
        "if [ \"$1\" = rev-parse ]; then\n"
        "  echo \"$REPO_ROOT\"\n"
        "fi\n"
    )
    fake_git.chmod(0o755)

    env = os.environ.copy()
    env.update({
        "PATH": f"{tmp_path}:{env['PATH']}",
        "LOG": str(log_file),
        "REPO_ROOT": str(repo_root),
    })

    script = ROOT / "scripts" / "migrate_old_docs.sh"
    subprocess.run([str(script)], cwd=repo_root, check=True, env=env)

    commands = log_file.read_text().splitlines()
    assert commands[0].startswith("rev-parse --show-toplevel")
    assert commands[1].startswith("clone https://github.com/d0tTino/d0tTino.git")
    assert commands[2].startswith("-C") and "filter-repo" in commands[2]
    assert commands[3].startswith("-C") and commands[3].endswith("+HEAD:d0tTino-import")

