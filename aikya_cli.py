#!/usr/bin/env python3
"""CLI de soporte de skills Aikya. La entrevista ocurre DENTRO de Claude Code."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import install as installer
from aikya_requirements import check, markdown


def resolved_answers(args, target:Path) -> Path:
    if args.answers:
        path=args.answers.expanduser().resolve()
    else:
        candidates=[target/'.aikya/answers.json',target/'.harness/project-profile.json']
        path=next((p for p in candidates if p.is_file()),candidates[0])
    if not path.is_file():
        raise ValueError(f'No hay respuestas en {path}; realiza /aikya-init o indica --answers.')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description='Aikya Harness · acciones ejecutadas por Claude Code')
    parser.add_argument('command',choices=['probe','requirements','init','answers','status','analyze'])
    parser.add_argument('--target',type=Path,default=Path.cwd())
    parser.add_argument('--answers',type=Path)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--strict',action='store_true',help='Requisitos incompletos generan exit 4')
    parser.add_argument('--external',choices=['skip','plan','install'],default='plan')
    parser.add_argument('--display-name')
    parser.add_argument('--scope',default='.')
    parser.add_argument('--focus',choices=['general','security','architecture','infrastructure','operations'],default='general')
    parser.add_argument('--refresh',action='store_true')
    parser.add_argument('--report-only',action='store_true')
    parser.add_argument('--approved',action='store_true',help='Explicit approval to create Aikya-owned files')
    args=parser.parse_args(argv)
    target=args.target.expanduser().resolve()
    if args.command=='analyze':
        from aikya_analyze import execute
        try:
            result=execute(target,scope=args.scope,focus=args.focus,
                           approved=args.approved,refresh=args.refresh,
                           dry_run=args.dry_run,report_only=args.report_only)
        except (ValueError,OSError,UnicodeError,TypeError) as exc:
            print('ERROR en análisis:',exc,file=sys.stderr)
            return 2
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['status']=='READY' else 4
    if args.command=='probe':
        detected=installer.detect_project(target) if target.exists() else {'modules':[],'findings':['Nuevo directorio']}
        print(json.dumps({'target':str(target),'detected':detected,
                          'existing_profile':installer.read_json_safe(target/'.harness/project-profile.json'),
                          'aikya_bootstrap':(target/'.aikya/bootstrap.json').is_file()},ensure_ascii=False,indent=2))
        return 0
    if args.command=='status':
        print(json.dumps({'configured':(target/'.harness/project-profile.json').is_file(),
           'docs':(target/'aikya/docs/README.md').is_file(),
           'answers':(target/'.aikya/answers.json').is_file()},indent=2))
        return 0
    try:
        source=resolved_answers(args,target)
        raw=json.loads(source.read_text(encoding='utf8'))
        profile=installer.validated(raw.get('decisions',raw),target)
    except (ValueError,OSError,UnicodeError,TypeError) as exc:
        print('ERROR en respuestas:',exc,file=sys.stderr)
        return 2
    if args.command=='init' and profile['mode']!='new':
        print('ERROR: /aikya-init sólo admite proyectos nuevos. Para repositorios existentes usa /aikya-analyze; no se escribieron archivos.',file=sys.stderr)
        return 2
    if args.command=='answers' and profile['mode']=='existing':
        print('AVISO: ruta declarativa legacy; para adopción automática y segura usa /aikya-analyze.',file=sys.stderr)
    report=check(profile,target)
    print('\n=== AIKYA · REQUISITOS DEL ENTORNO ===')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if args.command=='requirements':
        return 4 if args.strict and not report['ready'] else 0
    if args.strict and not report['ready']:
        print('REQUISITOS PENDIENTES: solicita permiso al desarrollador antes de actualizar SDKs.',file=sys.stderr)
        return 4
    # run through current process (same interpreter), never auto-install SDKs.
    flags=['--target',str(target),'--answers',str(source),'--external',args.external]
    if args.dry_run: flags.append('--dry-run')
    if args.display_name: flags+=['--display-name',args.display_name]
    if (target/'.aikya/bootstrap.json').exists() or (target/'.aikya/answers.json').exists(): flags.append('--allow-bootstrap')
    result=installer.main(flags)
    if result==0 and not args.dry_run:
        output=target/'aikya/docs/harness/requirements.md'
        output.parent.mkdir(parents=True,exist_ok=True)
        if output.is_symlink():
            print('AVISO: documento de requisitos es un enlace simbólico; no sobrescrito.',file=sys.stderr)
        elif output.exists() and not output.read_text(encoding='utf8').startswith('<!-- GENERATED BY AIKYA-HARNESS -->'):
            print('AVISO: documento de requisitos personalizado; no sobrescrito.',file=sys.stderr)
        else:
            output.write_text(markdown(report),encoding='utf8')
        print('\nAikya instalado. Para construir la aplicación, resuelve requisitos pendientes antes de ejecutar generadores.')
    return result

if __name__=='__main__':sys.exit(main())
