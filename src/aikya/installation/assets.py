"""Single destination inventory for source, registered and initialized runtimes."""
from dataclasses import dataclass
import json
from pathlib import Path
from aikya.resource_paths import package_root,source_path,source_root
from aikya.documentation.layout import asset_bytes

MODULES = json.loads((package_root() / 'module_map.json').read_text(encoding='utf8'))
HELPERS = {'scaffold', 'infrastructure', 'run_checks', 'skills_lint', 'docs_guard'}
EXECUTION_FILES = tuple(name + '.py' for name in MODULES if name in {
    'check_events', 'command_workflows', 'execution_state', 'execution_observer',
    'execution_config', 'execution_lifecycle', 'runtime_metrics', 'aikya_statusline',
    'aikya_subagent_statusline', 'odd_engine', 'agent_runtime', 'agent_loop',
    'agent_loop_state', 'agent_memory', 'memory_store', 'agent_memory_extract',
    'durable_io', 'code_quality', 'external_skills', 'skills_registry',
}) + ('requirements-agent-loop.txt', 'docs/AGENT_LOOP.md', 'docs/SECURITY_CONTROLS.md')
CORE_FILES = tuple(name + '.py' for name in MODULES if name not in HELPERS | {'context_budget'}) + (
    '_aikya_bootstrap.py', 'requirements-agent-loop.txt', 'docs/AGENT_LOOP.md', 'docs/SECURITY_CONTROLS.md',
)


@dataclass(frozen=True)
class AssetRecord:
    source: Path
    destination: Path
    kind: str


def runtime_assets(source: Path, target_kind: str, *, methodology=None) -> tuple[AssetRecord, ...]:
    if target_kind not in ('registration', 'initialized'):
        raise ValueError('Unsupported runtime target kind')
    source = Path(source)
    result = [AssetRecord(source_path(source, name), Path(name), 'adapter') for name in CORE_FILES]
    if target_kind == 'initialized' and methodology == 'odd':
        result = [asset for asset in result if asset.destination != Path('sdd_engine.py')]
    package = source / 'src/aikya'
    if not package.is_dir() and source == source_root():
        package = package_root()
    if not package.is_dir():
        raise ValueError('Incomplete packaged Aikya source')
    for path in sorted(package.rglob('*')):
        rel = path.relative_to(package)
        if path.is_file() and not path.is_symlink() and 'resources' not in rel.parts and '__pycache__' not in rel.parts and (path.suffix == '.py' or rel == Path('module_map.json')):
            result.append(AssetRecord(path, Path('src/aikya') / rel, 'package'))
    for folder in ('template', 'examples', 'aikya-skills', 'engineering', 'sdd-templates', 'claude-templates', 'aikya-template', 'migrations'):
        if folder == 'examples' and target_kind == 'initialized':
            continue
        origin = source_path(source, folder)
        for path in sorted(origin.rglob('*')):
            rel = Path(folder) / path.relative_to(origin)
            if path.is_file() and not path.is_symlink() and '__pycache__' not in rel.parts and path.suffix != '.pyc' and not rel.is_relative_to('examples/documentation/generated') and not (path.name.startswith('.env') and path.name != '.env.example'):
                result.append(AssetRecord(path, rel, 'resource'))
    destinations = [r.destination for r in result]
    if len(destinations) != len(set(destinations)):
        raise ValueError('Runtime asset destination collision')
    for record in result:
        if not record.source.is_file() or record.source.is_symlink():
            raise ValueError('Missing or unsafe runtime source: ' + str(record.source))
    return tuple(result)


SOURCE_GALLERY='https://github.com/jlema0590/aikya-harness/blob/08db4879ae3a8697c91adb0cc46bd76e333c693b/examples/documentation/generated/README.es.md'

def runtime_asset_bytes(relative:Path,raw:bytes)->bytes:
    """Keep source navigation local and registered-runtime navigation resolvable."""
    if relative==Path('examples/documentation/README.md'):
        raw=raw.replace(b'](generated/README.es.md)',(']('+SOURCE_GALLERY+')').encode('utf8'))
    return asset_bytes(relative,raw)

