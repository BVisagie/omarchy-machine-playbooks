import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "common/playbooks/omarchy-playbooks-awareness"
spec = importlib.util.spec_from_file_location("awareness", SOURCE / "files/awareness.py")
aw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aw)


class AwarenessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "user"
        self.home.mkdir()
        self.repo = self.make_repo(self.base / "custom checkout's location")

    def make_repo(self, root):
        (root / "common").mkdir(parents=True)
        (root / "machines").mkdir()
        (root / "AGENTS.md").write_text("instructions")
        (root / "common/INDEX.md").write_text("index")
        shutil.copytree(SOURCE, root / "common/playbooks/omarchy-playbooks-awareness")
        return root

    def apply(self):
        aw.awareness("apply", self.home, self.repo, {})

    def test_custom_path_and_readonly_check(self):
        self.apply()
        before = {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(aw.resolve_repo(self.home, {}), self.repo)
        self.assertEqual(aw.awareness("check", self.home, environ={}), 0)
        after = {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_repeat_and_restore_original(self):
        skill = self.home / ".agents/skills/machine-playbooks/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("original")
        skill.chmod(0o640)
        self.apply()
        self.apply()
        aw.awareness("rollback", self.home, environ={})
        self.assertEqual(skill.read_text(), "original")
        self.assertEqual(skill.stat().st_mode & 0o777, 0o640)
        self.assertFalse((self.home / ".config/machine-playbooks/repo-path").exists())

    def test_conflict_prevents_any_rollback(self):
        self.apply()
        skill = self.home / ".agents/skills/machine-playbooks/SKILL.md"
        skill.write_text("later user edit")
        with self.assertRaisesRegex(RuntimeError, "later edits"):
            aw.awareness("rollback", self.home, environ={})
        self.assertTrue((self.home / ".config/machine-playbooks/repo-path").exists())
        with self.assertRaisesRegex(RuntimeError, "changed since"):
            self.apply()

    def test_symlink_preflight(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.home / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            self.apply()
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.home / ".config/machine-playbooks/repo-path").exists())

    def test_invalid_selection_never_falls_back(self):
        self.make_repo(self.home / "Work/machine-playbooks")
        with self.assertRaisesRegex(RuntimeError, "Invalid MACHINE_PLAYBOOKS"):
            aw.resolve_repo(self.home, {"MACHINE_PLAYBOOKS": "/missing"})
        with self.assertRaises(RuntimeError):
            aw.resolve_repo(self.home, {"MACHINE_PLAYBOOKS": ""})
        self.apply()
        self.repo.rename(self.base / "moved")
        with self.assertRaisesRegex(RuntimeError, "Registered repository"):
            aw.resolve_repo(self.home, {})
        self.repo = self.base / "moved"
        self.apply()
        self.assertEqual(aw.resolve_repo(self.home, {}), self.repo)

    def test_ambiguous_checkouts_and_explicit_override(self):
        a = self.make_repo(self.home / "Work/machine-playbooks")
        self.make_repo(self.home / "Work/omarchy-machine-playbooks")
        with self.assertRaisesRegex(RuntimeError, "ambiguous"):
            aw.resolve_repo(self.home, {})
        self.apply()
        self.assertEqual(aw.resolve_repo(self.home, {}), self.repo)
        self.assertEqual(aw.resolve_repo(self.home, {"MACHINE_PLAYBOOKS": str(a)}), a)

    def test_update_propagates_failure_and_uses_selected_repo(self):
        self.apply()
        with patch.object(aw.subprocess, "run") as run:
            run.return_value.returncode = 7
            self.assertEqual(aw.awareness("update", self.home, environ={}), 7)
            self.assertEqual(run.call_args.args[0], [str(self.repo / "common/playbooks/omarchy-playbooks-awareness/apply.sh")])

    def test_interrupted_upgrade_preserves_recovery(self):
        target = self.base / "target"
        target.write_text("original")
        state = self.base / "files.json"
        aw.FileChanges(state).install([(target, b"version one", 0o644)])
        real_write = aw.write_snapshot

        def fail_target(path, data):
            if path == target:
                raise OSError("simulated failed install")
            real_write(path, data)

        with patch.object(aw, "write_snapshot", fail_target), self.assertRaises(OSError):
            aw.FileChanges(state).install([(target, b"version two", 0o644)])
        aw.FileChanges(state).rollback()
        self.assertEqual(target.read_text(), "original")

    def test_missing_check_does_not_create_state(self):
        with self.assertRaises(RuntimeError):
            aw.awareness("check", self.home, environ={"MACHINE_PLAYBOOKS": str(self.repo)})
        self.assertEqual(list(self.home.iterdir()), [])

    def test_file_symlink_rejected(self):
        self.apply()
        skill = self.home / ".agents/skills/machine-playbooks/SKILL.md"
        skill.unlink()
        skill.symlink_to(self.repo / "AGENTS.md")
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            self.apply()


if __name__ == "__main__":
    unittest.main()
