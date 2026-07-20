---
name: np-auditor
description: >-
  Audita prompts ANTES y verifica respuestas DESPUÉS vía MCP. Invocar SOLO cuando
  el usuario pide explícitamente auditar, verificar, o @np-auditor.
  NO auto-invocar en cada mensaje. NO loops audit→suggest→re-audit ni verify repetido.
disable-model-invocation: true
---
# NP Auditor

Backend: **API remota** (`NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY`) o bridge local (`HOME_HUB_ROOT`).

Instalación: `docs/install/AGENT-beta-remote.md`

## Tres fases

| Fase | Tool | Cuándo |
|------|------|--------|
| **ANTES** | `np_audit_input` | Prompt caro, vago o riesgoso |
| **DESPUÉS** | `np_verify_response` | IA ya respondió con claims técnicos |
| **CÓDIGO** | `np_audit_code` | Hay un repo (propio o de un tercero) que auditar, no un prompt |

## Tools MCP (7)

| Tool | Fase |
|------|------|
| `np_audit_input` | Antes |
| `np_coverage` | Antes (opcional) |
| `np_agent_risks` | Antes (pagos/prod) |
| `np_select_model` | Antes — elegir LLM (Ollama/NVIDIA) |
| `np_suggest_prompt` | Antes — **solo copiar**, no ejecutar |
| `np_verify_response` | **Después** |
| `np_audit_code` | **Código** — SAST + secretos + SCA + IaC sobre un repo `https://` |

## Verify — presentar al usuario

Resumir en lenguaje claro (no JSON crudo):

- Cuántas afirmaciones eran medibles
- Cuántas verificadas vs contradichas
- % alucinación **solo sobre lo medible**
- Si “sin claims medibles”: no es fallo — fuera de alcance del organismo

## Reglas

1. **Una pasada** por audit y **una** por verify.
2. Verify **después** de respuesta, no antes del prompt.
3. Si `riesgo_loop=high` → pedir objetivo y criterio de éxito.
4. No inventar scores; usar solo output del MCP.
5. `np_suggest_prompt` → usuario pega manualmente; no ejecutar.

## Ejemplos

**Antes:** *"Audita antes de ejecutar: …"* → `np_audit_input`

**Después:** *"Verifica esta respuesta: …"* → `np_verify_response`
