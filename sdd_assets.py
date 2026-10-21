"""Conservative migration of known generator/engine assets for explicit SDD opt-in."""
from pathlib import Path
import hashlib
import shutil

SOURCES = {'aikya/scripts/harness/sdd_localization.py':'sdd_localization.py', 'aikya/scripts/harness/scaffold.py': 'template/scripts/harness/scaffold.py', 'aikya/scripts/harness/infrastructure.py': 'template/scripts/harness/infrastructure.py', 'aikya/scripts/harness/sdd_engine.py': 'sdd_engine.py'}
TRUSTED = {'aikya/scripts/harness/sdd_localization.py':[], 'aikya/scripts/harness/scaffold.py': ['47181c3ad2cb22dbec5567953ae51378e115fcba21c9b590405491ffb990f752', '84cb93e758d45f5a1d14fdc0d7fe9ee484366f6e01a241906188f5ccb86413fc'], 'aikya/scripts/harness/infrastructure.py': ['c26d50ec3369dec6a8589c518c44eae5c246a586b0147d4d12a501d9c2623007', 'e3f186f10b57c75a5bb8f5a2651376a28775d6a36d53afb9d3055904ea82b2c3'], 'aikya/scripts/harness/sdd_engine.py': ['c7debd1a2a88336066162b609be19aa778284562f42dedfe51d28bef6f362a8c']}


def prepare(root: Path, source: Path) -> list[dict]:
    """Plan exact upgrades, rejecting custom or symlinked code before writes."""
    from sdd_engine import rel_file
    result = []
    for relative, origin in SOURCES.items():
        target = rel_file(root, relative)
        current_source = source/origin
        if not current_source.is_file(): raise ValueError('Incomplete SDD distribution: ' + origin)
        action = 'CREATE_MANAGED'
        if target.exists():
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if target.read_bytes() == current_source.read_bytes(): action = 'KEEP_EXISTING'
            elif digest in TRUSTED[relative]: action = 'UPDATE_KNOWN_SDD_ASSET_WITH_BACKUP'
            else: raise ValueError('Customized generator/engine requires SDD review: ' + relative)
        backup = '.harness/backup-v611/' + relative
        rel_file(root, backup)
        result.append({'path':relative, 'source':current_source, 'action':action, 'backup':backup})
    return result


def apply(root: Path, operations: list[dict], actions: list[str]) -> None:
    for operation in operations:
        if operation['action'] != 'UPDATE_KNOWN_SDD_ASSET_WITH_BACKUP': continue
        target = root/operation['path']; backup = root/operation['backup']
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists(): shutil.copy2(target, backup)
        shutil.copy2(operation['source'], target)
        actions.append('UPDATED known SDD asset with backup: ' + operation['path'])
