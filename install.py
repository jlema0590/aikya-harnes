#!/usr/bin/env python3
"""Instalador/entrevista de Aikya Harness. Python 3.9+, solo stdlib.

Scaffolding de aplicaciones es asistido. Skills de terceros requieren aprobación explícita; no lee secretos ni modifica Git.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any
from doc_bootstrap import pages as doc_pages, infra_files
from external_skills import enabled_names, planned_commands, install_all
from aikya_layout import LAYOUTS, app_count, layout_of, validate_layout

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'template'
# SHA-256 de archivos v3 distribuidos sin modificaciones; actualizaciones solo si coinciden exactamente.
V3_TEMPLATE_HASHES = {'scripts/harness/docs_guard.py': '7d67e06379ecc06f59aefdcdde5a81def7b52e47ae904b5a0c0c50d7d205650c', '.claude/agents/frontend-engineer.md': '528a8a1f85da49eea133d14917b70ba51e1ba170833282826bf06ae6f8f062e0', '.claude/agents/mobile-engineer.md': '224a031ae5293358ae642ac87aab2965c7c288bde1cab76233eb2b47308f44d5', '.claude/skills/documentation-sync/SKILL.md': 'eea913b37aa59a7928b45c9820da1e86976331225ea71367199e4baadbeebcbf', '.claude/skills/architecture-review/SKILL.md': 'ee132fb1e1c864b3d897418c999d17ffbe5ccfde2031fb2e64c34f6267acef24', '.claude/skills/bugfix/SKILL.md': 'f888b8594854b63dc73ddad950fbf89c1b775818accfbc603f3d8bf9546c93d4', '.claude/skills/feature/SKILL.md': '87912f2ba37452551e712f00e9de0edded8d9d15420567640ff77bf37de90b9c'}
CANDIDATE_DIRS = ('', 'api', 'backend', 'server', 'web', 'frontend', 'client',
                  'mobile', 'android', 'ios', 'apps/api', 'apps/web', 'apps/mobile',
                  'apps/android', 'apps/ios', 'apps/mobile/android', 'apps/mobile/ios', 'platforms/android', 'platforms/ios',
                  'packages/api', 'packages/web', 'mobile/android', 'mobile/ios')
BACKENDS = ['none', 'java', 'dotnet', 'node', 'next', 'python']
FRONTENDS = ['none', 'react', 'vue', 'angular']
MOBILES = ['none', 'android', 'ios', 'both']
FRAMEWORKS = ['native', 'flutter', 'react-native']
ARCHS = ['existing', 'modular-monolith', 'layered', 'hexagonal', 'clean', 'microservices', 'undecided']
DATABASES = ['undecided', 'none', 'postgresql', 'mysql', 'sqlserver', 'sqlite', 'mongodb', 'other']
CIS = ['undecided', 'github-actions', 'gitlab-ci', 'azure-pipelines', 'jenkins', 'none']
DEPLOYS = ['undecided', 'docker', 'kubernetes', 'serverless', 'cloud-managed', 'app-stores', 'none']
PACKAGES = ['npm', 'pnpm', 'yarn', 'bun']
API_STYLES = ['undecided', 'rest', 'graphql', 'grpc']
AUTH = ['undecided', 'oidc-oauth2', 'jwt', 'session', 'external-idp', 'none']
OBSERVABILITY = ['undecided', 'opentelemetry', 'structured-logging', 'none']
TEST_STYLES = ['unit', 'unit+integration', 'unit+integration+e2e']
RENDERING = ['undecided', 'spa', 'ssr', 'ssg', 'hybrid']



def root_directories(root: Path) -> list[Path]:
    return [p for rel in CANDIDATE_DIRS if (p := root / rel).is_dir()]


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix() or '.'


def read_json_safe(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding='utf8'))
        return value if isinstance(value, dict) else {}
    except (OSError, UnicodeError, ValueError):
        return {}


def detect_project(root: Path) -> dict[str, Any]:
    """Detección conservadora basada en nombres/manifiestos; no ejecuta comandos."""
    modules: list[dict[str, Any]] = []
    findings: list[str] = []
    seen: set[tuple[str, str, str]] = set()

    def add(role: str, technology: str, folder: Path, detail: str = '') -> None:
        key = (role, technology, relative(root, folder))
        if key not in seen:
            seen.add(key)
            modules.append({'role': role, 'technology': technology, 'path': key[2]})
            findings.append(f'{technology} ({role}) en {key[2]}' + (f' — {detail}' if detail else ''))

    for folder in root_directories(root):
        pkgpath = folder / 'package.json'
        if pkgpath.is_file():
            pkg = read_json_safe(pkgpath)
            declared = pkg.get('dependencies') or {}
            dev = pkg.get('devDependencies') or {}
            deps = {**(declared if isinstance(declared, dict) else {}), **(dev if isinstance(dev, dict) else {})}
            if '@angular/core' in deps:
                add('frontend', 'angular', folder)
            if 'next' in deps:
                add('backend', 'next', folder, 'Next.js, puede ser full-stack')
                add('frontend', 'react', folder, 'integrado en Next.js')
            elif any(k in deps for k in ('react-native', 'expo')):
                add('mobile', 'react-native', folder)
            else:
                if any(k in deps for k in ('express', 'fastify', '@nestjs/core', 'koa', 'hono')):
                    add('backend', 'node', folder)
                if 'react' in deps:
                    add('frontend', 'react', folder)
                if 'vue' in deps or 'nuxt' in deps:
                    add('frontend', 'vue', folder)
            if not deps:
                findings.append(f'package.json encontrado en {relative(root, folder)} (framework desconocido)')
        if (folder / 'pyproject.toml').is_file() or (folder / 'requirements.txt').is_file():
            add('backend', 'python', folder, 'Verificar framework y entorno virtual')
        if (folder / 'pom.xml').exists():
            add('backend', 'java', folder, 'Maven; confirmar tipo de aplicación')
        if (folder / 'build.gradle').exists() or (folder / 'build.gradle.kts').exists():
            is_android = (folder / 'app/src/main/AndroidManifest.xml').exists() or (folder / 'src/main/AndroidManifest.xml').exists()
            if is_android:
                add('mobile', 'android', folder)
            elif not (folder / 'pom.xml').exists():
                add('backend', 'java', folder, 'Gradle; confirmar tipo de aplicación')
        if (folder / 'app/src/main/AndroidManifest.xml').exists():
            add('mobile', 'android', folder)
        for project in sorted(folder.glob('*.csproj'))[:5]:
            add('backend', 'dotnet', folder, project.name)
        if any(folder.glob('*.xcodeproj')) or any(folder.glob('*.xcworkspace')):
            add('mobile', 'ios', folder)
        if (folder / 'pubspec.yaml').exists():
            add('mobile', 'flutter', folder)
    if not modules:
        findings.append('No se pudo identificar un framework con suficiente confianza.')
    return {'modules': modules, 'findings': findings}


def choice(question: str, values: list[str], default: str) -> str:
    while True:
        print(f'\n{question}')
        for idx, value in enumerate(values, 1):
            print(f'  {idx}. {value}' + (' [por defecto]' if value == default else ''))
        entered = input('Selecciona número o nombre (Enter = recomendado): ').strip().lower()
        if not entered:
            return default
        if entered.isdigit() and 1 <= int(entered) <= len(values):
            return values[int(entered)-1]
        if entered in values:
            return entered
        print('Opción no válida; vuelve a intentarlo.')


def ask(question: str, default: str = '') -> str:
    answer = input(f'{question}' + (f' [{default}]' if default else '') + ': ').strip()
    return answer or default


def yesno(question: str, default: bool = True) -> bool:
    while True:
        value = input(f'{question} [{"S/n" if default else "s/N"}]: ').strip().lower()
        if not value:
            return default
        if value in ('s', 'si', 'sí', 'y', 'yes'):
            return True
        if value in ('n', 'no'):
            return False
        print('Responde s o n.')


def interview(target: Path, detected: dict[str, Any]) -> dict[str, Any]:
    print('\n=== ENTREVISTA TÉCNICA — AIKYA HARNESS ===')
    print('Detección inicial (son indicios, no resultados de build ni pruebas):')
    for finding in detected['findings']:
        print(' -', finding)
    nonempty = target.exists() and any(target.iterdir())
    mode = choice('Tipo de instalación', ['existing', 'new'], 'existing' if nonempty else 'new')
    technologies = {role: next((m['technology'] for m in detected['modules'] if m['role'] == role), 'none')
                    for role in ('backend', 'frontend', 'mobile')}
    mobile_detected = technologies['mobile']
    mobile_default = 'both' if mobile_detected in ('flutter', 'react-native') else ('android' if mobile_detected == 'android' else ('ios' if mobile_detected == 'ios' else 'none'))
    backend = choice('Backend principal', BACKENDS, technologies['backend'] if mode == 'existing' else 'none')
    frontend = choice('Frontend web', FRONTENDS, technologies['frontend'] if mode == 'existing' else ('react' if backend == 'next' else 'none'))
    mobile = choice('Plataformas móviles', MOBILES, mobile_default if mode == 'existing' else 'none')
    framework = 'none'
    android_language = 'none'
    ios_ui = 'none'
    if mobile != 'none':
        default_framework = mobile_detected if mobile_detected in ('flutter','react-native') else 'native'
        framework = choice('Estrategia de desarrollo móvil', FRAMEWORKS, default_framework)
        if framework == 'native' and mobile in ('android', 'both'):
            android_language = choice('Lenguaje Android', ['kotlin', 'java'], 'kotlin')
        if framework == 'native' and mobile in ('ios', 'both'):
            ios_ui = choice('Tecnología interfaz iOS', ['swiftui', 'uikit'], 'swiftui')
    if backend == 'none' and frontend == 'none' and mobile == 'none':
        raise ValueError('Selecciona al menos un backend, frontend o plataforma móvil.')
    frameworks = {
        'java': ['undecided','spring-boot','quarkus','micronaut'],
        'python': ['undecided','fastapi','django','flask'],
        'dotnet': ['undecided','aspnet-core','minimal-api'],
        'node': ['undecided','nestjs','fastify','express','hono'],
        'next': ['next-app-router'],
        'none': ['none'],
    }
    backend_framework = choice('Framework de backend', frameworks[backend], frameworks[backend][1] if backend in ('java','dotnet','next') else frameworks[backend][0]) if backend != 'none' else 'none'
    api_style = choice('Estilo de API', API_STYLES, 'rest') if backend != 'none' else 'undecided'
    frontend_rendering = choice('Estrategia de renderizado web', RENDERING, 'hybrid' if backend=='next' and frontend=='react' else 'spa') if frontend != 'none' else 'undecided'
    layout = choice('Topología del repositorio', list(LAYOUTS),
                    'monorepo' if app_count({'backend':backend, 'frontend':frontend, 'mobile':mobile, 'mobile_framework':framework}) > 1 or (target/'apps').is_dir() else 'singlerepo')
    arch = choice('Arquitectura preferida (en existing, se respeta la observada)', ARCHS,
                  'existing' if mode == 'existing' else 'modular-monolith')
    event_driven = yesno('¿El proyecto necesita eventos asíncronos como estilo complementario?', False)
    database = choice('Base de datos', DATABASES, 'undecided')
    ci = choice('Integración continua', CIS, 'undecided')
    deployment = choice('Destino de despliegue', DEPLOYS, 'app-stores' if mobile != 'none' and backend == frontend == 'none' else 'undecided')
    pkg_mgr = choice('Gestor JS (si aplica)', PACKAGES, 'npm') if backend in ('node','next') or frontend != 'none' or framework == 'react-native' else 'none'
    auth = choice('Identidad/autenticación', AUTH, 'undecided')
    telemetry = choice('Observabilidad', OBSERVABILITY, 'opentelemetry' if backend != 'none' else 'undecided')
    quality = choice('Estrategia de pruebas', TEST_STYLES, 'unit+integration')
    versions = ask('Versiones/SDKs que necesitas fijar (vacío = por decidir)', '')
    return {'mode': mode, 'repository_layout':layout, 'name': ask('Nombre del producto/proyecto', target.name),
            'backend': backend, 'frontend': frontend, 'mobile': mobile,
            'mobile_framework': framework, 'backend_framework':backend_framework, 'api_style':api_style,
            'frontend_rendering':frontend_rendering, 'auth':auth, 'observability':telemetry,
            'runtime_versions':versions, 'android_language': android_language,
            'ios_ui': ios_ui, 'architecture': arch,
            'architecture_patterns':['event-driven'] if event_driven else [], 'database': database,
            'ci': ci, 'deployment': deployment, 'package_manager': pkg_mgr,
            'quality': quality, 'notes': ask('Restricciones técnicas o convenciones adicionales (opcional)', '')}


def validated(data: dict[str, Any], target: Path) -> dict[str, Any]:
    choices = {'mode': ['existing','new'], 'repository_layout': list(LAYOUTS), 'backend': BACKENDS, 'frontend': FRONTENDS,
               'mobile': MOBILES, 'mobile_framework': ['none']+FRAMEWORKS,
               'android_language':['none','kotlin','java'], 'ios_ui':['none','swiftui','uikit'],
               'architecture': ARCHS, 'database':DATABASES, 'ci':CIS,
               'deployment':DEPLOYS, 'package_manager':['none']+PACKAGES,
               'api_style': API_STYLES, 'auth':AUTH, 'observability':OBSERVABILITY,
               'quality':TEST_STYLES, 'frontend_rendering':RENDERING}
    defaults = {'mode':'new', 'repository_layout':'monorepo', 'backend':'none', 'frontend':'none', 'mobile':'none',
                'mobile_framework':'none', 'android_language':'none', 'ios_ui':'none',
                'architecture':'undecided', 'database':'undecided', 'ci':'undecided',
                'deployment':'undecided', 'package_manager':'npm',
                'quality':'unit+integration', 'notes':'', 'name':target.name,
                'api_style':'undecided', 'auth':'undecided', 'observability':'undecided',
                'backend_framework':'undecided', 'frontend_rendering':'undecided', 'runtime_versions':'',
                'architecture_patterns':[]}
    result = {**defaults, **data}
    for field, values in choices.items():
        if result[field] not in values:
            raise ValueError(f'{field}={result[field]!r} no válido. Opciones: {values}')
    if not any(result[k] != 'none' for k in ('backend','frontend','mobile')):
        raise ValueError('Debes elegir algún backend, frontend o plataforma móvil.')
    if result['mobile'] == 'none':
        for k in ('mobile_framework','android_language','ios_ui'):
            result[k] = 'none'
    elif result['mobile_framework'] == 'none':
        raise ValueError('Selecciona mobile_framework al habilitar Android/iOS.')
    if result['mobile_framework'] != 'native':
        result['android_language'] = 'none'
        result['ios_ui'] = 'none'
    patterns = result.get('architecture_patterns', [])
    if not isinstance(patterns, list) or any(v != 'event-driven' for v in patterns) or len(patterns) != len(set(patterns)):
        raise ValueError('architecture_patterns sólo admite una lista sin duplicados de event-driven.')
    if not isinstance(result['name'], str) or not result['name'].strip():
        raise ValueError('name debe ser texto no vacío.')
    if not isinstance(result['notes'], str) or not isinstance(result['runtime_versions'], str):
        raise ValueError('notes y runtime_versions deben ser texto.')
    frameworks = {'none':['none','undecided'], 'java':['undecided','spring-boot','quarkus','micronaut'],
                  'python':['undecided','fastapi','django','flask'],
                  'dotnet':['undecided','aspnet-core','minimal-api'],
                  'node':['undecided','nestjs','fastify','express','hono'],
                  'next':['undecided','next-app-router']}
    if result['backend_framework'] not in frameworks[result['backend']]:
        raise ValueError('backend_framework no coincide con backend.')
    validate_layout(result)
    return result


def package_command(manager: str, script: str) -> list[str]:
    return {'npm': ['npm','run',script], 'pnpm':['pnpm','run',script],
            'yarn':['yarn',script], 'bun':['bun','run',script]}[manager]


def manager_for(folder: Path, fallback: str) -> str:
    if (folder / 'pnpm-lock.yaml').exists():
        return 'pnpm'
    if (folder / 'yarn.lock').exists():
        return 'yarn'
    if (folder / 'bun.lockb').exists() or (folder / 'bun.lock').exists():
        return 'bun'
    if (folder / 'package-lock.json').exists():
        return 'npm'
    return fallback if fallback in PACKAGES else 'npm'


def make_checks(root: Path, profile: dict[str, Any], modules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """No inventar comandos sin manifiesto ni tests sin scripts."""
    checks: list[dict[str, Any]] = []
    def add(name: str, command: list[str] | None, cwd: str='.', required: bool=False) -> None:
        if not any(x['name'] == name for x in checks):
            checks.append({'name': name, 'command': command, 'cwd': cwd, 'required': required})
    if profile['mode'] == 'new':
        roles=[('backend',profile['backend']), ('frontend', profile['frontend'])]
        if profile['mobile']=='both':
            roles.extend([('android','android'),('ios','ios')])
        else:
            roles.append(('mobile',profile['mobile']))
        for role, name in roles:
            if role == 'frontend' and profile['backend'] == 'next' and name == 'react':
                continue  # React pertenece a Next; un solo proyecto y set de gates
            if name != 'none':
                add(f'{role}:test', None, required=True)
                add(f'{role}:lint', None)
                add(f'{role}:build', None)
        return checks

    for module in modules:
        if module['role'] == 'frontend' and module['technology'] == 'react' and any(
            m['role'] == 'backend' and m['technology'] == 'next' and m['path'] == module['path'] for m in modules):
            continue  # Next.js y React integrado: evitar ejecutar dos veces los mismos scripts
        folder = root / module['path']
        role, tech = module['role'], module['technology']
        suffix = f'{role}:{tech}:{module["path"]}'
        if (folder / 'package.json').exists() and tech in ('node','next','react','vue','angular','react-native'):
            pkg = read_json_safe(folder / 'package.json')
            scripts = pkg.get('scripts') or {}
            scripts = scripts if isinstance(scripts, dict) else {}
            manager = manager_for(folder, profile['package_manager'])
            for task in ('lint','test','build','typecheck'):
                content = scripts.get(task)
                supported = isinstance(content, str) and 'no test specified' not in content.lower()
                add(f'{suffix}:{task}', package_command(manager,task) if supported else None,
                    module['path'], required=(task=='test'))
        elif tech == 'java':
            if (folder / 'pom.xml').exists():
                launcher = './mvnw' if (folder / 'mvnw').exists() else 'mvn'
                add(f'{suffix}:test', [launcher,'test'], module['path'], True)
                add(f'{suffix}:build', [launcher,'-DskipTests','package'], module['path'])
            elif (folder / 'gradlew').exists():
                add(f'{suffix}:test', ['./gradlew','test'], module['path'], True)
                add(f'{suffix}:build', ['./gradlew','build'], module['path'])
            else:
                add(f'{suffix}:test', None, module['path'], True)
        elif tech == 'python':
            # Sólo ejecutamos pytest cuando existe en la configuración conocida.
            if (folder / 'pytest.ini').is_file() or (folder / 'pyproject.toml').is_file():
                add(f'{suffix}:test', [sys.executable,'-m','pytest'], module['path'], True)
            else:
                add(f'{suffix}:test', None, module['path'], True)
        elif tech == 'dotnet':
            projects = sorted(folder.glob('*.csproj'))
            target = [projects[0].name] if len(projects) == 1 else []
            add(f'{suffix}:test', ['dotnet','test',*target], module['path'], True)
            add(f'{suffix}:build', ['dotnet','build',*target], module['path'])
        else:
            # Android/iOS: son necesarias variantes/schemes/simulador reales.
            add(f'{suffix}:test', None, module['path'], True)
            add(f'{suffix}:build', None, module['path'])
    if not checks:
        add('project:test', None, required=True)
    return checks


def safe_write(path: Path, content: str, actions: list[str], *, replace_managed: bool=False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if replace_managed and path.is_file() and path.read_text(encoding='utf8').startswith('<!-- GENERATED BY AIKYA-HARNESS -->'):
            path.write_text(content, encoding='utf8')
            actions.append('ACTUALIZADO ' + str(path))
        elif path.is_file() and path.read_text(encoding='utf8') == content:
            actions.append('IGUAL ' + str(path))
        else:
            actions.append('CONSERVADO (sin sobrescribir) ' + str(path))
        return
    path.write_text(content, encoding='utf8')
    actions.append('CREADO ' + str(path))


def merge_settings(target: Path, actions: list[str]) -> None:
    source = read_json_safe(TEMPLATE / '.claude/settings.json')
    path = target / '.claude/settings.json'
    if not path.exists():
        safe_write(path, json.dumps(source, indent=2, ensure_ascii=False)+'\n', actions)
        return
    try:
        local = json.loads(path.read_text(encoding='utf8'))
        if not isinstance(local, dict):
            raise ValueError('settings.json no es objeto JSON')
    except (ValueError, OSError, UnicodeError) as exc:
        safe_write(target / '.harness/settings.harness-proposed.json', json.dumps(source, indent=2)+'\n', actions)
        actions.append(f'AVISO settings.json inválido: {exc}; no modificado')
        return
    merged = json.loads(json.dumps(local))
    perms = merged.setdefault('permissions', {})
    if not isinstance(perms, dict):
        actions.append('AVISO permissions existente no es objeto; revisar manualmente')
        return
    for section in ('ask','deny'):
        items = perms.setdefault(section, [])
        if not isinstance(items, list):
            actions.append(f'AVISO permissions.{section} no es lista; revisar manualmente')
            return
        for rule in source['permissions'].get(section, []):
            if rule not in items:
                items.append(rule)
    hooks = merged.setdefault('hooks', {})
    if not isinstance(hooks, dict):
        actions.append('AVISO hooks existente no es objeto; revisar manualmente')
        return
    for event, groups in source['hooks'].items():
        theirs = hooks.setdefault(event, [])
        if not isinstance(theirs, list):
            actions.append(f'AVISO hooks.{event} no es lista; revisar manualmente')
            return
        for group in groups:
            cmd = group['hooks'][0]['command']
            exists = any(isinstance(g, dict) and any(h.get('command') == cmd for h in g.get('hooks', []) if isinstance(h, dict)) for g in theirs)
            if not exists:
                theirs.append(group)
    if merged != local:
        path.write_text(json.dumps(merged, indent=2, ensure_ascii=False)+'\n', encoding='utf8')
        actions.append('FUSIONADO (sin eliminar reglas previas) ' + str(path))
    else:
        actions.append('SIN CAMBIOS ' + str(path))


def md_text(value: Any) -> str:
    return str(value).replace('\n', ' ').replace('\r', ' ').replace('`', "'").strip()


def context_markdown(profile: dict[str, Any], modules: list[dict[str, Any]]) -> str:
    rows = '\n'.join(f'- {md_text(m["role"])}: **{md_text(m["technology"])}** (`{md_text(m["path"])}`)' for m in modules)
    if not rows:
        rows = '- Repositorio nuevo; aún no hay framework implementado ni comandos verificados.'
    return f'''<!-- GENERATED BY AIKYA-HARNESS -->
# Perfil técnico — {md_text(profile['name'])}

> Entrevista de instalación. El perfil expresa **decisiones**, no garantiza dependencias instaladas ni que el código exista.

| Aspecto | Decisión |
|---|---|
| Modalidad | {md_text(profile['mode'])} |
| Topología del repositorio | {md_text(layout_of(profile))} |
| Backend | {md_text(profile['backend'])} |
| Framework backend | {md_text(profile['backend_framework'])} |
| Estilo de API | {md_text(profile['api_style'])} |
| Frontend web | {md_text(profile['frontend'])} |
| Renderizado web | {md_text(profile['frontend_rendering'])} |
| Plataforma móvil | {md_text(profile['mobile'])} |
| Framework móvil | {md_text(profile['mobile_framework'])} |
| Android | {md_text(profile['android_language'])} |
| UI iOS | {md_text(profile['ios_ui'])} |
| Arquitectura | {md_text(profile['architecture'])} |
| Patrones complementarios | {md_text(', '.join(profile.get('architecture_patterns', [])) or 'ninguno')} |
| Versiones/SDK | {md_text(profile['runtime_versions']) or 'Por decidir'} |
| Autenticación | {md_text(profile['auth'])} |
| Observabilidad | {md_text(profile['observability'])} |
| Persistencia | {md_text(profile['database'])} |
| CI | {md_text(profile['ci'])} |
| Despliegue | {md_text(profile['deployment'])} |
| Gestor JS | {md_text(profile['package_manager'])} |
| Estrategia de pruebas | {md_text(profile['quality'])} |

## Módulos detectados durante instalación (indicios, no validación)
{rows}

## Restricciones acordadas
{md_text(profile['notes']) or 'No declaradas.'}

## Instrucciones permanentes para Claude Code
- En repositorio existente: inspeccionar el código real antes de proponer cambios; si contradice el perfil, comunicar la divergencia.
- En proyecto nuevo: establecer primero estructura, contratos, versiones y comandos de scaffold; solicitar confirmación antes de ejecutar creadores remotos o instalar dependencias.
- Crear apps/, contracts/ y packages/ únicamente en monorepo; en singlerepo generar la única aplicación en la raíz y mantener Aikya en aikya/.
- Para Next.js, usar Route Handlers / Server Actions según arquitectura y exposición, no asumir que equivale a un backend independiente por defecto.
- Para Android, usar convenciones Kotlin/Java y lifecycle; para iOS, Swift, signing y Xcode; para Flutter/React Native, contemplar ambas plataformas y pruebas reales.
- No atribuir éxito a builds, testing de simulador, firma o publicación sin ejecutarlos.
- Los tests exigidos no configurados deben quedar como **NO VERIFICADO**.
'''


def project_bootstrap(profile: dict[str, Any]) -> str:
    lines = ['<!-- GENERATED BY AIKYA-HARNESS -->',
             '# Guía de inicialización del proyecto', '',
             'Esta guía **no ejecuta** comandos. Confirma versiones, directorios y nombres antes de crear los proyectos.',
             'Las herramientas deben estar instaladas previamente. Los comandos pueden descargar dependencias.', '']
    backend = profile['backend']
    frontend = profile['frontend']
    mobile = profile['mobile']
    if backend == 'java':
        java_options = {
            'spring-boot': ('Spring Initializr', 'https://start.spring.io'),
            'quarkus': ('Quarkus code generator', 'https://code.quarkus.io'),
            'micronaut': ('Micronaut Launch', 'https://launch.micronaut.io'),
            'undecided': ('generador oficial del framework elegido', 'https://start.spring.io'),
        }
        generator, url = java_options[profile['backend_framework']]
        lines += ['## Backend Java', f'Genera el proyecto con **{generator}** ({url}) y Maven o Gradle.',
                  'Selecciona Java compatible, paquetes y dependencias necesarias; coloca el proyecto en `apps/api`.',
                  'No fijamos versión de Java o framework sin confirmar compatibilidad.', '']
    elif backend == 'python':
        lines += ['## Backend Python',
                  f'Framework acordado: **{profile["backend_framework"]}**. Crear entorno virtual y proyecto en `apps/api` con generador/documentación oficial apropiada,',
                  'sin instalar paquetes ni fijar versiones sin confirmación. Validar Python y gestor de dependencias antes del scaffold.', '']
    elif backend == 'dotnet':
        lines += ['## Backend .NET / ASP.NET Core', '```bash', 'dotnet new webapi -o apps/api', '```',
                  'Confirma antes el SDK soportado con `dotnet --list-sdks`.', '']
    elif backend == 'node':
        lines += ['## Backend Node.js', f'Framework acordado: **{profile["backend_framework"]}**; si es undecided, elige Express, Fastify, NestJS o Hono. **Node.js es runtime, no framework**.',
                  'Configura TypeScript, test runner y scripts reales en `apps/api/package.json`.', '']
    elif backend == 'next':
        lines += ['## Next.js (backend BFF o aplicación full-stack)', '```bash',
                  'npx create-next-app@latest apps/web', '```',
                  'Next incluye React: si se eligió React, normalmente **no necesitas otro frontend**; si Vue, implica app separada.', '']
    if frontend in ('react','vue') and backend != 'next':
        template = 'react-ts' if frontend == 'react' else 'vue-ts'
        lines += [f'## Frontend {frontend.title()} con Vite', '```bash',
                  f'npm create vite@latest apps/web -- --template {template}', '```',
                  'Adapta el gestor de paquetes a la decisión de la entrevista.', '']
    elif frontend == 'angular':
        lines += ['## Frontend Angular', 'Utiliza Angular CLI compatible con el Node.js seleccionado,',
                  'dentro de `apps/web` (o `apps/frontend` cuando el backend es Next.js).',
                  'Planifica y autoriza cualquier instalación de CLI/dependencias. Evita añadir versiones no verificadas.', '']
    elif frontend == 'vue' and backend == 'next':
        lines += ['## Vue desacoplado de Next.js', '```bash',
                  'npm create vite@latest apps/frontend -- --template vue-ts', '```',
                  'Separar API en Next.js y SPA Vue requiere definir CORS, autenticación, rutas y despliegue.', '']
    if mobile != 'none':
        fw = profile['mobile_framework']
        lines += ['## Aplicación móvil']
        if fw == 'native':
            if mobile in ('android','both'):
                lines += ['- **Android:** crea el proyecto en Android Studio (Empty Activity, Kotlin/Java conforme al perfil), Gradle/AGP compatibles.']
            if mobile in ('ios','both'):
                lines += ['- **iOS:** crea el proyecto en Xcode con SwiftUI o UIKit conforme al perfil; para compilar iOS necesitas macOS/Xcode.']
        elif fw == 'flutter':
            platforms = 'android,ios' if mobile == 'both' else mobile
            lines += ['```bash', f'flutter create --platforms={platforms} apps/mobile', '```',
                      'Comprueba antes `flutter doctor`; generación iOS requiere macOS para el toolchain correspondiente.']
        else:
            lines += ['Usa el generador oficial vigente de **React Native / Expo**, previa validación de Node y SDKs; concreta Expo vs bare antes del scaffold.']
        lines += ['', 'Configura variantes, schemes, dispositivos/simuladores, certificados de firma y pruebas antes de completar quality gates.', '']
    lines += ['## Activación de verificaciones',
              '1. Genera el código usando la herramienta oficial apropiada y revisa sus archivos.',
              '2. Ajusta `harness.json`: reemplaza cada `command: null` con un comando real que funcione en ese módulo.',
              '3. Ejecuta `python3 aikya/scripts/harness/run_checks.py` y registra evidencias.',
              '4. Desde Claude Code, continúa con `/aikya-feature` o `/aikya-quality`.', '']
    guide = '\n'.join(lines) + '\n'
    if layout_of(profile) == 'singlerepo':
        for folder in ('apps/api','apps/web','apps/frontend','apps/mobile','apps/android','apps/ios'):
            guide = guide.replace(folder, '.')
        guide += '\nScaffold de singlerepo: generar temporalmente, revisar conflictos y trasladar a la raíz sin sobrescribir archivos preexistentes.\n'
    return guide


def copy_legacy_docs(target: Path, actions: list[str]) -> None:
    """Copiar documentación anterior sin eliminar ni sobrescribir fuentes del usuario."""
    source_dir = target/'docs'
    target_dir = target/'aikya/docs'
    if not source_dir.is_dir() or source_dir.is_symlink():
        return
    for old in sorted(source_dir.rglob('*')):
        if not old.is_file() or old.is_symlink():
            continue
        new = target_dir / old.relative_to(source_dir)
        if new.exists() or any(x.is_symlink() for x in (new, *new.parents) if x != target.parent and target in (x, *x.parents)):
            actions.append('CONSERVADO legacy sin migrar: '+str(old))
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(old,new)
        actions.append('COPIADO docs legacy a aikya/docs (original conservado): '+str(new))


def install(target: Path, profile: dict[str, Any], detected: dict[str, Any], dry_run: bool=False) -> list[str]:
    """Instala sin sobrescribir archivos de usuario. Para dry-run no muta."""
    actions: list[str] = []
    validate_layout(profile)
    if dry_run:
        return [f'PLAN: instalar harness en {target}', 'PLAN: crear aikya/docs/, aikya/test/, aikya/scripts/ según '+layout_of(profile)+' y CI/infra', 'PLAN: incorporar hooks por petición + Stop gate y generar receta de scaffold opcional sin ejecutarla', 'PLAN: conservar documentos de usuario y módulos existentes; no instalar dependencias ni desplegar', 'PLAN: integrar Ponytail/Graphify y UI UX Pro Max sólo si hay frontend o móvil, previa aprobación']
    target.mkdir(parents=True, exist_ok=True)
    # Guardar un perfil estructurado: en reruns sólo actualizar si es del instalador.
    profile_path = target / '.harness/project-profile.json'
    payload = {'_generated_by':'claude-dev-harness-interactive', 'schema_version':1,
               'decisions':profile, 'detected':detected}
    if profile_path.exists():
        old = read_json_safe(profile_path)
        if old.get('_generated_by') != 'claude-dev-harness-interactive':
            actions.append('CONSERVADO perfil ajeno: '+str(profile_path))
        else:
            profile_path.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
            actions.append('ACTUALIZADO '+str(profile_path))
    else:
        safe_write(profile_path, json.dumps(payload,indent=2,ensure_ascii=False)+'\n',actions)
    for source in sorted(TEMPLATE.rglob('*')):
        if not source.is_file() or '__pycache__' in source.parts or source.suffix == '.pyc':
            continue
        rel = source.relative_to(TEMPLATE)
        if rel.as_posix() in ('CLAUDE.md','harness.json','.claude/settings.json'):
            continue
        dest = target / (Path('aikya/scripts') / Path(*rel.parts[1:]) if rel.parts[0]=='scripts' else Path('aikya/test') / Path(*rel.parts[1:]) if rel.parts[0]=='tests' else rel)
        if dest.exists():
            old_hash = V3_TEMPLATE_HASHES.get(rel.as_posix())
            if old_hash and dest.is_file() and not dest.is_symlink() and hashlib.sha256(dest.read_bytes()).hexdigest() == old_hash:
                backup = target/'.harness/backup-v3'/rel
                backup.parent.mkdir(parents=True, exist_ok=True)
                if not backup.exists():
                    shutil.copy2(dest, backup)
                shutil.copy2(source,dest)
                actions.append('ACTUALIZADO DESDE v3 (backup creado) '+str(dest))
            else:
                actions.append('CONSERVADO (sin sobrescribir) '+str(dest))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            actions.append('CREADO '+str(dest))
    # Alias prefijados: se conservan los comandos heredados para compatibilidad.
    for original in sorted((TEMPLATE/'.claude/skills').glob('*/SKILL.md')):
        old_name=original.parent.name
        if old_name == 'project-bootstrap':
            continue  # Comando público renombrado a aikya-infra-project.
        if old_name.startswith('aikya-'):
            continue
        alias='aikya-'+old_name
        content=original.read_text(encoding='utf8').replace('name: '+old_name+'\n','name: '+alias+'\n',1)
        safe_write(target/'.claude/skills'/alias/'SKILL.md',content,actions)
    # Registrar todos los comandos gestionados Aikya cuando el proyecto se inicializa.
    # Los wrappers tienen la marca AIKYA BOOTSTRAP MANAGED y no sustituyen skills personalizadas.
    from aikya_setup import BOOTSTRAP_COMMANDS
    for name in BOOTSTRAP_COMMANDS:
        src=HERE/'aikya-skills'/name/'SKILL.md'
        dst=target/'.claude/skills'/name/'SKILL.md'
        if not src.is_file():
            continue
        if dst.exists() and not dst.is_symlink() and 'AIKYA BOOTSTRAP MANAGED' in dst.read_text(encoding='utf8'):
            if dst.read_bytes()!=src.read_bytes():
                dst.write_bytes(src.read_bytes())
                actions.append('ACTUALIZADO skill gestionada '+str(dst))
        elif not dst.exists():
            safe_write(dst,src.read_text(encoding='utf8'),actions)
    # Migrar únicamente wrappers anteriores que coinciden con los originales de Aikya.
    from aikya_setup import retire_legacy_commands
    for _scope in (target/'.aikya/runtime', HERE):
        if (_scope/'bootstrap_skills').is_dir():
            retire_legacy_commands(target/'.claude/skills',_scope,actions)
            break
    # v4 también generaba un alias sin marca gestionada, a partir de la skill interna.
    old_alias=target/'.claude/skills/aikya-project-bootstrap/SKILL.md'
    original=TEMPLATE/'.claude/skills/project-bootstrap/SKILL.md'
    if old_alias.is_file() and not old_alias.is_symlink() and original.is_file():
        expected=original.read_text(encoding='utf8').replace('name: project-bootstrap\n',
                                                               'name: aikya-project-bootstrap\n',1)
        if old_alias.read_text(encoding='utf8')==expected:
            old_alias.unlink()
            try: old_alias.parent.rmdir()
            except OSError: pass
            actions.append('RETIRADO alias anterior aikya-project-bootstrap')
    # Comandos no Aikya heredados permanecen disponibles en el proyecto.
    # Disponible también cuando Aikya se instaló desde la fuente sin bootstrap.
    requirements_file=HERE/'aikya_requirements.py'
    if requirements_file.is_file():
        safe_write(target/'aikya/scripts/harness/aikya_requirements.py',requirements_file.read_text(encoding='utf8'),actions)
    merge_settings(target, actions)
    claude = target / 'CLAUDE.md'
    if not claude.exists():
        safe_write(claude, (TEMPLATE/'CLAUDE.md').read_text(encoding='utf8') + '\n' +
                   '## Perfil técnico\nLee `.claude/rules/00-project-profile.md` antes de diseñar o modificar la aplicación.\n', actions)
    else:
        actions.append('CONSERVADO CLAUDE.md existente; el perfil se encuentra en .claude/rules/00-project-profile.md')
    safe_write(target/'.claude/rules/00-project-profile.md', context_markdown(profile,detected['modules']), actions, replace_managed=True)
    checks = [{'name':'docs:structure', 'command':['python3','aikya/scripts/harness/docs_guard.py','base'], 'cwd':'.', 'required':True}, {'name':'skills:format', 'command':['python3','aikya/scripts/harness/skills_lint.py'], 'cwd':'.', 'required':True}] + make_checks(target,profile,detected['modules'])
    safe_write(target/'harness.json',json.dumps({'schema_version':2,'checks':checks},indent=2,ensure_ascii=False)+'\n',actions)
    safe_write(target/'aikya/docs/harness/bootstrap.md',project_bootstrap(profile)+
        '\n## Bootstrap ejecutable, opcional\n\n'
        'Desde Claude Code utiliza `/aikya-scaffold plan` para revisar generadores soportados. '
        'La skill `/aikya-scaffold` ejecutará los generadores **sólo con aprobación expresa**: pueden descargar dependencias y crear código. '
        'Java y proyectos móviles nativos pueden requerir sus generadores gráficos oficiales.\n',
        actions,replace_managed=False)
    copy_legacy_docs(target,actions)
    for rel, content in doc_pages(profile,detected['modules']).items():
        safe_write(target/rel,content,actions)
    # Catálogo técnico importado y curado: copia assets sin ejecutarlos y activa sólo
    # los agentes/skills adecuados a las decisiones confirmadas de la entrevista.
    from engineering_catalog import discover, install_selected
    for original in sorted((HERE/'engineering').rglob('*')):
        if original.is_file() and not original.is_symlink():
            relative = original.relative_to(HERE/'engineering')
            safe_write(target/'aikya/scripts/harness/engineering'/relative,
                       original.read_text(encoding='utf8'), actions)
    safe_write(target/'aikya/scripts/harness/engineering_catalog.py',
               (HERE/'engineering_catalog.py').read_text(encoding='utf8'), actions)
    selected = discover(target, profile, detected['modules'])
    actions.extend(install_selected(target, selected, source=HERE/'engineering'))
    # Inventario local de skills (disponibles != invocadas); conserva documento personalizado.
    from skills_registry import write_inventory
    ok, note = write_inventory(target,profile)
    actions.append(('INVENTARIO ' if ok else 'AVISO ') + note)
    for rel, content in infra_files(profile).items():
        if rel == '.gitignore':
            ignore = target/'.gitignore'
            if not ignore.exists():
                safe_write(ignore,content,actions)
            else:
                old=ignore.read_text(encoding='utf8')
                extras=['.harness/state/', '.harness/welcome.json', 'graphify-out/', '.env', '.env.*', '!.env.example']
                missing=[x for x in extras if x not in old.splitlines()]
                if missing:
                    with ignore.open('a',encoding='utf8') as handle:
                        handle.write('\n# Claude Dev Harness v3 (estado local y secretos)\n'+'\n'.join(missing)+'\n')
                    actions.append('AMPLIADO (gitignore) '+str(ignore))
                else:
                    actions.append('SIN CAMBIOS '+str(ignore))
        else:
            safe_write(target/rel,content,actions)
    safe_write(target/'aikya/docs/harness/installer-readme.md',
        '<!-- GENERATED BY AIKYA-HARNESS -->\n# Instalación del harness\n\n'
        'Perfil de decisiones: `.harness/project-profile.json`.\n\n'
        'Reglas contextuales: `.claude/rules/00-project-profile.md`.\n\n'
        'Quality gates: `harness.json` y `/aikya-quality` dentro de Claude Code.\n\n'
        'Si ya existía `CLAUDE.md`, se ha conservado. Si existía `harness.json`, se ha conservado: revisa los checks manualmente.\n',
        actions,replace_managed=True)
    return actions


def only_aikya_bootstrap(target:Path) -> bool:
    """Allow new mode only if the directory contains bootstrap assets or answers.

    Global Aikya stores its runtime in HOME and writes only `.aikya/answers.json`
    to a new target; project-scope Aikya also has a managed local runtime.
    An unrelated code file or settings file will *always* reject new mode.
    """
    state=target/'.aikya'
    answers=state/'answers.json'
    marker=state/'bootstrap.json'
    local_bootstrap=(marker.is_file() and not marker.is_symlink() and
                     read_json_safe(marker).get('_generated_by')=='aikya-setup')
    answers_only=answers.is_file() and not answers.is_symlink() and bool(read_json_safe(answers))
    if not (local_bootstrap or answers_only):
        return False
    allowed_roots={'.git','.aikya'} | ({'.claude'} if local_bootstrap else set())
    if any(entry.name not in allowed_roots or entry.is_symlink() for entry in target.iterdir()):
        return False
    claude=target/'.claude'
    if claude.is_dir():
        from aikya_setup import BOOTSTRAP_COMMANDS
        safe={f'skills/{name}/SKILL.md' for name in BOOTSTRAP_COMMANDS}
        settings=claude/'settings.json'
        if settings.is_file() and not settings.is_symlink():
            raw=read_json_safe(settings)
            hooks=raw.get('hooks',{}).get('SessionStart',[]) if isinstance(raw.get('hooks',{}),dict) else []
            registered=any('aikya_session.py' in str(h.get('command',''))
                           for group in hooks if isinstance(group,dict)
                           for h in group.get('hooks',[]) if isinstance(h,dict))
            if registered:
                safe.add('settings.json')
        if any(entry.relative_to(claude).as_posix() not in safe for entry in claude.rglob('*') if entry.is_file()):
            return False
    permitted={'runtime','bootstrap.json','answers.json'} if local_bootstrap else {'answers.json'}
    if any(entry.name not in permitted or entry.is_symlink() for entry in state.iterdir()):
        return False
    return True


def main(argv: list[str]|None=None) -> int:
    parser=argparse.ArgumentParser(description='Entrevista técnica e instalador seguro para Claude Code')
    parser.add_argument('--target',type=Path,default=Path.cwd(),help='Repositorio existente o nuevo directorio')
    parser.add_argument('--answers',type=Path,help='Respuestas JSON para instalación no interactiva')
    parser.add_argument('--dry-run',action='store_true',help='Mostrar plan sin escribir archivos')
    parser.add_argument('--allow-bootstrap',action='store_true',help='Permitir new sólo con bootstrap Aikya verificado')
    parser.add_argument('--display-name',default=None,help='Nombre local que se muestra en el saludo de Claude Code (no se versiona)')
    parser.add_argument('--external',choices=['ask','install','plan','skip'],default=None,help='Skills de terceros: pedir consentimiento (terminal), instalar con consentimiento explícito, plan o saltar')
    args=parser.parse_args(argv)
    target=args.target.expanduser().resolve()
    if target.exists() and not target.is_dir():
        parser.error('--target debe ser un directorio')
    detected=detect_project(target) if target.exists() else {'modules':[],'findings':['Directorio nuevo.']}
    try:
        if args.answers:
            answers=read_json_safe(args.answers)
            if not answers:
                raise ValueError('Archivo --answers vacío/inválido o sin permisos.')
            profile=validated(answers,target)
            welcome_name = args.display_name if args.display_name is not None else answers.get('welcome_name', '')
        else:
            profile=validated(interview(target,detected),target)
            welcome_name = args.display_name if args.display_name is not None else ask(
                'Nombre para la bienvenida en Claude Code (vacío = git user.name)', '')
    except (ValueError,KeyboardInterrupt,EOFError) as exc:
        print(f'Entrevista cancelada o inválida: {exc}',file=sys.stderr)
        return 2
    if profile['mode']=='existing' and not target.exists():
        print('ERROR: mode=existing requiere una carpeta de proyecto existente.',file=sys.stderr)
        return 2
    if profile['mode']=='new' and target.exists() and any(target.iterdir()) and not (args.allow_bootstrap and only_aikya_bootstrap(target)):
        if args.answers:
            print('ERROR: mode=new requiere un directorio vacío (protección anti-sobrescritura).',file=sys.stderr)
            return 2
        print('El directorio de destino ya contiene archivos.')
        if not yesno('¿Continuar manteniendo los archivos sin sobrescribirlos?',False):
            return 2
    print('\n=== RESUMEN DE DECISIONES ===')
    print(json.dumps(profile,indent=2,ensure_ascii=False))
    if not args.answers and not args.dry_run and not yesno('¿Instalar el harness con este perfil?',True):
        print('Instalación cancelada. No se han creado archivos.')
        return 0
    try:
        actions=install(target,profile,detected,dry_run=args.dry_run)
    except (OSError,UnicodeError,ValueError) as exc:
        print(f'ERROR durante la instalación: {exc}',file=sys.stderr)
        return 1
    if not args.dry_run and welcome_name:
        if not isinstance(welcome_name, str) or not welcome_name.strip():
            print('AVISO: nombre de bienvenida inválido; no guardado.', file=sys.stderr)
        else:
            # La identidad es por usuario/equipo local, no forma parte del perfil compartido.
            welcome_file = target / '.harness/welcome.json'
            if welcome_file.is_symlink():
                print('AVISO: welcome.json es enlace simbólico; no modificado.', file=sys.stderr)
            else:
                welcome_file.parent.mkdir(parents=True, exist_ok=True)
                welcome_file.write_text(json.dumps({'display_name': welcome_name.strip()[:48]},
                    ensure_ascii=False, indent=2) + '\n', encoding='utf8')
                actions.append('IDENTIDAD LOCAL configurada en .harness/welcome.json (ignorado por Git)')
    print('\n=== RESULTADO ===')
    for a in actions:
        print('-',a)
    failed_external = False
    if not args.dry_run:
        policy = args.external or ('plan' if args.answers else 'ask')
        if policy in ('ask','install','plan'):
            print('\n=== AGENT SKILLS EXTERNAS ===')
            for command in planned_commands(profile):
                print('PLAN:', command)
        if policy == 'ask':
            policy = 'install' if yesno('¿Autorizar descarga y ejecución de instaladores oficiales de terceros?',False) else 'plan'
        if policy == 'install':
            print('\nInstalando skills externas seleccionadas ...')
            record = install_all(target, profile, permission=True)
            failed = [k for k,v in record.get('skills',{}).items() if v.get('state')=='failed']
            if failed:
                failed_external = True
                print('AVISO: instalaciones externas pendientes: '+', '.join(failed),file=sys.stderr)
                print('Desde Claude Code utiliza /aikya-skills-install, con autorización explícita.')
        elif policy == 'plan':
            print('Skills externas PENDIENTES; para instalarlas tras revisar procedencia:')
            print('Desde Claude Code utiliza /aikya-skills-install, con autorización explícita.')
        print('\nSiguiente: desde Claude Code ejecuta /aikya-doctor y /aikya-scaffold plan; luego /aikya-quality.')
    return 3 if failed_external else 0

if __name__=='__main__':
    sys.exit(main())
