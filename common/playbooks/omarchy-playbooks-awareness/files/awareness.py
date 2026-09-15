#!/usr/bin/env python3
"""User-level awareness and small, conflict-aware file installation journal."""

import base64
import contextlib
import fcntl
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile


def safe_path(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.is_symlink():
            raise RuntimeError(f"Refusing symlink destination: {part}")
    return path


def snapshot(path):
    path = safe_path(path)
    if not path.exists():
        return None
    if not path.is_file():
        raise RuntimeError(f"Expected a regular file: {path}")
    return {"data": base64.b64encode(path.read_bytes()).decode(),
            "mode": stat.S_IMODE(path.stat().st_mode)}


def content(data, mode):
    return {"data": base64.b64encode(data).decode(), "mode": mode}


def write_snapshot(path, value):
    path = safe_path(path)
    if value is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".playbooks-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(base64.b64decode(value["data"], validate=True))
            stream.flush()
            os.fchmod(stream.fileno(), value["mode"])
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


class FileChanges:
    """Preserve the first original; refuse later edits before any replacement."""

    def __init__(self, state):
        self.state = safe_path(state)
        self.entries = json.loads(self.state.read_text()) if self.state.exists() else {}

    def save(self):
        write_snapshot(self.state, content((json.dumps(self.entries, indent=2) + "\n").encode(), 0o600))

    def conflicts(self):
        return [path for path, entry in self.entries.items()
                if snapshot(path) not in (entry["original"], entry["installed"], entry.get("previous", entry["installed"]))]

    def install(self, files):
        conflicts = self.conflicts()
        if conflicts:
            raise RuntimeError("Files changed since installation: " + ", ".join(conflicts))
        before = {str(safe_path(path)): snapshot(path) for path, _, _ in files}
        for path, data, mode in files:
            key = str(safe_path(path))
            entry = self.entries.setdefault(key, {"original": before[key]})
            entry["previous"] = before[key]
            entry["installed"] = content(data, mode)
        self.save()
        for path, _, _ in files:
            write_snapshot(path, self.entries[str(safe_path(path))]["installed"])
        for entry in self.entries.values():
            entry.pop("previous", None)
        self.save()

    def check(self):
        return [path for path, entry in self.entries.items() if snapshot(path) != entry["installed"]]

    def rollback(self):
        conflicts = self.conflicts()
        if conflicts:
            raise RuntimeError("Rollback would overwrite later edits: " + ", ".join(conflicts))
        for path, entry in self.entries.items():
            write_snapshot(path, entry["original"])
        self.state.unlink(missing_ok=True)


@contextlib.contextmanager
def locked(state):
    lock = safe_path(Path(state).with_suffix(".lock"))
    lock.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def repo_valid(root):
    return (root.is_absolute() and (root / "AGENTS.md").is_file()
            and (root / "common/INDEX.md").is_file() and (root / "machines").is_dir()
            and (root / "common/playbooks/omarchy-playbooks-awareness/apply.sh").is_file())


def resolve_repo(home, environ):
    selected = environ.get("MACHINE_PLAYBOOKS")
    registration = home / ".config/machine-playbooks/repo-path"
    if selected is not None:
        root = Path(selected)
        if not selected or not repo_valid(root):
            raise RuntimeError("Invalid MACHINE_PLAYBOOKS; supply an absolute playbooks repository path")
        return root.resolve()
    if registration.exists():
        root = Path(registration.read_text().strip())
        if not repo_valid(root):
            raise RuntimeError(f"Registered repository is missing or invalid: {root}. Re-run its awareness installer.")
        return root.resolve()
    candidates = [home / "Work/machine-playbooks", home / "machine-playbooks",
                  home / "Work/omarchy-machine-playbooks"]
    matches = list(dict.fromkeys(p.resolve() for p in candidates if repo_valid(p)))
    if len(matches) != 1:
        raise RuntimeError("Repository discovery is missing or ambiguous; run awareness apply.sh in your chosen repository")
    return matches[0]


def awareness_files(home, repo):
    source = repo / "common/playbooks/omarchy-playbooks-awareness/files"
    skill = home / ".agents/skills/machine-playbooks"
    return [(skill / "SKILL.md", (source / "SKILL.md").read_bytes(), 0o644),
            (skill / "awareness.py", (source / "awareness.py").read_bytes(), 0o644),
            (home / ".config/omarchy/hooks/post-update.d/50-machine-playbooks-awareness",
             (source / "50-machine-playbooks-awareness").read_bytes(), 0o755),
            (home / ".config/machine-playbooks/repo-path", (str(repo) + "\n").encode(), 0o600)]


def awareness(action, home, repo=None, environ=None):
    environ = os.environ if environ is None else environ
    state = home / ".local/state/machine-playbooks/awareness/files.json"
    if action == "resolve":
        print(resolve_repo(home, environ))
        return 0
    if action == "update":
        root = resolve_repo(home, environ)
        return subprocess.run([str(root / "common/playbooks/omarchy-playbooks-awareness/apply.sh")], check=False).returncode
    if action == "check":
        root = resolve_repo(home, environ)
        journal = FileChanges(state)
        expected = awareness_files(home, root)
        bad = [str(path) for path, data, mode in expected if snapshot(path) != content(data, mode)]
        if not journal.entries or bad or journal.check():
            raise RuntimeError("Awareness incomplete or out of date: " + ", ".join(bad or journal.check()))
        print(f"Awareness verified: {root}")
        return 0
    with locked(state):
        journal = FileChanges(state)
        if action == "apply":
            if repo is None or not repo_valid(repo):
                raise RuntimeError("Installer must be run from a complete playbooks repository")
            journal.install(awareness_files(home, repo.resolve()))
            print(f"Awareness installed for {repo.resolve()}")
        elif action == "rollback":
            if not journal.entries:
                raise RuntimeError("No installation journal; follow the documented legacy cleanup")
            journal.rollback()
            print("Awareness files restored; empty directories remain.")
        else:
            raise RuntimeError(f"Unknown action: {action}")
    return 0


if __name__ == "__main__":
    try:
        command = sys.argv[1] if len(sys.argv) == 2 else ""
        if command in {"apply", "rollback", "update"} and os.geteuid() == 0:
            raise RuntimeError("Run user awareness as your normal user, without sudo")
        source_repo = Path(__file__).resolve().parents[4]
        raise SystemExit(awareness(command, Path.home(), source_repo))
    except (OSError, ValueError, RuntimeError) as error:
        print(f"machine-playbooks: {error}", file=sys.stderr)
        raise SystemExit(1)
