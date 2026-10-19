# GitHub Actions de Aikya Harness — corrección v5.9.1

## Política de ramas y de publicación

```text
feat/* o fix/* → PR develop → PR main → CI → tag vX.Y.Z + GitHub Release
```

- PR a `develop` y ramas `feat/*`/`fix/*`: pruebas y smoke sin publicar.
- PR a `main`: `release-check.yml` comprueba SemVer, incremento frente a `origin/main`, `LICENSE`, `CHANGELOG.md` y ausencia de tags duplicados.
- Push tras merge a `main`: `release.yml` publica automáticamente si vuelven a superar las pruebas los archivos exactos fusionados. `workflow_dispatch` sirve únicamente como recuperación manual tras una interrupción.
- La versión se lee de `VERSION` como `5.9.1`; la etiqueta se llama `v5.9.1`. No se inventa una versión basada en fecha o SHA.

## Inventario de workflows

| Workflow | Triggers | Responsabilidad |
| --- | --- | --- |
| `tests.yml` | push develop/main/feat/fix/release, PR, manual | Sintaxis y unittest Python 3.10–3.13 |
| `smoke-stacks.yml` | push/PR sobre rutas relevantes, manual | Simular 14 perfiles sin desplegar |
| `check-asset-sync.yml` | push/PR sobre agentes, skills y bootstrap; manual | Catálogo, frontmatter y comandos |
| `refresh-catalogs.yml` | lunes, manual | Inventario solo lectura; NO sincroniza contenido tercero |
| `release-check.yml` | PR hacia main, push feature cuando cambia release, manual | Contrato SemVer y tests de release |
| `bump-versions.yml` | manual en develop | Genera PR con VERSION y CHANGELOG; no publica |
| `release.yml` | push main, recuperación manual | Verifica, ZIP/sha256, tag y GitHub Release |

## Archivos auxiliares

- `scripts/ci/release_contract.py`: validación estable de versión, notas, tags e incremento de PR.
- `scripts/ci/prepare_release.py`: transforma las notas de `## Sin publicar` en changelog de nueva versión y actualiza VERSION. Requiere contenido real, falla si faltan notas.
- `scripts/ci/check_assets.py`, `smoke_profiles.py`, `catalog_review.py`: no generan ni despliegan recursos.
- `tests/test_release_workflows.py`: contratos de versión, fallos, recuperación, preparación del siguiente release.

## Pasos de configuración de GitHub (mantenedor)

1. En Settings → Branches o Rulesets, exige PRs para `main` (sin push directo ni bypass), revisiones y checks obligatorios. Incluye `Validate VERSION and changelog` y los jobs de tests de la matriz Python.
2. Verifica que GitHub Actions no está deshabilitado. El job de publicación solicita `contents: write`; el resto usa lectura. No necesita personal access token, secretos cloud ni acceso a servidores.
3. GitHub Actions debe permitir a la acción que prepara versiones crear Pull Requests; si la configuración de la organización no lo permite, el mantenedor puede abrir un PR con VERSION y CHANGELOG manualmente.
4. Promueve `feat/adap_workflows` a `develop`, valida el CI, después abre PR a `main`. El merge dispara la primera publicación automática `v5.9.1`, siempre que ese tag no exista todavía.

**Nunca actives una Release automática antes de comprobar el derecho a distribuir agentes y skills terceros.** La licencia MIT del proyecto no sustituye las licencias de terceros.

## Recuperación e idempotencia

- Antes de crear un tag, el pipeline comprueba versión y assets. El tag apunta exactamente a `GITHUB_SHA` de main validado; no se mueve ni se fuerza.
- Si el tag ya existe en otro commit, el job falla de forma segura.
- Si existe en el mismo commit, el workflow puede recuperar la publicación sin recrearlo.
- Si la Release existe, no se duplica: sólo añade artefactos faltantes. Release completa no se altera.
- Si falla una verificación no se crea el tag ni se publica la Release.
- Las ejecuciones se serializan con cola para minimizar carreras entre merges.

**Límites:** este pipeline no despliega cloud, no actualiza SDKs, no publica NPM y no audita jurídicamente las licencias. `sha256sum` verifica integridad del ZIP, no procedencia del contenido.

## Recuperación de v5.9.1 si la publicación todavía no existe

`github_tag.py` consulta GitHub con estado HTTP explícito: 404 significa tag ausente, 401/403/5xx detienen la operación, y los tags anotados se resuelven hasta el commit real. La publicación crea el tag con `gh release create --target "$GITHUB_SHA"` únicamente si la referencia no existe.

Si `main` contiene VERSION=5.9.1 pero el tag aún no existe, se permite un PR de reparación sin incremento de versión; luego el merge a main publicará `v5.9.1` sobre el **nuevo commit**. Después de publicar ese tag, la siguiente versión debe aumentar. No utilices `Re-run failed jobs` del workflow antiguo: GitHub Actions reejecuta la definición anterior; hay que integrar el fix en main para usarla.
