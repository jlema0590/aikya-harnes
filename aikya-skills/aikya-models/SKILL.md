---
name: aikya-models
description: Configura modelos por rol con consentimiento explícito y sin alterar la selección global de Claude Code.
disable-model-invocation: true
---
# /aikya-models

Pregunta por los modelos para Planner/Orchestrator (recomendación: opus) y para el resto (por defecto inherit). Si la sesión principal está usando Opus, recomienda que el usuario considere Sonnet para tareas comunes; no ejecutes /model por tu cuenta ni modifiques ajustes globales sin permiso. Permite Haiku para tareas auxiliares acotadas únicamente con consentimiento explícito y tras comprobar disponibilidad. No presupongas que el alias haiku corresponde a Haiku 4.5; comprueba el modelo efectivo y ofrece heredar como fallback.

Guarda solo la decisión confirmada en `.aikya/model-policy.json`, validándola mediante `python3 token_policy.py --policy .aikya/model-policy.json` desde el runtime. No sobrescribas configuraciones personalizadas.
