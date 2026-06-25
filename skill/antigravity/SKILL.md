# NP Auditor — Antigravity / Gemini CLI skill

---
name: np-auditor
description: >-
  Audita prompts ANTES y verifica respuestas DESPUÉS vía MCP. Invocar cuando el
  usuario pide auditar/verificar o hay contexto pagos/prod/deploy.
  NO loops automáticos.
---

# NP Auditor (Antigravity)

Instalación: `docs/install/AGENT-beta-remote.md` (beta) o `AGENT-operator-local.md`

## Dos fases

1. **ANTES** — `np_audit_input` (prompt importante)
2. **DESPUÉS** — `np_verify_response` (respuesta con afirmaciones)

## Tools

- `np_audit_input` — antes de ejecutar
- `np_coverage` — mapa KNOWN/PARTIAL/UNKNOWN
- `np_agent_risks` — payment / prod
- `np_suggest_prompt` — copiar al usuario, no ejecutar
- `np_verify_response` — **después** de la respuesta del agente

## Flujo

```
Prompt → audit (1×) → usuario ajusta → agente trabaja → verify (1×) si hay claims
```

## Verify — qué decir al usuario

- Verificados / contradichos / alucinación medible
- Si nada medible: explicar que no es veredicto, solo fuera de alcance
- Una pasada; no re-verificar en bucle

## Reglas

- No inventar scores
- Beta remota: `NP_AUDITOR_API_URL` + key
- Una pasada por fase
