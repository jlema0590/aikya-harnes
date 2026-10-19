#!/usr/bin/env python3
"""Consulta segura del tag remoto usado en GitHub Release.

Trata HTTP 404 como ausencia de referencia, 401/403/5xx como errores, y
resuelve tags anotados antes de comparar con el commit del workflow.
No crea, borra ni mueve referencias. Sólo stdlib.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
TAG = re.compile(r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\Z")
SHA = re.compile(r"[a-fA-F0-9]{40}\Z")


class TagError(ValueError):
    """El estado del tag no se puede verificar de forma segura."""


def check_args(repo: str, tag: str, expected: str) -> None:
    if not REPO.fullmatch(repo) or not TAG.fullmatch(tag) or not SHA.fullmatch(expected):
        raise TagError("Repositorio, tag o SHA inválido")


def _get_json(repo: str, path: str, token: str, *, allow_not_found=False, opener=urlopen):
    req = Request(
        "https://api.github.com/repos/" + repo + "/" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "aikya-harness-release-check",
        },
    )
    try:
        with opener(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 404 and allow_not_found:
            return None
        raise TagError(f"GitHub API HTTP {exc.code} al consultar {path}") from exc
    except (URLError, UnicodeError, ValueError, OSError) as exc:
        raise TagError("Error consultando la API de GitHub: " + str(exc)) from exc
    if not isinstance(data, dict):
        raise TagError("Respuesta GitHub API no válida")
    return data


def resolve_commit(repo: str, tag: str, token: str, *, getter=None) -> str | None:
    """Retorna SHA del commit o None únicamente cuando la referencia no existe."""
    if getter is None:
        getter = lambda path, missing: _get_json(
            repo, path, token, allow_not_found=missing
        )
    ref = getter("git/ref/tags/" + tag, True)
    if ref is None:
        return None
    obj = ref.get("object")
    for _ in range(6):
        if not isinstance(obj, dict):
            raise TagError("Referencia sin object.type/object.sha")
        kind, sha = obj.get("type"), obj.get("sha")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise TagError("Referencia con SHA inválido o null")
        if kind == "commit":
            return sha.lower()
        if kind != "tag":
            raise TagError("Objeto inesperado detrás del tag: " + str(kind))
        annotated = getter("git/tags/" + sha, False)
        if annotated is None or not isinstance(annotated, dict):
            raise TagError("No se pudo resolver tag anotado")
        obj = annotated.get("object")
    raise TagError("Demasiados tags anotados encadenados")


def compare_tag(repo: str, tag: str, expected: str, token: str, *, getter=None) -> str:
    check_args(repo, tag, expected)
    result = resolve_commit(repo, tag, token, getter=getter)
    if result is None:
        return "missing"
    if result != expected.lower():
        raise TagError(
            f"Conflicto real: {tag} apunta a {result}; "
            f"el commit validado es {expected.lower()}. No se moverá el tag."
        )
    return "match"


def main(argv=None):
    p = argparse.ArgumentParser(description="Consultar Git tag remoto antes de publicar")
    p.add_argument("--repository", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--sha", required=True)
    args = p.parse_args(argv)
    try:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            raise TagError("Falta token de GitHub para consultar tags")
        status = compare_tag(args.repository, args.tag, args.sha, token)
    except TagError as exc:
        print("ERROR TAG:", exc, file=sys.stderr)
        return 2
    print(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
