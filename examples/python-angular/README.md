# Ejemplo: FastAPI + Angular (aplicación nueva)

> **Plantilla de decisiones, no aplicación generada.** No hay compilación, dependencia ni SDK instalado por este ejemplo.

**Stack:** backend `python` + frontend `angular` + móvil `none`. **Arquitectura base:** `layered`. **Patrones complementarios:** ninguno.

## Uso desde Claude Code

1. Instala Aikya en modo global o proyecto desde una conversación de Claude Code.
2. Solicita: `/aikya-answers` y usa `examples/python-angular/answers.json` como respuestas. Pide a Claude que te muestre primero las decisiones y las adapte a tu entorno.
3. Continúa con `/aikya-doctor` para diagnosticar versiones y dependencias sin instalarlas automáticamente.
4. En aplicaciones nuevas, pide `/aikya-scaffold plan` y aprueba el generador adecuado. En un repositorio existente no ejecutes scaffolding sobre el código.
5. Solicita `/aikya-skills-status`, `/aikya-tests` y `/aikya-quality` para revisar los componentes activados y las verificaciones realmente disponibles.

## Skills y agentes previstos

Tras inicializar, Aikya utiliza el perfil para activar únicamente especialistas pertinentes; consulta `docs/agents.md`, `docs/skills.md` y `.harness/engineering-catalog.json`.
No todos los componentes del catálogo se instalan en cada proyecto y **disponible no significa ejecutado**.

## Consideraciones

FastAPI con Python y Angular; los generadores deben seleccionarse en Claude Code tras comprobar SDK y compatibilidad.

Revisa los comandos de build/test según los manifiestos creados. Si faltan, deben permanecer como pendientes en `harness.json`.
