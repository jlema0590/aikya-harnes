#!/usr/bin/env python3
"""Contrato de versiones y notas de publicación de Aikya Harness.

Sólo verifica archivos locales y tags Git; no modifica el repositorio ni publica.
Las pruebas y el empaquetado se ejecutan fuera de este módulo.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
TAG_RE = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
HEADER_RE = re.compile(r"(?m)^##\s+v([0-9]+\.[0-9]+\.[0-9]+)(?=\s|$)[^\n]*$")
FILLER_RE = re.compile(r"(?i)\b(?:todo|tbd|pendiente de documentar|describe changes|replace me)\b")


class ReleaseError(ValueError):
    """Error de contrato: abortar sin crear tag ni release."""


def parse_version(text: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(text.strip())
    if not match:
        raise ReleaseError("VERSION exige SemVer estable X.Y.Z (sin prefijo v, sufijos o ceros a la izquierda).")
    return tuple(int(n) for n in match.groups())


def parse_tag(text: str) -> tuple[int, int, int] | None:
    match = TAG_RE.fullmatch(text)
    return tuple(map(int, match.groups())) if match else None


def read_version(root: Path) -> tuple[str, tuple[int, int, int]]:
    path = root / "VERSION"
    if not path.is_file() or path.is_symlink():
        raise ReleaseError("Falta VERSION regular en la raíz del repositorio.")
    raw = path.read_text(encoding="utf-8").strip()
    return raw, parse_version(raw)


def notes_from_changelog(changelog: str, version: str) -> str:
    headers = list(HEADER_RE.finditer(changelog))
    matches = [(n, match) for n, match in enumerate(headers) if match.group(1) == version]
    if len(matches) != 1:
        raise ReleaseError(f"CHANGELOG.md debe contener exactamente un encabezado '## v{version}'.")
    index, match = matches[0]
    end = headers[index + 1].start() if index + 1 < len(headers) else len(changelog)
    # Contenido exclusivo de la versión, sin incluir las notas de versiones anteriores.
    body = changelog[match.end():end].strip()
    if not body or not re.search(r"(?m)^\s*[-*]\s+\S", body):
        raise ReleaseError("Las notas de versión deben contener al menos un cambio en una lista.")
    if FILLER_RE.search(body):
        raise ReleaseError("Hay marcadores de texto pendientes en las notas de versión.")
    return "# Aikya Harness v" + version + "\n\n" + body + "\n"


def run_git(root: Path, *args: str, allow_missing: bool = False) -> str | None:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=False, timeout=15
    )
    if result.returncode:
        if allow_missing:
            return None
        raise ReleaseError("Git no pudo consultar " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def known_tags(root: Path) -> list[str]:
    raw = run_git(root, "tag", "--list", "v*")
    return [tag for tag in raw.splitlines() if parse_tag(tag) is not None] if raw else []


def tagged_commit(root: Path, tag: str) -> str | None:
    # ^{} resuelve también tags anotados al commit, evitando comparar el objeto tag.
    value = run_git(root, "rev-parse", "--verify", "refs/tags/" + tag + "^{}", allow_missing=True)
    return value.lower() if value else None


def compare_base_version(root: Path, base_ref: str) -> str | None:
    # El primer lanzamiento de VERSION es compatible con un main legado sin archivo.
    raw = run_git(root, "show", base_ref + ":VERSION", allow_missing=True)
    if raw is None:
        return None
    return raw.strip()


def validate(
    root: Path, *,
    head_sha: str | None = None,
    base_ref: str | None = None,
    tags: list[str] | None = None,
) -> dict[str, str | bool]:
    version, parsed = read_version(root)
    license_file = root / "LICENSE"
    if not license_file.is_file() or license_file.is_symlink():
        raise ReleaseError("LICENSE obligatorio antes de distribuir el código fuente.")
    changelog_file = root / "CHANGELOG.md"
    if not changelog_file.is_file() or changelog_file.is_symlink():
        raise ReleaseError("Falta CHANGELOG.md.")
    notes = notes_from_changelog(changelog_file.read_text(encoding="utf-8"), version)
    tag = "v" + version
    refs = tags if tags is not None else known_tags(root)
    semvers = [parse_tag(x) for x in refs if x != tag]
    older_max = max((v for v in semvers if v is not None), default=None)
    if older_max is not None and parsed <= older_max:
        raise ReleaseError(f"v{version} debe superar todos los tags de versiones anteriores.")
    current_head = head_sha or run_git(root, "rev-parse", "HEAD")
    existing = tag in refs
    if existing:
        if tags is not None:
            raise ReleaseError("La versión ya figura entre los tags existentes.")
        on_tag = tagged_commit(root, tag)
        if on_tag != current_head.lower():
            raise ReleaseError(f"{tag} ya existe y apunta a {on_tag}, no a {current_head}.")
    if base_ref:
        previous = compare_base_version(root, base_ref)
        if previous:
            if parse_version(previous) >= parsed:
                raise ReleaseError("El PR hacia main debe incrementar VERSION frente a " + base_ref + ".")
    return {"version": version, "tag": tag, "head_sha": current_head,
            "tag_exists": existing, "notes": notes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aikya release version contract (offline)")
    parser.add_argument("action", choices=["check", "notes"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", help="Validar incremento frente a rama main en PR")
    parser.add_argument("--output", type=Path, help="Guardar notas Markdown en una ruta indicada")
    parser.add_argument("--github-output", type=Path, help="Publicar salidas simples para GitHub Actions")
    args = parser.parse_args(argv)
    try:
        root = args.root.expanduser().resolve()
        result = validate(root, base_ref=args.base_ref)
        if args.output:
            output = args.output.expanduser().resolve()
            if args.action != "notes":
                raise ReleaseError("--output sólo está permitido con notes")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(str(result["notes"]), encoding="utf-8")
        if args.github_output:
            with args.github_output.open("a", encoding="utf-8") as stream:
                stream.write(f"release_tag={result['tag']}\nrelease_version={result['version']}\n")
        result.pop("notes", None)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ReleaseError, OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
        print("ERROR RELEASE:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
