#!/usr/bin/env python3
"""Aikya Skills support CLI. New-project interviews run inside Claude Code."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
# Dry-run and report-only must not leave bytecode in a project-local Aikya runtime.
sys.dont_write_bytecode = True
import install as installer
from aikya_requirements import check, markdown


def resolved_answers(args, target:Path) -> Path:
    if args.answers:
        path=args.answers.expanduser().resolve()
    else:
        candidates=[target/'.aikya/answers.json',target/'.harness/project-profile.json']
        path=next((p for p in candidates if p.is_file()),candidates[0])
    if not path.is_file():
        raise ValueError(f'No technical profile was found at {path}; use /aikya-init for new projects, /aikya-analyze for existing repositories, or provide --answers.')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description='Aikya Harness commands executed by Claude Code')
    parser.add_argument('command',choices=['probe','requirements','init','answers','status','analyze'])
    parser.add_argument('--target',type=Path,default=Path.cwd())
    parser.add_argument('--answers',type=Path)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--strict',action='store_true',help='Fail with exit 4 if SDK requirements are incomplete')
    parser.add_argument('--external',choices=['skip','plan','install'],default='plan')
    parser.add_argument('--display-name')
    parser.add_argument('--scope',default='.')
    parser.add_argument('--focus',choices=['general','security','architecture','infrastructure','operations'],default='general')
    parser.add_argument('--docs-lang',choices=['en','es'],default=None,help='Aikya living documentation language')
    parser.add_argument('--methodology', choices=['standard', 'sdd'], default=None)
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
                           dry_run=args.dry_run,report_only=args.report_only,docs_lang=args.docs_lang,methodology=args.methodology)
        except (ValueError,OSError,UnicodeError,TypeError) as exc:
            print('ERROR during analysis:',exc,file=sys.stderr)
            return 2
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['status']=='READY' else 4
    if args.command=='probe':
        detected=installer.detect_project(target) if target.exists() else {'modules':[],'findings':['New directory']}
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
        print('ERROR parsing answers:',exc,file=sys.stderr)
        return 2
    if args.command=='init' and profile['mode']!='new':
        print('ERROR: /aikya-init is only for new projects. Use /aikya-analyze for existing repositories; nothing was written.',file=sys.stderr)
        return 2
    if args.command=='answers' and profile['mode']=='existing':
        print('NOTICE: legacy declarative profile; use /aikya-analyze for automatic existing-repository discovery.',file=sys.stderr)
        # Compatibility shim: existing profiles remain valid but no user IaC, CI or Docker files change.
        detected=installer.detect_project(target)
        try:
            actions=installer.install(target,profile,detected,dry_run=args.dry_run,adopt_existing=True,docs_lang=args.docs_lang)
        except (ValueError,OSError,UnicodeError) as exc:
            print('ERROR during adoption:',exc,file=sys.stderr)
            return 2
        print(json.dumps({'mode':'existing','dry_run':args.dry_run,'actions':actions},
                         ensure_ascii=False,indent=2))
        return 0
    report=check(profile,target)
    print('\n=== AIKYA TOOLCHAIN REQUIREMENTS ===')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if args.command=='requirements':
        return 4 if args.strict and not report['ready'] else 0
    if args.strict and not report['ready']:
        print('REQUIREMENTS PENDING: request developer approval before updating SDKs.',file=sys.stderr)
        return 4
    # run through current process (same interpreter), never auto-install SDKs.
    flags=['--target',str(target),'--answers',str(source),'--external',args.external]
    if args.dry_run: flags.append('--dry-run')
    if args.display_name: flags+=['--display-name',args.display_name]
    if args.docs_lang: flags+=['--docs-lang',args.docs_lang]
    if (target/'.aikya/bootstrap.json').exists() or (target/'.aikya/answers.json').exists(): flags.append('--allow-bootstrap')
    result=installer.main(flags)
    if result==0 and not args.dry_run:
        output=target/'aikya/docs/harness/requirements.md'
        output.parent.mkdir(parents=True,exist_ok=True)
        if output.is_symlink():
            print('NOTICE: requirements document is a symlink and was not overwritten.',file=sys.stderr)
        elif output.exists() and not output.read_text(encoding='utf8').startswith('<!-- GENERATED BY AIKYA-HARNESS -->'):
            print('NOTICE: customized requirements document was not overwritten.',file=sys.stderr)
        else:
            output.write_text(markdown(report, __import__('docs_language').resolve(target, args.docs_lang)),encoding='utf8')
        print('\nAikya installed. Resolve outstanding SDK requirements before running project generators.')
    return result

if __name__=='__main__':sys.exit(main())
