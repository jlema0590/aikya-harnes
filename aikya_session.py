#!/usr/bin/env python3
"""SessionStart discovery notice for uninitialized workspaces.

Does NOT execute agents or commands. Interactive Claude Code does not support
starting a user turn from SessionStart; the hook prompts /aikya-init.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path


def is_new_project(directory: Path, home: Path | None = None) -> bool:
    home = (home or Path.home()).resolve()
    root = directory.resolve()
    if root == home or root == root.parent:
        return False
    if root == home/'.claude/aikya-harnes' or root == home/'.claude':
        return False
    if (root/'.harness/project-profile.json').is_file():
        return False
    # Avoid advising Aikya on arbitrary folders. A project is an empty workspace,
    # a Git repo, or has clear project/build/bootstrap files.
    if not root.is_dir():
        return False
    visible=[p for p in root.iterdir() if p.name not in ('.DS_Store',)]
    if not visible:
        return True
    return any((root/path).exists() for path in
               ('.git','.aikya/bootstrap.json','.aikya/answers.json','pom.xml','build.gradle',
                'package.json','global.json','Cargo.toml','pubspec.yaml'))


def main():
    try:
        data=json.load(sys.stdin)
    except (ValueError,OSError):
        data={}
    if not isinstance(data,dict) or data.get('source','startup')!='startup':
        return 0
    root=Path(data.get('cwd') or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()).expanduser()
    try:
        if not is_new_project(root):
            return 0
    except OSError:
        return 0
    print(json.dumps({
        'systemMessage':'Aikya Harness disponible · Proyecto sin inicializar. Usa /aikya-init para la entrevista o /aikya-answers para usar decisiones guardadas. Después: /aikya-scaffold, /aikya-skills-status y /aikya-quality.',
        'hookSpecificOutput':{'hookEventName':'SessionStart',
           'additionalContext':'Este repositorio aún no tiene perfil de Aikya. El usuario puede iniciar /aikya-init o /aikya-answers; confirma sus preferencias antes de hacer cualquier instalación o cambio.'}
    },ensure_ascii=False))
    return 0

if __name__=='__main__':sys.exit(main())
