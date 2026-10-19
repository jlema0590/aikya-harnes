## Resumen

<!-- ¿Qué cambia y por qué? Relaciona el Issue, si existe. -->

## Tipo de cambio

- [ ] `feat`: nueva funcionalidad
- [ ] `fix`: corrección
- [ ] `docs`: documentación
- [ ] `test`: pruebas
- [ ] `refactor` / mantenimiento
- [ ] Infrastructure / DevOps / Engineering Skill

## Áreas afectadas

- [ ] `/aikya-*` (`aikya-skills/`)
- [ ] Instalación y runtime (`install.py`, `aikya_setup.py`, `template/`)
- [ ] Agentes y skills (`engineering/`)
- [ ] `development`
- [ ] `infrastructure` (Terraform / OpenTofu / Ansible)
- [ ] `devops` (Docker / Compose / Kubernetes / Helm / Kustomize)
- [ ] Workflows GitHub Actions

## Verificación

- [ ] He ejecutado `python3 -m unittest discover -s tests -p 'test_*.py' -v`.
- [ ] Los perfiles de `examples/` siguen siendo compatibles.
- [ ] He ejecutado `python3 scripts/ci/check_assets.py` si cambia el catálogo.
- [ ] He ejecutado `python3 scripts/ci/smoke_profiles.py` si cambian los perfiles/planes.
- [ ] He actualizado documentación y `CHANGELOG.md` cuando procede.
- [ ] He comprobado que no se sobrescriben archivos de usuario.
- [ ] No he añadido secretos, credenciales, estado Terraform ni datos personales.
- [ ] Los recursos externos no se modifican sin aprobación expresa.

**Pruebas ejecutadas y resultados:**

<!-- Describe aquí las verificaciones reales. Indica las no realizadas. -->

## Compatibilidad y riesgos

<!-- Impacto sobre Aikya existente, agents/skills, backend/frontend, permisos y rollback. -->

## Licencias de terceros

<!-- Si incorporas contenido externo: origen, licencia y obligaciones de atribución. -->

## Lista de verificación de publicación

- [ ] Este Pull Request apunta a `develop` (salvo preparación deliberada de una release).
- [ ] No publica paquetes ni despliega infraestructura automáticamente.
