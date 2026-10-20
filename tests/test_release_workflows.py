"""Regression tests for v5.9.1 release contract and automatic GitHub Actions."""
from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts/ci"))
import release_contract as contract
import prepare_release as prepare

class VersionContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/"LICENSE").write_text("MIT License\n",encoding="utf8")
        (self.root/"VERSION").write_text("5.9.1\n",encoding="utf8")
        (self.root/"CHANGELOG.md").write_text(
            "# Changelog\n\n## v5.9.1 — 2026-10-19\n\n- Corrige publicación.\n"
            "- Incluye artefactos verificables.\n\n## v5.9.0 — 2026-10-18\n\n- Anterior.\n",
            encoding="utf8")

    def valid(self,**kwargs):
        return contract.validate(self.root,tags=["v5.9.0"],head_sha="a"*40,**kwargs)

    def test_version_is_semver_stable(self):
        self.assertEqual((5,9,1),contract.parse_version("5.9.1"))
        self.assertEqual((6,0,0),contract.parse_version("6.0.0\n"))
        for value in ("v5.9.1","5.9.1-rc1","01.2.3","5.9","5.9.1.0","-1.0.0"):
            with self.subTest(version=value),self.assertRaises(contract.ReleaseError):
                contract.parse_version(value)

    def test_contract_accepts_patch_release_above_existing_tag(self):
        output=self.valid()
        self.assertEqual("v5.9.1",output["tag"])
        self.assertFalse(output["tag_exists"])
        self.assertIn("Corrige publicación",output["notes"])
        self.assertNotIn("Anterior.",output["notes"])

    def test_changelog_missing_version_is_rejected(self):
        (self.root/"CHANGELOG.md").write_text("# Changelog\n## v5.9.0\n- test\n")
        with self.assertRaisesRegex(contract.ReleaseError,"exactly one"):
            self.valid()

    def test_duplicate_changelog_release_is_rejected(self):
        file=self.root/"CHANGELOG.md"
        file.write_text(file.read_text()+"\n## v5.9.1 — duplicado\n\n- repetido\n")
        with self.assertRaisesRegex(contract.ReleaseError,"exactly one"):
            self.valid()

    def test_empty_and_placeholder_release_notes_rejected(self):
        file=self.root/"CHANGELOG.md"
        file.write_text("# Changelog\n\n## v5.9.1\n\n## v5.9.0\n\n- Previous\n")
        with self.assertRaisesRegex(contract.ReleaseError,"at least one"):
            self.valid()
        file.write_text("# Changelog\n\n## v5.9.1\n\n- TODO: escribir notas.\n")
        with self.assertRaisesRegex(contract.ReleaseError,"unresolved"):
            self.valid()

    def test_missing_license_or_version_rejected(self):
        (self.root/"LICENSE").unlink()
        with self.assertRaisesRegex(contract.ReleaseError,"LICENSE"):
            self.valid()
        (self.root/"LICENSE").write_text("MIT License")
        (self.root/"VERSION").unlink()
        with self.assertRaisesRegex(contract.ReleaseError,"VERSION"):
            self.valid()

    def test_older_or_equal_release_is_rejected(self):
        with self.assertRaisesRegex(contract.ReleaseError,"higher"):
            contract.validate(self.root,tags=["v5.9.2"],head_sha="a"*40)
        with self.assertRaisesRegex(contract.ReleaseError,"higher"):
            contract.validate(self.root,tags=["v5.10.0"],head_sha="a"*40)

    def test_existing_tag_in_different_commit_rejected(self):
        with patch.object(contract,"known_tags",return_value=["v5.9.0","v5.9.1"]),\
             patch.object(contract,"tagged_commit",return_value="b"*40):
            with self.assertRaisesRegex(contract.ReleaseError,"points to"):
                contract.validate(self.root,head_sha="a"*40)

    def test_existing_tag_on_same_commit_is_idempotent(self):
        with patch.object(contract,"known_tags",return_value=["v5.9.0","v5.9.1"]),\
             patch.object(contract,"tagged_commit",return_value="a"*40):
            result=contract.validate(self.root,head_sha="a"*40)
        self.assertTrue(result["tag_exists"])

    def test_pull_request_allows_same_version_only_if_tag_missing(self):
        with patch.object(contract,"compare_base_version",return_value="5.9.1"):
            result=self.valid(base_ref="origin/main")
            self.assertEqual("v5.9.1",result["tag"])
            self.assertFalse(result["tag_exists"])
        with patch.object(contract,"compare_base_version",return_value="5.9.2"):
            with self.assertRaisesRegex(contract.ReleaseError,"lower"):
                self.valid(base_ref="origin/main")
        with patch.object(contract,"compare_base_version",return_value="5.9.0"):
            self.assertEqual("v5.9.1",self.valid(base_ref="origin/main")["tag"])
        with patch.object(contract,"compare_base_version",return_value=None):
            self.assertEqual("v5.9.1",self.valid(base_ref="origin/main")["tag"])

    def test_same_version_pr_blocked_when_tag_is_already_published(self):
        with patch.object(contract,"compare_base_version",return_value="5.9.1"), \
             patch.object(contract,"known_tags",return_value=["v5.9.0","v5.9.1"]), \
             patch.object(contract,"tagged_commit",return_value="a"*40):
            with self.assertRaisesRegex(contract.ReleaseError,"untagged"):
                contract.validate(self.root,head_sha="a"*40,base_ref="origin/main")

    def test_prepare_next_version_updates_changelog_and_version(self):
        f=self.root/"CHANGELOG.md"
        f.write_text("# Changelog\n\n## Sin publicar\n\n- Nuevo cambio.\n\n"+f.read_text().split("# Changelog\n\n",1)[1])
        name,date=prepare.prepare(self.root,"v5.9.2",date="2026-10-19")
        self.assertEqual("v5.9.2",name)
        self.assertEqual("5.9.2",(self.root/"VERSION").read_text().strip())
        body=f.read_text()
        self.assertIn("## Unreleased\n\n## v5.9.2 — 2026-10-19",body)
        self.assertEqual(1,body.count("## v5.9.2"))
        self.assertIn("Nuevo cambio",contract.notes_from_changelog(body,"5.9.2"))

    def test_prepare_never_overwrites_without_unreleased_notes(self):
        before=(self.root/"VERSION").read_bytes()
        with self.assertRaisesRegex(contract.ReleaseError,"Unreleased"):
            prepare.prepare(self.root,"v5.9.2")
        self.assertEqual(before,(self.root/"VERSION").read_bytes())
        with self.assertRaisesRegex(contract.ReleaseError,"higher"):
            prepare.prepare(self.root,"v5.9.1")

    def test_repository_workflow_is_main_only_and_minimal_write(self):
        yaml=(ROOT/".github/workflows/release.yml").read_text(encoding="utf8")
        self.assertIn("branches: [main]",yaml)
        self.assertIn("workflow_dispatch:",yaml)
        self.assertIn("queue: max",yaml)
        self.assertIn("contents: read",yaml)
        self.assertIn("contents: write",yaml)
        self.assertIn("needs: [verify, package]",yaml)
        self.assertIn("gh release create",yaml)
        self.assertIn("--verify-tag",yaml)
        self.assertIn("github_tag.py",yaml)
        self.assertIn("--target",yaml)
        self.assertNotIn("2>/dev/null || true",yaml)
        self.assertIn("SHA256SUMS",yaml)
        self.assertNotIn("terraform apply",yaml)

    def test_pr_contract_checks_main_not_develop(self):
        yaml=(ROOT/".github/workflows/release-check.yml").read_text(encoding="utf8")
        self.assertIn("branches: [main]",yaml)
        self.assertIn("--base-ref origin/main",yaml)
        self.assertNotIn("contents: write",yaml)

    def test_version_and_release_notes_in_repo(self):
        self.assertEqual("6.0.0",(ROOT/"VERSION").read_text().strip())
        changelog=(ROOT/"CHANGELOG.md").read_text()
        self.assertIn("## v5.9.1",changelog)
        self.assertIn("GitHub Actions fixes and automation",changelog)


if __name__=="__main__":
    unittest.main()
