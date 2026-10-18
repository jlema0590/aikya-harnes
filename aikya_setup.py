#!/usr/bin/env python3
"""Bootstrap reversible de Aikya para Claude Code: scopes global y project.

Invócalo DESDE Claude Code mediante una petición natural. No ejecuta entrevistas ni
instala SDKs ni terceros. Registra comandos Aikya con ejecución conversacional y consentimiento en Claude Code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BOOTSTRAP_COMMANDS=(
    'aikya-init', 'aikya-answers', 'aikya-doctor',
    'aikya-project-init', 'aikya-infra-project', 'aikya-scaffold',
    'aikya-feature', 'aikya-bugfix', 'aikya-architecture-review', 'aikya-mobile-feature',
    'aikya-skills-status', 'aikya-skills-plan', 'aikya-skills-install', 'aikya-quality', 'aikya-docs', 'aikya-tests',
    'aikya-documentation-sync', 'aikya-verify',
)
CORE_FILES=('install.py','doc_bootstrap.py','external_skills.py','aikya_cli.py','aikya_requirements.py','aikya_session.py','aikya_setup.py','skills_registry.py')


def files_to_copy(source:Path):
    for name in CORE_FILES:
        yield source/name,Path(name)
    for folder in ('template','examples','bootstrap_skills'):
        for path in sorted((source/folder).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and not path.name.endswith('.pyc'):
                yield path,path.relative_to(source)


def managed_copy(src:Path,dst:Path,root:Path,logs:list[str]):
    if not src.is_file(): raise FileNotFoundError(src)
    for candidate in (dst, *list(dst.parents)):
        if candidate == root.parent:
            break
        if candidate.is_symlink():
            raise ValueError(f'Enlace simbólico rechazado: {candidate}')
    if dst.exists():
        if dst.read_bytes()==src.read_bytes():
            logs.append(f'IGUAL {dst}')
            return
        # Sólo actualizar contenido generado por una versión anterior de Aikya.
        marker=root/'manifest.json'
        if not marker.is_file():
            logs.append(f'CONSERVADO PERSONALIZADO {dst}')
            return
        previous=json.loads(marker.read_text(encoding='utf8')).get('files',{})
        key=dst.relative_to(root).as_posix()
        old=previous.get(key)
        if not old or hashlib.sha256(dst.read_bytes()).hexdigest()!=old:
            logs.append(f'CONSERVADO PERSONALIZADO {dst}')
            return
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)
    logs.append(f'INSTALADO {dst}')


def register_startup_hook(settings:Path, command:str, logs:list[str]) -> None:
    """Merge a lightweight project-discovery hook without clobbering user settings."""
    if settings.is_symlink():
        logs.append(f'AVISO configuración simbólica conservada: {settings}')
        return
    try:
        user=json.loads(settings.read_text(encoding='utf8')) if settings.exists() else {}
        if not isinstance(user,dict) or not isinstance(user.get('hooks',{}),dict):
            raise ValueError('settings inválido')
    except (ValueError,UnicodeError,OSError):
        logs.append(f'AVISO settings inválido; instalar hook manualmente: {settings}')
        return
    hooks=user.setdefault('hooks',{})
    session=hooks.setdefault('SessionStart',[])
    if not isinstance(session,list):
        logs.append(f'AVISO hooks.SessionStart inválido: {settings}')
        return
    # Avoid hook duplication when setup runs twice.
    if not any('aikya_session.py' in str(h.get('command',''))
               for group in session if isinstance(group,dict)
               for h in group.get('hooks',[]) if isinstance(h,dict)):
        session.append({'matcher':'startup','hooks':[{'type':'command','command':command,'timeout':5}]})
        settings.parent.mkdir(parents=True,exist_ok=True)
        settings.write_text(json.dumps(user,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
        logs.append(f'HOOK SessionStart añadido: {settings}')


# Sólo se retiran los comandos anteriores si conservan literalmente la plantilla antigua.
# Una skill modificada por el usuario nunca se elimina de forma implícita.
LEGACY_RENAMES={
    'aikya-project-bootstrap':'aikya-infra-project',
    'aikya-skills':'aikya-skills-status',
}

def retire_legacy_commands(skill_root: Path, runtime: Path, logs: list[str]) -> None:
    for name,replacement in LEGACY_RENAMES.items():
        legacy=skill_root/name/'SKILL.md'
        older=runtime/'bootstrap_skills'/name/'SKILL.md'
        if not legacy.exists() or legacy.is_symlink():
            continue
        if not older.is_file() or older.is_symlink() or legacy.read_bytes()!=older.read_bytes():
            logs.append(f'CONSERVADO comando antiguo personalizado /{name}; revisar migración a /{replacement}')
            continue
        legacy.unlink()
        try: legacy.parent.rmdir()
        except OSError: pass
        logs.append(f'RETIRADO comando gestionado antiguo /{name}; sustituido por /{replacement}')

def setup(source:Path,target:Path,scope:str,home:Path|None=None,dry_run:bool=False)->list[str]:
    source=source.resolve()
    target=target.expanduser().resolve()
    home=(home or Path.home()).expanduser().resolve()
    if scope not in ('global','project'):raise ValueError('scope debe ser global o project')
    if not (source/'install.py').is_file() or any(not (source/'bootstrap_skills'/name/'SKILL.md').is_file() for name in BOOTSTRAP_COMMANDS):
        raise ValueError('La fuente no es una distribución completa de Aikya')
    runtime=(home/'.claude/aikya-harnes') if scope=='global' else (target/'.aikya/runtime')
    skill_root=(home/'.claude/skills') if scope=='global' else (target/'.claude/skills')
    for candidate in (runtime, runtime.parent, skill_root, skill_root.parent):
        if candidate.is_symlink():
            raise ValueError(f'No usar directorios simbólicos: {candidate}')
    operations=list(files_to_copy(source))
    logs=[f'AIKYA SCOPE={scope} runtime={runtime} skills={skill_root}']
    if dry_run:
        logs.append(f'PLAN: {len(operations)} ficheros de runtime y {len(BOOTSTRAP_COMMANDS)} skills; sin entrevista, sin descarga externa')
        return logs
    runtime.mkdir(parents=True,exist_ok=True)
    retire_legacy_commands(skill_root,runtime,logs)
    old_manifest={}
    if (runtime/'manifest.json').is_file():
        try:old_manifest=json.loads((runtime/'manifest.json').read_text(encoding='utf8')).get('files',{})
        except (ValueError,OSError):old_manifest={}
    new_manifest=dict(old_manifest)
    for src,rel in operations:
        dst=runtime/rel
        managed_copy(src,dst,runtime,logs)
        new_manifest[rel.as_posix()]=hashlib.sha256(dst.read_bytes()).hexdigest()
    (runtime/'manifest.json').write_text(json.dumps({'_generated_by':'aikya-setup','files':new_manifest},indent=2)+'\n',encoding='utf8')
    for name in BOOTSTRAP_COMMANDS:
        src=source/'bootstrap_skills'/name/'SKILL.md'
        dst=skill_root/name/'SKILL.md'
        if dst.is_symlink() or dst.parent.is_symlink():
            raise ValueError(f'Skill simbólica no permitida: {dst}')
        if dst.exists() and dst.read_bytes()!=src.read_bytes():
            # Only replace our own previous generated bootstrap skills.
            if 'AIKYA BOOTSTRAP MANAGED' not in dst.read_text(encoding='utf8'):
                logs.append(f'CONSERVADO skill personalizado: {dst}')
                continue
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst)
        logs.append(f'SKILL disponible: /{name} ({scope})')
    if scope=='global':
        command='python3 "'+str(runtime/'aikya_session.py').replace('"','\\"')+'"'
        register_startup_hook(home/'.claude/settings.json',command,logs)
    else:
        command='python3 "${CLAUDE_PROJECT_DIR}/.aikya/runtime/aikya_session.py"'
        register_startup_hook(target/'.claude/settings.json',command,logs)
    if scope=='project':
        marker=target/'.aikya/bootstrap.json' 
        marker.parent.mkdir(parents=True,exist_ok=True)
        if not marker.exists():
            marker.write_text(json.dumps({'_generated_by':'aikya-setup','scope':'project','runtime':'.aikya/runtime'},indent=2)+'\n',encoding='utf8')
    return logs


def main(argv=None):
    p=argparse.ArgumentParser(description='Instalación inicial de Aikya desde Claude Code')
    p.add_argument('--scope',choices=['global','project'],required=True)
    p.add_argument('--target',type=Path,default=Path.cwd(),help='Directorio de trabajo actual, cuando scope=project')
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args(argv)
    try:
        for line in setup(ROOT,args.target,args.scope,dry_run=args.dry_run): print(line)
    except (OSError,ValueError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 1
    print('Siguiente: dentro de Claude Code utiliza /aikya-init, /aikya-answers, /aikya-scaffold, /aikya-skills-status o /aikya-quality.')
    return 0

if __name__=='__main__':sys.exit(main())
