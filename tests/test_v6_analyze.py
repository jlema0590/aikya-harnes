"""v6 greenfield/brownfield separation and safety compatibility tests."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import aikya_cli
import install
from aikya_analyze import execute
from project_discovery import scan, safe_scope
from profile_builder import build
from token_policy import HAIKU_45

class AnalyzeV6Tests(unittest.TestCase):
    def test_empty_repository_redirects_to_init_without_writes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            result = execute(p, approved=True)
            self.assertEqual(result["status"], "EMPTY")
            self.assertFalse(result["writes"])
            self.assertEqual(list(p.iterdir()), [])

    def test_safe_scope_rejects_traversal_and_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/"a").mkdir()
            with self.assertRaises(ValueError):
                safe_scope(root, "../")
            outside = root.parent
            (root/"link").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                safe_scope(root, "link")

    def test_java_docker_profile_detected_without_writes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/"pom.xml").write_text("<project/>")
            (root/"Dockerfile").write_text("FROM example:1")
            inv = scan(root)
            self.assertEqual(inv["project_type"], "development")
            profile = build(root, inv)
            self.assertEqual(profile["status"], "READY")
            self.assertEqual(profile["profile"]["backend"], "java")
            self.assertEqual(profile["profile"]["mode"], "existing")
            self.assertEqual(profile["profile"]["deployment"], "docker")
            result = execute(root, dry_run=True)
            self.assertFalse(result["writes"])
            self.assertFalse((root/".aikya").exists())

    def test_vue_and_angular_are_discovered(self):
        for dep, tech in (("vue", "vue"), ("@angular/core", "angular")):
            with self.subTest(tech=tech), tempfile.TemporaryDirectory() as d:
                root=Path(d)
                (root/"package.json").write_text(json.dumps({"dependencies":{dep:"1"}}))
                inv=scan(root)
                self.assertIn(tech, {m["technology"] for m in inv["modules"]})
                self.assertEqual(build(root,inv)["profile"]["frontend"],tech)

    def test_fluttter_is_recognized(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pubspec.yaml").write_text("name: example")
            profile=build(root,scan(root))
            self.assertEqual(profile["status"], "READY")
            self.assertEqual(profile["profile"]["mobile_framework"], "flutter")

    def test_terraform_scripts_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"main.tf").write_text('provider "azurerm" {}')
            (root/"deploy.sh").write_text("#!/bin/sh\nexit 1\n")
            inv=scan(root)
            self.assertEqual(inv["project_type"], "infrastructure")
            self.assertIn("scripts", inv["infrastructure"])
            projection=build(root,inv)
            self.assertEqual(projection["status"],"READY")
            self.assertEqual(projection["profile"]["infrastructure"]["iac"], "terraform")
            self.assertFalse((root/".aikya").exists())

    def test_multistack_keeps_evidence_without_inventing_main_backend(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"node").mkdir();(root/"py").mkdir()
            (root/"node/package.json").write_text(json.dumps({"dependencies":{"express":"1"}}))
            (root/"py/pyproject.toml").write_text("[project]\nname='sample'")
            inv=scan(root)
            self.assertEqual(len([m for m in inv["modules"] if m["role"]=="backend"]),2)
            projection=build(root,inv)
            self.assertEqual(projection["status"],"PARTIAL")
            report=execute(root,approved=True)
            self.assertFalse(report["writes"])
            self.assertEqual(report["status"],"PARTIAL")

    def test_default_analyze_is_consent_required_and_no_write(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pom.xml").write_text("<project/>")
            report=execute(root)
            self.assertEqual(report["status"],"READY")
            self.assertFalse(report["writes"])
            self.assertTrue(report["approval_required"])
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["pom.xml"])
            self.assertTrue(all(op["action"]=="CREATE_MANAGED" for op in report["plan"]))

    def test_approved_adoption_preserves_existing_workflows_gitignore_and_app(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            original={
                "pom.xml": "<project/>",
                "Dockerfile": "FROM example:1",
                ".gitignore": "team-custom-ignore\n",
                ".github/workflows/deploy.yml": "name: custom\n",
                "scripts/deploy.sh": "#!/bin/sh\nexit 0\n"
            }
            for name, contents in original.items():
                target=root/name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(contents)
            report=execute(root,approved=True)
            self.assertEqual(report["status"],"READY")
            self.assertTrue(report["writes"])
            for name, data in original.items():
                self.assertEqual((root/name).read_text(),data)
            self.assertTrue((root/".harness/project-profile.json").is_file())
            self.assertTrue((root/".aikya/analysis/manifest.json").is_file())
            self.assertTrue((root/".claude/agents/java-developer.md").is_file())
            self.assertTrue((root/".claude/agents/docker-developer.md").is_file())
            self.assertTrue((root/".claude/skills/aikya-analyze/SKILL.md").is_file())

    def test_refresh_without_changes_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pom.xml").write_text("<project/>")
            self.assertEqual(execute(root,approved=True)["status"],"READY")
            report=root/".aikya/analysis/report.md"
            manifest=root/".aikya/analysis/manifest.json"
            before=(report.read_bytes(),manifest.read_bytes())
            result=execute(root,approved=True,refresh=True)
            self.assertEqual(result["status"],"READY")
            self.assertEqual(before,(report.read_bytes(),manifest.read_bytes()))

    def test_custom_report_conflict_does_not_clobber(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pom.xml").write_text("<project/>")
            execute(root,approved=True)
            report=root/".aikya/analysis/report.md"
            report.write_text("CUSTOM USER REPORT")
            response=execute(root,approved=True,refresh=True)
            self.assertEqual(response["status"],"NEEDS_REVIEW")
            self.assertFalse(response["writes"])
            self.assertEqual(report.read_text(),"CUSTOM USER REPORT")

    def test_legacy_profile_and_model_policy_stable(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pom.xml").write_text("<project/>")
            (root/".aikya").mkdir()
            policy=root/".aikya/model-policy.json"
            policy.write_text(json.dumps({"schema_version":1,"auxiliary_enabled":True,
                                          "user_approved":True,"auxiliary_model":HAIKU_45}))
            old=policy.read_bytes()
            self.assertEqual(execute(root,approved=True)["status"],"READY")
            self.assertEqual(policy.read_bytes(),old)

    def test_existing_init_cli_fails_without_write(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pom.xml").write_text("<project/>")
            source=root/"old-answers.json"
            source.write_text(json.dumps({"mode":"existing","backend":"java"}))
            result=aikya_cli.main(["init","--target",str(root),"--answers",str(source)])
            self.assertEqual(result,2)
            self.assertFalse((root/".harness").exists())

    def test_report_only_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"pom.xml").write_text("<project/>")
            result=execute(root,report_only=True,approved=True,focus="security")
            self.assertFalse(result["writes"])
            self.assertFalse((root/".aikya").exists())

if __name__ == "__main__":
    unittest.main()
