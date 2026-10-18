#!/usr/bin/env python3
"""Integraciones de Agent Skills externas para Claude Code (sin MCP).

No se descargan ni ejecutan programas sin consentimiento de la persona que instala.
Ninguna integración toca archivos de usuario existentes ni hace instalaciones en hooks.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SOURCES = {
    'ponytail': 'https://github.com/DietrichGebert/ponytail.git',
    'graphify': 'https://github.com/Graphify-Labs/graphify.git',
    'ui-ux-pro-max': 'https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git',
}


def enabled_names(profile: dict[str, Any]) -> list[str]:
    names = ['ponytail', 'graphify']
    if profile.get('frontend') not in ('none', None) or profile.get('mobile') not in ('none', None):
        names.append('ui-ux-pro-max')
    return names


def planned_commands(profile: dict[str, Any]) -> list[str]:
    commands = [
        'git clone --depth 1 https://github.com/DietrichGebert/ponytail.git <carpeta-temporal>; copiar exclusivamente skills/ponytail/ -> .claude/skills/ponytail/',
        'uv tool install graphifyy  (alternativa: pipx install graphifyy)',
        'graphify install --project --platform claude',
    ]
    if 'ui-ux-pro-max' in enabled_names(profile):
        commands.append('npx --yes ui-ux-pro-max-cli init --ai claude')
    return commands


def _invoke(argv: list[str], *, cwd: Path | None = None, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True,
                          text=True, timeout=timeout, check=False, shell=False)


def _copy_safe_skill(src: Path, dst: Path) -> None:
    if dst.exists() or dst.is_symlink():
        raise FileExistsError(f'Ya existe: {dst}; no sobrescrito')
    if not (src/'SKILL.md').is_file() or (src/'SKILL.md').is_symlink():
        raise ValueError('El repositorio descargado no contiene skills/ponytail/SKILL.md regular')
    entries: list[tuple[Path, Path]] = []
    total = 0
    for path in src.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlink no permitido en skill de terceros: {path}')
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f'Entrada inválida en skill de terceros: {path}')
        sz = path.stat().st_size
        total += sz
        if sz > 1_000_000 or total > 5_000_000 or len(entries) > 500:
            raise ValueError('Skill excede presupuesto de tamaño/archivos')
        entries.append((path, path.relative_to(src)))
    # copiado temporal y rename atomizado: ningún archivo del usuario es sobrescrito
    with tempfile.TemporaryDirectory(dir=str(dst.parent)) as temp:
        stage = Path(temp)/'prepared'
        stage.mkdir()
        for src_file, rel in entries:
            target = stage/rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, target, follow_symlinks=False)
        dst.parent.mkdir(parents=True, exist_ok=True)
        stage.rename(dst)


def install_ponytail(root: Path) -> dict[str, str]:
    dest = root/'.claude/skills/ponytail'
    if (dest/'SKILL.md').is_file():
        return {'state':'present', 'detail':'Ya existe una skill Ponytail; se conserva sin actualizar.'}
    if dest.exists() or dest.is_symlink():
        raise FileExistsError(f'Destino no apto: {dest}')
    if not shutil.which('git'):
        raise RuntimeError('Falta git para instalar Ponytail desde el repositorio oficial.')
    with tempfile.TemporaryDirectory(prefix='harness-ponytail-') as temp:
        checkout = Path(temp)/'upstream'
        result = _invoke(['git','clone','--depth','1',SOURCES['ponytail'],str(checkout)],timeout=120)
        if result.returncode:
            raise RuntimeError(f'git clone falló (código {result.returncode}): {result.stderr[-500:]}')
        revision = _invoke(['git','-C',str(checkout),'rev-parse','HEAD'],timeout=15)
        if revision.returncode:
            raise RuntimeError('No se pudo determinar el commit upstream.')
        _copy_safe_skill(checkout/'skills/ponytail',dest)
        return {'state':'installed','commit':revision.stdout.strip(), 'location':'.claude/skills/ponytail',
                'note':'Se instala sólo la skill; el plugin completo, su band y hooks upstream no se activan.'}


def _bin(name: str, preferred: str | None = None) -> str | None:
    # uv tool may not add user bin dir to current process PATH immediately
    if preferred and Path(preferred).is_file():
        return preferred
    located = shutil.which(name)
    if located:
        return located
    for base in (Path.home()/'.local/bin', Path.home()/'.cargo/bin'):
        candidate = base/name
        if candidate.is_file():
            return str(candidate)
    return None


def install_graphify(root: Path) -> dict[str, str]:
    dest = root/'.claude/skills/graphify'
    already_installed_skill = (dest/'SKILL.md').is_file()
    if (dest.exists() or dest.is_symlink()) and not already_installed_skill:
        raise FileExistsError(f'Destino no apto: {dest}')
    cli = _bin('graphify')
    if already_installed_skill and cli:
        return {'state':'present','detail':'Skill Graphify y CLI detectados; no se reescriben.'}
    if not cli:
        manager = _bin('uv') or _bin('pipx')
        if not manager:
            raise RuntimeError('Requiere uv o pipx para instalar el paquete oficial graphifyy (doble y).')
        result = _invoke([manager,'tool','install','graphifyy'] if Path(manager).name=='uv' else
                         [manager,'install','graphifyy'],timeout=300)
        if result.returncode:
            raise RuntimeError(f'Instalación graphifyy falló ({result.returncode}): {result.stderr[-500:]}')
        cli = _bin('graphify')
    if not cli:
        raise RuntimeError('graphifyy instalado pero graphify no aparece en PATH ni ~/.local/bin.')
    # Usa registro de skill de proyecto si aún no existe. No crea servidor MCP.
    if not already_installed_skill:
        result = _invoke([cli,'install','--project','--platform','claude'],cwd=root,timeout=90)
        if result.returncode:
            raise RuntimeError(f'graphify install falló ({result.returncode}): {result.stderr[-500:]}')
        if not (dest/'SKILL.md').is_file():
            raise RuntimeError('El comando terminó, pero no existe .claude/skills/graphify/SKILL.md.')
    version = _invoke([cli,'--version'],timeout=15)
    return {'state':'installed','location':'.claude/skills/graphify','version':version.stdout.strip()[:120] if version.returncode==0 else 'desconocida',
            'note':'Sólo CLI local; el índice se genera bajo demanda, no durante la instalación.'}


def install_ui_ux(root: Path) -> dict[str, str]:
    dest = root/'.claude/skills/ui-ux-pro-max'
    if (dest/'SKILL.md').is_file():
        return {'state':'present','detail':'Skill UI/UX ya presente; se conserva.'}
    if dest.exists() or dest.is_symlink():
        raise FileExistsError(f'Destino no apto: {dest}')
    npx = _bin('npx')
    if not npx:
        raise RuntimeError('Falta npx (Node.js/npm) para instalar ui-ux-pro-max-cli.')
    result = _invoke([npx,'--yes','ui-ux-pro-max-cli','init','--ai','claude'],cwd=root,timeout=300)
    if result.returncode:
        raise RuntimeError(f'uipro init falló ({result.returncode}): {result.stderr[-500:]}')
    if not (dest/'SKILL.md').is_file():
        raise RuntimeError('uipro terminó, pero .claude/skills/ui-ux-pro-max/SKILL.md no aparece.')
    return {'state':'installed','location':'.claude/skills/ui-ux-pro-max',
            'note':'CLI npm upstream; en producción conviene fijar la versión e inspeccionar la dependencia.'}


INSTALLERS = {'ponytail':install_ponytail,'graphify':install_graphify,'ui-ux-pro-max':install_ui_ux}


def _profile(root: Path) -> dict[str, Any]:
    try:
        return json.loads((root/'.harness/project-profile.json').read_text(encoding='utf8'))['decisions']
    except (OSError, KeyError, ValueError) as exc:
        raise RuntimeError('Perfil no encontrado en .harness/project-profile.json') from exc


def status(root: Path, profile: dict[str,Any]) -> dict[str, Any]:
    raw: dict[str,Any] = {}
    lock = root/'.harness/external-skills-lock.json'
    if lock.is_file():
        try:
            raw = json.loads(lock.read_text(encoding='utf8'))
        except (ValueError,OSError):
            pass
    for name in enabled_names(profile):
        location = root/'.claude/skills'/name/'SKILL.md'
        item = raw.get('skills',{}).get(name,{}) if isinstance(raw.get('skills'),dict) else {}
        state = 'present' if location.is_file() else 'missing'
        print(f'{name}: {state}' + (f' ({item.get("state")}: {item.get("detail", "")})' if item and state=='missing' else ''))
    print('Graphify CLI:', 'disponible' if _bin('graphify') else 'no encontrado')
    return raw


def install_all(root: Path, profile: dict[str, Any], *, permission: bool, dry_run: bool=False) -> dict[str, Any]:
    if not dry_run and not permission:
        raise PermissionError('Instalación de terceros exige aprobación explícita (--yes).')
    root = root.resolve()
    if not root.is_dir():
        raise RuntimeError('El destino debe existir y ser directorio.')
    if dry_run:
        for cmd in planned_commands(profile):
            print('PLAN:',cmd)
        return {'dry_run':True}
    record: dict[str,Any] = {'schema_version':1, 'sources':SOURCES, 'updated_at_utc':datetime.now(timezone.utc).isoformat(), 'skills':{}}
    old_lock = root/'.harness/external-skills-lock.json'
    if old_lock.exists():
        try:
            old = json.loads(old_lock.read_text(encoding='utf8'))
            if isinstance(old,dict) and isinstance(old.get('skills'),dict):
                record['skills'].update(old['skills'])
        except (OSError,ValueError):
            pass
    for name in enabled_names(profile):
        print('Instalando/verificando:',name,flush=True)
        try:
            record['skills'][name] = INSTALLERS[name](root)
            print('  ->',record['skills'][name]['state'])
        except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
            record['skills'][name] = {'state':'failed','detail':str(exc)[:700]}
            print('  -> FALLÓ:',str(exc)[:300],file=sys.stderr)
    old_lock.parent.mkdir(parents=True,exist_ok=True)
    old_lock.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return record


def main(argv: list[str]|None = None) -> int:
    parser = argparse.ArgumentParser(description='Gestionar skills externas de Claude Dev Harness v4')
    parser.add_argument('action',choices=['plan','install','status'])
    parser.add_argument('--target',type=Path,default=Path.cwd())
    parser.add_argument('--yes',action='store_true',help='Aprueba explícitamente ejecutar instaladores externos')
    args=parser.parse_args(argv)
    root=args.target.expanduser().resolve()
    try:
        profile = _profile(root)
        if args.action == 'plan':
            install_all(root,profile,permission=False,dry_run=True)
            return 0
        if args.action == 'status':
            status(root,profile)
            return 0
        result = install_all(root,profile,permission=args.yes)
        return 1 if any(v.get('state')=='failed' for v in result['skills'].values()) else 0
    except (RuntimeError, PermissionError) as exc:
        print('ERROR:',exc,file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
