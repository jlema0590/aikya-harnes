#!/usr/bin/env python3
"""Bienvenida de Aikya en sesiones globales y aviso de inicio para nuevos proyectos.

SessionStart no inicia automáticamente la entrevista: espera /aikya-init.
No descarga recursos, no lee secretos y evita duplicar el saludo local.
"""
from __future__ import annotations
import importlib.util
import json
import os
import sys
from pathlib import Path

def is_new_project(directory: Path, home: Path | None = None) -> bool:
    home=(home or Path.home()).resolve()
    root=directory.resolve()
    if root in (home, home/'.claude', home/'.claude/aikya-harnes') or root==root.parent:
        return False
    if (root/'.harness/project-profile.json').is_file() or not root.is_dir():
        return False
    visible=[x for x in root.iterdir() if x.name != '.DS_Store']
    if not visible:return True
    return any((root/x).exists() for x in
               ('.git','.aikya/bootstrap.json','.aikya/answers.json',
                'pom.xml','build.gradle','package.json','global.json','pubspec.yaml'))

def has_local_welcome(root: Path) -> bool:
    # Si el proyecto ya tiene su propio SessionStart de Aikya, no mostrar doble aviso.
    config=root/'.claude/settings.json'
    if not (root/'.claude/hooks/welcome.py').is_file():
        return False
    try:
        hooks=json.loads(config.read_text(encoding='utf8')).get('hooks',{}).get('SessionStart',[])
        return any('welcome.py' in str(h.get('command',''))
                   for group in hooks if isinstance(group,dict)
                   for h in group.get('hooks',[]) if isinstance(h,dict))
    except (OSError,ValueError,AttributeError,TypeError):
        return False

def banner(root: Path) -> str:
    source=Path(__file__).resolve().parent/'template/.claude/hooks/welcome.py'
    try:
        spec=importlib.util.spec_from_file_location('aikya_global_welcome',source)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.build_message(root)
    except (OSError,ValueError,AttributeError,TypeError):
        return 'Bienvenido a Aikya Harness · '+root.name

def main() -> int:
    try:data=json.load(sys.stdin)
    except (ValueError,OSError):data={}
    if not isinstance(data,dict) or data.get('source','startup') not in ('startup','resume','fork'):
        return 0
    root=Path(data.get('cwd') or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()).expanduser().resolve()
    if not root.is_dir() or has_local_welcome(root):
        return 0
    try:new=is_new_project(root)
    except OSError:new=False
    message=banner(root)
    payload={'systemMessage':message}
    if new:
        payload['systemMessage'] += '\nProyecto sin inicializar. Ejecuta /aikya-init o /aikya-answers para comenzar.'
        if data.get('source','startup')=='startup':
            payload['hookSpecificOutput']={'hookEventName':'SessionStart',
                'additionalContext':'Aikya está disponible. El usuario puede pedir /aikya-init o /aikya-answers; no generes código ni instales herramientas sin confirmación.'}
    print(json.dumps(payload,ensure_ascii=False))
    return 0

if __name__=='__main__':sys.exit(main())
