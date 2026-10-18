"""Perfil de infraestructura Aikya v5.7: validación tipada y compatibilidad legado."""
from __future__ import annotations
import re
from typing import Any

PROVIDERS = ('none', 'aws', 'azure', 'gcp', 'on-prem', 'hybrid')
IAC = ('none', 'terraform', 'opentofu', 'existing')
CONFIG = ('none', 'ansible', 'existing')
ORCHESTRATION = ('none', 'kubernetes', 'cloud-managed', 'vm')
METHODS = ('none', 'helm', 'kustomize', 'yaml')
_ENV_RE = re.compile(r'^[a-z][a-z0-9-]{0,30}$')
_REPO_RE = re.compile(r'^[a-zA-Z0-9._/@:-]+


def defaults(profile: dict) -> dict[str, Any]:
    """Perfiles previos no necesitan cambiar para seguir instalándose."""
    deployment = profile.get('deployment')
    kubernetes = deployment == 'kubernetes'
    return {
        'provider': 'none',
        'iac': 'none',
        'configuration_management': 'none',
        'containers': {'enabled': deployment in ('docker', 'kubernetes'), 'compose': False},
        'orchestration': 'kubernetes' if kubernetes else 'none',
        'deployment_method': 'yaml' if kubernetes else 'none',
        'environments': [],
        'image_repository': '',
        'container_port': None,
    }


def validated(profile: dict) -> dict[str, Any]:
    previous = defaults(profile)
    raw = profile.get('infrastructure')
    if raw is None:
        return previous
    if not isinstance(raw, dict):
        raise ValueError('infrastructure debe ser un objeto JSON')
    extras = set(raw) - set(previous)
    if extras:
        raise ValueError('Campos infrastructure no admitidos: ' + ', '.join(sorted(extras)))
    result = {**previous, **raw}
    for key, options in (
        ('provider', PROVIDERS), ('iac', IAC), ('configuration_management', CONFIG),
        ('orchestration', ORCHESTRATION), ('deployment_method', METHODS),
    ):
        if not isinstance(result[key], str) or result[key] not in options:
            raise ValueError('infrastructure.' + key + ': opción no válida')
    containers = result['containers']
    if not isinstance(containers, dict) or set(containers) - {'enabled', 'compose'}:
        raise ValueError('infrastructure.containers debe contener enabled y compose')
    enabled, compose = containers.get('enabled', False), containers.get('compose', False)
    if not isinstance(enabled, bool) or not isinstance(compose, bool):
        raise ValueError('infrastructure.containers enabled y compose deben ser booleanos')
    if compose and not enabled:
        raise ValueError('Docker Compose requiere containers.enabled=true')
    result['containers'] = {'enabled': enabled, 'compose': compose}
    if result['orchestration'] != 'kubernetes' and result['deployment_method'] != 'none':
        raise ValueError('Helm, Kustomize o YAML requieren Kubernetes')
    if result['orchestration'] == 'kubernetes':
        if result['deployment_method'] == 'none':
            raise ValueError('Selecciona helm, kustomize o yaml para Kubernetes')
        if not enabled:
            raise ValueError('Kubernetes requiere containers.enabled=true')
    environments = result['environments']
    if not isinstance(environments, list) or any(not isinstance(e, str) or not _ENV_RE.fullmatch(e) for e in environments):
        raise ValueError('infrastructure.environments debe ser lista de nombres seguros')
    if len(set(environments)) != len(environments) or len(environments) > 12:
        raise ValueError('Entornos duplicados o más de 12 entornos')
    repository = result['image_repository']
    if not isinstance(repository, str) or (repository and (len(repository) > 200 or not _REPO_RE.fullmatch(repository))):
        raise ValueError('infrastructure.image_repository no válido')
    port = result['container_port']
    if port is not None and (type(port) is not int or not 1 <= port <= 65535):
        raise ValueError('infrastructure.container_port debe ser un puerto TCP 1-65535')
    return result


def selected(info: dict) -> bool:
    return (info['iac'] not in ('none', 'existing') or
            info['configuration_management'] == 'ansible' or
            info['containers']['enabled'] or info['orchestration'] != 'none')


def capabilities(profile: dict) -> list[str]:
    info = validated(profile)
    caps = []
    if info['iac'] in ('terraform', 'opentofu'):
        caps.append(info['iac'])
    if info['configuration_management'] == 'ansible':
        caps.append('ansible')
    if info['containers']['enabled']:
        caps.append('docker')
    if info['containers']['compose']:
        caps.append('docker-compose')
    if info['orchestration'] == 'kubernetes':
        caps.append('kubectl')
        if info['deployment_method'] == 'helm':
            caps.append('helm')
        elif info['deployment_method'] == 'kustomize':
            caps.append('kustomize')
    return caps
)


def defaults(profile: dict) -> dict[str, Any]:
    """Perfiles previos no necesitan cambiar para seguir instalándose."""
    deployment = profile.get('deployment')
    kubernetes = deployment == 'kubernetes'
    return {
        'provider': 'none',
        'iac': 'none',
        'configuration_management': 'none',
        'containers': {'enabled': deployment in ('docker', 'kubernetes'), 'compose': False},
        'orchestration': 'kubernetes' if kubernetes else 'none',
        'deployment_method': 'yaml' if kubernetes else 'none',
        'environments': [],
        'image_repository': '',
        'container_port': None,
    }


def validated(profile: dict) -> dict[str, Any]:
    previous = defaults(profile)
    raw = profile.get('infrastructure')
    if raw is None:
        return previous
    if not isinstance(raw, dict):
        raise ValueError('infrastructure debe ser un objeto JSON')
    extras = set(raw) - set(previous)
    if extras:
        raise ValueError('Campos infrastructure no admitidos: ' + ', '.join(sorted(extras)))
    result = {**previous, **raw}
    for key, options in (
        ('provider', PROVIDERS), ('iac', IAC), ('configuration_management', CONFIG),
        ('orchestration', ORCHESTRATION), ('deployment_method', METHODS),
    ):
        if not isinstance(result[key], str) or result[key] not in options:
            raise ValueError('infrastructure.' + key + ': opción no válida')
    containers = result['containers']
    if not isinstance(containers, dict) or set(containers) - {'enabled', 'compose'}:
        raise ValueError('infrastructure.containers debe contener enabled y compose')
    enabled, compose = containers.get('enabled', False), containers.get('compose', False)
    if not isinstance(enabled, bool) or not isinstance(compose, bool):
        raise ValueError('infrastructure.containers enabled y compose deben ser booleanos')
    if compose and not enabled:
        raise ValueError('Docker Compose requiere containers.enabled=true')
    result['containers'] = {'enabled': enabled, 'compose': compose}
    if result['orchestration'] != 'kubernetes' and result['deployment_method'] != 'none':
        raise ValueError('Helm, Kustomize o YAML requieren Kubernetes')
    if result['orchestration'] == 'kubernetes':
        if result['deployment_method'] == 'none':
            raise ValueError('Selecciona helm, kustomize o yaml para Kubernetes')
        if not enabled:
            raise ValueError('Kubernetes requiere containers.enabled=true')
    environments = result['environments']
    if not isinstance(environments, list) or any(not isinstance(e, str) or not _ENV_RE.fullmatch(e) for e in environments):
        raise ValueError('infrastructure.environments debe ser lista de nombres seguros')
    if len(set(environments)) != len(environments) or len(environments) > 12:
        raise ValueError('Entornos duplicados o más de 12 entornos')
    repository = result['image_repository']
    if not isinstance(repository, str) or (repository and (len(repository) > 200 or not _REPO_RE.fullmatch(repository))):
        raise ValueError('infrastructure.image_repository no válido')
    port = result['container_port']
    if port is not None and (type(port) is not int or not 1 <= port <= 65535):
        raise ValueError('infrastructure.container_port debe ser un puerto TCP 1-65535')
    return result


def selected(info: dict) -> bool:
    return (info['iac'] not in ('none', 'existing') or
            info['configuration_management'] == 'ansible' or
            info['containers']['enabled'] or info['orchestration'] != 'none')


def capabilities(profile: dict) -> list[str]:
    info = validated(profile)
    caps = []
    if info['iac'] in ('terraform', 'opentofu'):
        caps.append(info['iac'])
    if info['configuration_management'] == 'ansible':
        caps.append('ansible')
    if info['containers']['enabled']:
        caps.append('docker')
    if info['containers']['compose']:
        caps.append('docker-compose')
    if info['orchestration'] == 'kubernetes':
        caps.append('kubectl')
        if info['deployment_method'] == 'helm':
            caps.append('helm')
        elif info['deployment_method'] == 'kustomize':
            caps.append('kustomize')
    return caps
