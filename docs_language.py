"""Documentation language policy: only Aikya living docs may use Spanish."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

POLICY_FILE = ".aikya/docs-policy.json"
SUPPORTED = frozenset(("en", "es"))


def validate(language: str) -> str:
    if not isinstance(language, str) or language not in SUPPORTED:
        raise ValueError("Documentation language must be 'en' or 'es'.")
    return language


def policy_path(root: Path) -> Path:
    root = Path(root).absolute()
    for segment in (root / ".aikya", root / POLICY_FILE):
        if segment.is_symlink():
            raise ValueError("Symlinked documentation policy path is not allowed.")
    return root / POLICY_FILE


def read(root: Path) -> str | None:
    path = policy_path(root)
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError("Documentation policy must be a regular file.")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError) as exc:
        raise ValueError("Invalid documentation policy JSON.") from exc
    if not isinstance(obj, dict) or obj.get("schema_version") != 1 or set(obj) != {"schema_version", "language"}:
        raise ValueError("Unknown documentation policy schema or fields.")
    return validate(obj["language"])


def resolve(root: Path, requested: str | None = None, *, default: str = "en") -> str:
    current = read(root)
    if requested is not None:
        desired = validate(requested)
        if current is not None and current != desired:
            raise ValueError("Existing documentation language differs; use the approved documentation language migration workflow.")
        return desired
    return current or validate(default)


def write_approved(root: Path, language: str) -> bool:
    """Create an immutable policy once; never overwrite existing custom choices."""
    language = validate(language)
    path = policy_path(root)
    current = read(root)
    if current is not None:
        if current != language:
            raise ValueError("Changing a documentation language requires a separate reviewed migration.")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    value = json.dumps({"schema_version": 1, "language": language}, indent=2) + "\n"
    # Exclusive creation avoids overwriting an unexpected concurrent file.
    with path.open("x", encoding="utf-8") as stream:
        stream.write(value)
    return True
