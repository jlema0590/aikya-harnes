#!/usr/bin/env python3
"""Preparación revisable del próximo VERSION y CHANGELOG, sin publicar nada."""
from __future__ import annotations
import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from release_contract import parse_version, ReleaseError, read_version

TAG=re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")


def prepare(root:Path, name:str, date:str|None=None) -> tuple[str,str]:
    if not TAG.fullmatch(name):
        raise ReleaseError("La versión debe tener formato vX.Y.Z sin sufijos")
    next_version=name[1:]
    current,parsed=read_version(root)
    if parse_version(next_version)<=parsed:
        raise ReleaseError(f"La versión nueva {name} debe superar v{current}")
    changelog=root/"CHANGELOG.md"
    if not changelog.is_file() or changelog.is_symlink():
        raise ReleaseError("Falta CHANGELOG.md")
    content=changelog.read_text(encoding="utf-8")
    if re.search(r"(?m)^##\s+"+re.escape(name)+r"(?=\s|$)",content):
        raise ReleaseError("Versión ya incluida en el changelog")
    heading=re.search(r"(?m)^## Sin publicar\s*$",content)
    if heading is None:
        raise ReleaseError("Añade un encabezado ## Sin publicar con notas revisadas antes de versionar")
    rest=content[heading.end():]
    nxt=re.search(r"(?m)^## ",rest)
    notes=rest[:nxt.start()] if nxt else rest
    if not re.search(r"(?m)^\s*[-*]\s+\S",notes):
        raise ReleaseError("No hay cambios listados bajo ## Sin publicar")
    today=date or datetime.now(timezone.utc).date().isoformat()
    replacement=f"## Sin publicar\n\n## {name} — {today}"
    revised=content[:heading.start()]+replacement+content[heading.end():]
    from release_contract import notes_from_changelog
    notes_from_changelog(revised,next_version)
    changelog.write_text(revised,encoding="utf-8")
    (root/"VERSION").write_text(next_version+"\n",encoding="utf-8")
    return name,today


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Prepare a version PR; never publish")
    parser.add_argument("--version",required=True)
    args=parser.parse_args(argv)
    try:
        version,date=prepare(ROOT,args.version)
    except (OSError,ReleaseError,UnicodeError) as exc:
        print("ERROR PREPARE:",exc,file=sys.stderr)
        return 2
    print(f"Prepared {version} — {date} in CHANGELOG.md and VERSION; review before merge.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
