#!/usr/bin/env python3
"""Documentación por petición: snapshots locales, verificación de cobertura y CI.

Solo stdlib. No lee contenido de prompts ni secretos; almacena hash, categoría y rutas.
Nota: un guardrail verifica modificaciones/estructura, NO exactitud semántica.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[3] if Path(__file__).resolve().parents[2].name == 'aikya' else Path(__file__).resolve().parents[2]
STATE = ROOT / '.harness' / 'state'
IGNORED = {'.git', '.harness', 'node_modules', '.next', '.nuxt', '.venv',
           'venv', 'dist', 'build', 'target', 'obj', 'bin', 'coverage',
           '.gradle', '.idea', '.dart_tool', 'Pods', '.terraform', '__pycache__'}
CONFIG_FILES = {'pom.xml','build.gradle','build.gradle.kts','package.json',
                'tsconfig.json','Dockerfile','docker-compose.yml','compose.yaml',
                'settings.gradle','settings.gradle.kts', 'pubspec.yaml',
                'global.json', 'gradle.properties'}
DOCS_REQUIRED = ('aikya/docs/skills.md','aikya/docs/overview.md','aikya/docs/plan/roadmap.md',
                 'aikya/docs/features/index.md','aikya/docs/bugs/index.md',
                 'aikya/docs/security/security.md','aikya/docs/architecture/overview.md',
                 'aikya/docs/operations/deployment.md','aikya/docs/operations/observability.md',
                 'aikya/docs/quality/testing.md','aikya/docs/decisions/README.md',
                 'aikya/docs/changes/README.md')


def normalized_session(session: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_-]', '_', session or 'default')[:80] or 'default'


def file_map() -> dict[str,str]:
    """Snapshot de archivos relevantes; ignora .env y secretos sin abrirlos."""
    mapping: dict[str,str] = {}
    seen = 0
    for base, dirs, names in os.walk(ROOT, followlinks=False):
        dirs[:] = [d for d in dirs if d not in IGNORED and not d.startswith('.git')]
        for name in names:
            path = Path(base)/name
            rel = path.relative_to(ROOT).as_posix()
            if name.startswith('.env') or path.is_symlink() or not path.is_file():
                continue
            if rel.startswith('aikya/docs/') or is_source(rel):
                try:
                    if path.stat().st_size > 3_000_000:
                        mapping[rel] = f'large:{path.stat().st_size}:{path.stat().st_mtime_ns}'
                    else:
                        mapping[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
                except OSError:
                    continue
                seen += 1
                if seen >= 12000:
                    # En un repo enorme es una aproximación; avisar a través de estado.
                    mapping['__TRUNCATED__'] = 'true'
                    return mapping
    return mapping


def is_source(path: str) -> bool:
    name = path.rsplit('/',1)[-1]
    if path.startswith('.claude/skills/') and name == 'SKILL.md':
        return True
    if name in CONFIG_FILES or name.endswith(('.csproj','.sln','.xcodeproj','.xcworkspace')):
        return True
    return (path.startswith(('apps/','api/','backend/','server/','src/','web/',
                             'client/','frontend/','mobile/','android/','ios/',
                             'packages/','tests/','test/','infra/','.github/',
                             '.gitlab/')) or
            path.endswith(('.java','.kt','.kts','.swift','.cs','.tsx','.ts',
                           '.jsx','.js','.vue','.dart','.go','.py','.tf')))


def kind_from_prompt(prompt: str) -> str:
    """Word-boundary classification; suggestions only, never sole proof of changed files."""
    p = prompt.lower()
    keywords = {
        'security': ('seguridad', 'vulnerabilidad', 'autenticación', 'autorización',
                     'security', 'cve', 'secrets'),
        'bug': ('bug', 'error', 'fix', 'corrige', 'corregir', 'fallo',
                'regresión', 'defecto'),
        'architecture': ('arquitectura', 'refactor', 'migración',
                         'architecture', 'refactoring'),
        'operations': ('devops', 'deploy', 'pipeline', 'docker',
                       'kubernetes', 'terraform', 'ci/cd'),
        'feature': ('feature', 'funcionalidad', 'implementa', 'crear',
                    'añade', 'agrega', 'endpoint', 'pantalla'),
    }
    matches = [kind for kind, terms in keywords.items()
               if any(re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', p)
                      for term in terms)]
    return '+'.join(matches) if matches else 'general'


def start_request(session: str, prompt: str) -> dict:
    STATE.mkdir(parents=True,exist_ok=True)
    request_id = 'REQ-'+datetime.now(timezone.utc).strftime('%Y%m%d')+'-'+uuid4().hex[:8]
    state = {'request_id':request_id, 'session_id':normalized_session(session),
             'kind':kind_from_prompt(prompt),
             'prompt_sha256':hashlib.sha256(prompt.encode('utf8')).hexdigest(),
             'started_utc':datetime.now(timezone.utc).isoformat(),
             'baseline':file_map()}
    # Sólo escribe estado local; nunca persiste el texto completo del prompt.
    path = STATE / (normalized_session(session)+'.json')
    path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return state


def load_state(session: str) -> dict | None:
    path = STATE/(normalized_session(session)+'.json')
    try:
        data = json.loads(path.read_text(encoding='utf8'))
        return data if isinstance(data,dict) and 'baseline' in data else None
    except (OSError,ValueError):
        return None


def changes(baseline: dict[str,str], current: dict[str,str]) -> tuple[list[str],list[str]]:
    code = sorted(p for p in baseline.keys() | current.keys()
                  if p != '__TRUNCATED__' and is_source(p) and not p.startswith('aikya/docs/')
                  and baseline.get(p) != current.get(p))
    docs = sorted(p for p in baseline.keys() | current.keys()
                  if p.startswith('aikya/docs/') and baseline.get(p) != current.get(p))
    return code,docs


def affected_docs(kind: str, paths: list[str]) -> list[str]:
    required: set[str] = set()
    kinds=set(kind.split('+'))
    if 'feature' in kinds:
        required.update(('aikya/docs/features/index.md','aikya/docs/plan/roadmap.md'))
    if 'bug' in kinds:
        required.add('aikya/docs/bugs/index.md')
    if 'security' in kinds:
        required.add('aikya/docs/security/security.md')
    if 'architecture' in kinds:
        required.add('aikya/docs/architecture/overview.md')
    if 'operations' in kinds:
        required.add('aikya/docs/operations/deployment.md')
    for path in paths:
        if path.startswith('.claude/skills/'):
            required.add('aikya/docs/skills.md')
        p = path.lower()
        # El sistema de diseño sólo se exige si existe una interfaz y se toca una pantalla/componente.
        if (p.endswith(('.tsx','.jsx','.vue','.css','.scss','.svelte')) or
            any(part in p for part in ('/screens/','/components/','/pages/','/views/','/ui/'))) and (
            p.startswith(('apps/web/','apps/frontend/','frontend/','web/','client/','src/','apps/mobile/','apps/android/','apps/ios/','mobile/'))):
            if (ROOT/'aikya/docs/design/design-system.md').is_file():
                required.add('aikya/docs/design/design-system.md')
        if p.startswith(('tests/','test/','aikya/test/')) or '/test/' in p or '/tests/' in p or p.endswith(('.test.ts','.spec.ts')):
            required.add('aikya/docs/quality/testing.md')
        if p.startswith(('infra/','.github/','.gitlab/')) or any(w in p for w in ('docker','terraform','k8s','helm')):
            required.add('aikya/docs/operations/deployment.md')
        if any(w in p for w in ('security','auth','permission','credential')):
            required.add('aikya/docs/security/security.md')
        if any(w in p for w in ('telemetry','observab','tracing','metrics')):
            required.add('aikya/docs/operations/observability.md')
        if any(w in p for w in ('architecture','module','schema','migration')):
            required.add('aikya/docs/architecture/overview.md')
    if not required:
        required.add('aikya/docs/overview.md')
    return sorted(required)


def nonplaceholder(path: Path) -> bool:
    try:
        s = path.read_text(encoding='utf8')
    except (OSError,UnicodeError):
        return False
    return len(s.strip()) >= 80 and 'TODO: completar' not in s and 'PENDIENTE_DE_COMPLETAR' not in s


def validate_request(state: dict, now: dict|None=None) -> tuple[bool,list[str]]:
    now = now if now is not None else file_map()
    changed, updated = changes(state['baseline'],now)
    if not changed:
        return True,['Sin cambios en código/infraestructura durante esta petición: no se requieren modificaciones documentales.']
    req = state['request_id']
    change_path = 'aikya/docs/changes/'+req+'.md'
    required = affected_docs(state['kind'],changed)
    errors: list[str] = []
    if '__TRUNCATED__' in state['baseline'] or '__TRUNCATED__' in now:
        errors.append('Inventario de archivos truncado; revisa manualmente los cambios.')
    if change_path not in updated or not nonplaceholder(ROOT/change_path):
        errors.append(f'Falta bitácora sustantiva de la petición: {change_path}.')
    else:
        content = (ROOT/change_path).read_text(encoding='utf8')
        for heading in ('## Cambios', '## Evidencias', '## Documentos actualizados'):
            if heading not in content:
                errors.append(f'La bitácora debe contener {heading}.')
        if not any(p in content for p in changed):
            errors.append('La bitácora no referencia ninguno de los archivos de código modificados.')
        if not any(doc in content for doc in required):
            errors.append('La bitácora no referencia los documentos obligatorios.')
    for doc in required:
        if doc not in updated or not nonplaceholder(ROOT/doc):
            errors.append(f'Falta actualizar documento afectado: {doc}')
    return not errors, ([f'Cambios en código: {", ".join(changed[:12])}',
                         f'Documentos requeridos: {", ".join(required)}'] + errors)


def validate_base() -> list[str]:
    return [f'No existe o está vacío: {p}' for p in DOCS_REQUIRED
            if not (ROOT/p).is_file() or not (ROOT/p).read_text(encoding='utf8').strip()]


def git_changed(base: str) -> list[str]:
    # Evita shell=True; sólo nombres, no se leen secretos ni contenido de archivos.
    command = ['git','diff','--name-only','--diff-filter=ACDMRT',f'{base}...HEAD']
    res = subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=15)
    if res.returncode:
        res = subprocess.run(['git','diff','--name-only','--diff-filter=ACDMRT',base,'HEAD'],
                             cwd=ROOT,capture_output=True,text=True,timeout=15)
    if res.returncode:
        raise ValueError('No se pudo resolver base Git: '+res.stderr.strip())
    return sorted({x.strip() for x in res.stdout.splitlines() if x.strip()})


def validate_ci(paths: list[str]) -> tuple[bool,list[str]]:
    changed = [p for p in paths if is_source(p) and not p.startswith('aikya/docs/')]
    if not changed:
        return True,['Sin código modificado en el diff: documentación sin cambios permitida.']
    docs = {p for p in paths if p.startswith('aikya/docs/')}
    # El tipo exacto de la petición no se infiere en CI; se valida categoría por rutas +
    # al menos un doc funcional, con revisión humana para semántica.
    required = [p for p in affected_docs('general',changed) if p != 'aikya/docs/overview.md']
    if not any(x in docs for x in DOCS_REQUIRED if x not in ('aikya/docs/README.md',)):
        required.append('una página temática de aikya/docs/ (además de la bitácora)')
    errors = [f'Falta documento afectado en diff: {p}' for p in required if p not in docs and not p.startswith('una página')]
    if 'una página temática de aikya/docs/ (además de la bitácora)' in required:
        errors.append('Falta actualizar al menos un documento temático de aikya/docs/.')
    logs = [p for p in docs if re.fullmatch(r'aikya/docs/changes/REQ-\d{8}-[a-f0-9]{8}\.md',p)]
    if not logs:
        errors.append('Falta al menos un aikya/docs/changes/REQ-*.md en el diff.')
    return not errors,errors or ['Validación estructural de documentación del diff: OK.']


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description='Validar cobertura documental por petición/CI')
    parser.add_argument('mode',choices=['base','status','ci'])
    parser.add_argument('--session',default='',help='ID de sesión (vacío: auto si sólo hay un estado local)')
    parser.add_argument('--base')
    args=parser.parse_args(argv)
    base_errors=validate_base()
    if base_errors:
        print('\n'.join(base_errors),file=sys.stderr)
        return 1
    if args.mode=='base':
        print('Estructura documental: OK')
        return 0
    if args.mode=='ci':
        if not args.base:
            print('--base requerido para CI; no se omite validación.',file=sys.stderr)
            return 2
        try:
            ok,messages=validate_ci(git_changed(args.base))
        except (OSError,ValueError,subprocess.TimeoutExpired) as exc:
            print(str(exc),file=sys.stderr)
            return 2
    else:
        session=args.session
        if not session:
            candidates=list(STATE.glob('*.json')) if STATE.exists() else []
            if len(candidates)==1:
                session=candidates[0].stem
            else:
                print(f'Se encontraron {len(candidates)} sesiones: indica --session <id>.',file=sys.stderr)
                return 2
        state=load_state(session)
        if state is None:
            print('No se encontró la petición activa. Ejecuta /documentation-sync.',file=sys.stderr)
            return 2
        ok,messages=validate_request(state)
    print('\n'.join(messages))
    return 0 if ok else 1

if __name__=='__main__':
    sys.exit(main())
