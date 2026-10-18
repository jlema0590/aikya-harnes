"""Acceptance tests for Claude-native Aikya command routing and documentation."""
import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import aikya_setup
import install

REQUIRED={
    'aikya-init', 'aikya-answers', 'aikya-doctor', 'aikya-project-init',
    'aikya-project-bootstrap', 'aikya-scaffold', 'aikya-feature',
    'aikya-bugfix', 'aikya-architecture-review', 'aikya-mobile-feature',
    'aikya-skills', 'aikya-quality', 'aikya-docs', 'aikya-tests',
    'aikya-documentation-sync', 'aikya-verify',
}

class V51Commands(unittest.TestCase):
    def test_all_commands_are_registered_and_valid(self):
        self.assertEqual(REQUIRED,set(aikya_setup.BOOTSTRAP_COMMANDS))
        for name in REQUIRED:
            body=(ROOT/'bootstrap_skills'/name/'SKILL.md').read_text()
            self.assertTrue(body.startswith('---\nname: '+name+'\n'),name)
            self.assertIn('<!-- AIKYA BOOTSTRAP MANAGED -->',body,name)
            self.assertIn('disable-model-invocation: true',body,name)

    def test_global_installs_every_command_without_changing_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); project=base/'app'; project.mkdir()
            (project/'package.json').write_text('{"name":"app"}')
            aikya_setup.setup(ROOT,project,'global',home=base/'home')
            for name in REQUIRED:
                self.assertTrue((base/'home/.claude/skills'/name/'SKILL.md').is_file(),name)
            self.assertEqual(['package.json'],sorted(x.name for x in project.iterdir()))
            self.assertFalse((project/'.harness').exists())

    def test_project_bootstrap_still_allows_new_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp)/'app'
            aikya_setup.setup(ROOT,project,'project')
            self.assertTrue(install.only_aikya_bootstrap(project))
            self.assertTrue((project/'.aikya/runtime/bootstrap_skills/aikya-skills/SKILL.md').exists())
            for name in REQUIRED:
                self.assertTrue((project/'.claude/skills'/name/'SKILL.md').exists(),name)

    def test_managed_skill_updates_but_custom_skill_is_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); project=base/'proj'
            aikya_setup.setup(ROOT,project,'project')
            managed=project/'.claude/skills/aikya-skills/SKILL.md'
            custom=project/'.claude/skills/aikya-tests/SKILL.md'
            managed.write_text(managed.read_text().replace('Agent Skills', 'Agent Skills actualizadas'))
            custom.write_text('Reglas del equipo\n')
            aikya_setup.setup(ROOT,project,'project')
            self.assertEqual((ROOT/'bootstrap_skills/aikya-skills/SKILL.md').read_text(),managed.read_text())
            self.assertEqual('Reglas del equipo\n',custom.read_text())

    def test_external_and_scaffold_require_approval_from_claude(self):
        skills=(ROOT/'bootstrap_skills/aikya-skills/SKILL.md').read_text()
        scaffold=(ROOT/'bootstrap_skills/aikya-scaffold/SKILL.md').read_text()
        self.assertIn('autorización explícita',skills.lower())
        self.assertIn('aprobación inequívoca',scaffold.lower())
        self.assertIn('requirements',scaffold)
        self.assertIn('mode: existing',scaffold)

    def test_installed_project_has_new_workflows(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            sample=json.loads((ROOT/'examples/new-next-react.json').read_text())
            profile=install.validated(sample,target)
            install.install(target,profile,{'modules':[]},dry_run=False)
            for name in ('aikya-scaffold','aikya-skills','aikya-quality','aikya-tests','aikya-docs'):
                self.assertTrue((target/'.claude/skills'/name/'SKILL.md').is_file(),name)

    def test_readme_no_manual_terminal_commands(self):
        readme=(ROOT/'README.md').read_text()
        self.assertNotIn('```bash',readme)
        self.assertNotIn('python3 ',readme)
        self.assertNotIn('git clone ',readme)
        for name in REQUIRED:
            self.assertIn('/'+name,readme)
        self.assertIn('Claude Code',readme)

if __name__=='__main__': unittest.main()
