#!/usr/bin/env python3
"""Validate playbook metadata, local Markdown links, and executable scripts."""
import datetime
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote

import yaml


def validate(root):
    failures = []
    shell = []
    files = [p for p in root.rglob("*") if p.is_file()
             and not any(part.startswith(".") or part == "__pycache__" for part in p.relative_to(root).parts[:-1])]
    files += list((root / ".github").rglob("*.md"))
    for path in files:
        if path.suffix == ".md":
            text = path.read_text()
            for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
                target = unquote(target.split("#", 1)[0])
                if target and not re.match(r"[a-z]+:", target) and not (path.parent / target).exists():
                    failures.append(f"{path.relative_to(root)}: broken link {target}")
        if path.name == "PLAYBOOK.md":
            try:
                text = path.read_text()
                assert text.startswith("---\n"), "missing front matter"
                data = yaml.safe_load(text.split("---", 2)[1])
                required = {"id", "scope", "host", "depends_on", "agnostic", "status", "last_verified", "needs_reboot"}
                assert required <= data.keys(), "missing required metadata"
                assert data["id"] == path.parent.name, "id must match folder"
                assert data["status"] in {"draft", "verified", "example", "retired"}, "invalid maturity"
                assert data["scope"] in {"common", "machine"}, "invalid scope"
                assert type(data["agnostic"]) is bool and type(data["needs_reboot"]) is bool, "expected boolean"
                assert data["last_verified"] is None or type(data["last_verified"]) is datetime.date, "invalid verification date"
                assert data["status"] != "verified" or data["last_verified"] is not None, "verified requires date"
                assert re.fullmatch(r"none|(?:app|plugin):[\w.-]+", data["depends_on"]), "invalid dependency"
                relative = path.relative_to(root).parts
                if relative[0] == "examples":
                    assert data["status"] == "example", "examples must be labeled"
                elif data["scope"] == "common":
                    assert relative[0] == "common" and data["host"] == "all", "common host mismatch"
                else:
                    assert relative[:2] == ("machines", data["host"]), "machine host mismatch"
                for heading in ("Symptoms", "Root cause", "Apply", "Verify", "Rollback", "What not to change", "Tested environment and evidence"):
                    assert f"## {heading}" in text, f"missing {heading}"
            except (AssertionError, TypeError, KeyError, ValueError, yaml.YAMLError) as error:
                failures.append(f"{path.relative_to(root)}: {error}")
        if path.name == "MACHINE.md":
            try:
                data = yaml.safe_load(path.read_text().split("---", 2)[1])
                if path.parent.name != "_template":
                    assert data["id"] == data["hostname"] == path.parent.name, "machine identity mismatch"
                assert isinstance(data["match"], dict), "missing hardware match keys"
            except (AssertionError, TypeError, KeyError, IndexError, yaml.YAMLError) as error:
                failures.append(f"{path.relative_to(root)}: {error}")
        if path.suffix in {".png", ".jpg"}:
            continue
        try:
            first = path.open("rb").readline()
        except OSError:
            continue
        if first.rstrip() == b"#!/bin/bash":
            shell.append(str(path))
            if not path.stat().st_mode & 0o111:
                failures.append(f"{path.relative_to(root)}: missing executable bit")
            if subprocess.run(["bash", "-n", str(path)], check=False).returncode:
                failures.append(f"{path.relative_to(root)}: shell syntax error")
    if shutil.which("shellcheck"):
        if shell and subprocess.run(["shellcheck", *shell], check=False).returncode:
            failures.append("ShellCheck failed")
    else:
        failures.append("ShellCheck is required; install it with your OS package manager")
    return failures


if __name__ == "__main__":
    problems = validate(Path(__file__).resolve().parents[1])
    print("\n".join(problems) if problems else "Repository validation passed")
    sys.exit(bool(problems))
