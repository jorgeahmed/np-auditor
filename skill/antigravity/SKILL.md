# NP Auditor — Antigravity / Gemini CLI skill
# Copiar a: ~/.gemini/skills/np-auditor/SKILL.md

---
name: np-auditor
description: Audita prompts y respuestas de agentes antes de quemar tokens o ejecutar pagos/prod.
---

# NP Auditor

Usa las tools MCP `np_auditor` cuando:

- El usuario envía un prompt largo o costoso
- Hay contexto de pagos, wallet, prod, deploy
- Debes verificar claims tras una respuesta del agente

## Flujo

1. `np_audit_input` — antes de ejecutar
2. `np_verify_response` — tras respuesta con afirmaciones
3. `np_agent_risks` — domain=payment o prod

## Reglas

- No inventar scores; usar output del MCP
- Si riesgo_loop=high → pedir objetivo y criterio medible
- R1: el MCP no crea dimensiones; solo audita
