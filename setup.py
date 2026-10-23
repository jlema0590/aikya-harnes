"""Build-time resource staging; runtime installation uses aikya.installation."""
import json
from pathlib import Path
import shutil
from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).resolve().parent


class BuildPy(build_py):
    def run(self):
        super().run()
        package = Path(self.build_lib) / 'aikya'
        resources = package / 'resources'
        canonical = ROOT / 'src/aikya/resources'
        if canonical.is_dir():
            shutil.copytree(canonical, resources, dirs_exist_ok=True, ignore=lambda folder,names: [name for name in names if name == '__pycache__' or name.endswith('.pyc') or (name.startswith('.env') and name != '.env.example')])
        distribution = resources / 'distribution'
        distribution.mkdir(parents=True, exist_ok=True)
        mapping = json.loads((ROOT / 'src/aikya/module_map.json').read_text())
        for name in [*(key + '.py' for key in mapping if (ROOT / (key + '.py')).is_file()), '_aikya_bootstrap.py', 'requirements-agent-loop.txt', 'VERSION']:
            shutil.copy2(ROOT / name, distribution / name)
        for name in ('AGENT_LOOP.md', 'SECURITY_CONTROLS.md'):
            destination = distribution / 'docs' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / 'docs' / name, destination)
        dependency = self.distribution.extras_require.get('agent-loop', [])
        current = [line.strip() for line in (ROOT / 'requirements-agent-loop.txt').read_text().splitlines() if line.strip() and not line.startswith('#')]
        if current != dependency:
            raise ValueError('Optional SDK requirements must match pyproject.toml')


setup(cmdclass={'build_py': BuildPy})
