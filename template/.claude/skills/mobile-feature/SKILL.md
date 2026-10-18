---
name: mobile-feature
description: Implementa funcionalidades móviles en Android/iOS o Flutter/React Native con validación específica de plataforma.
disable-model-invocation: true
---
Solicitud: $ARGUMENTS
1. Revisa el perfil y los manifiestos de Android/iOS/Flutter/React Native reales.
2. Establece criterios de aceptación por plataforma, permisos, accesibilidad, red y datos locales.
3. Usa `mobile-engineer` para cambios complejos; evita cambios simultáneos al mismo archivo.
4. Crea pruebas unitarias e instrumentadas/UI cuando existan herramientas disponibles.
5. Ejecuta builds por variante/scheme real; si faltan SDK, Xcode o simulador, informa NO VERIFICADO.
6. Revisa claves, permisos, firma y publicación; no ejecutes releases sin aprobación.
7. Actualiza `docs/features/index.md` con diferencias Android/iOS y criterios de aceptación, `docs/quality/testing.md` con pruebas reales y `docs/security/security.md` si toca permisos/datos. Registra la petición en `docs/changes/REQ-*.md`.
