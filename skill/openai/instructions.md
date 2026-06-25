# NP Auditor — instrucciones para agentes OpenAI

Instalación: `docs/install/AGENT-beta-remote.md`

---

## Backend

**Beta remota:** `NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY`  
**Operador local:** `HOME_HUB_ROOT` + `NP_BRAIN_HOME`

## Dos fases de uso

| Fase | Tool | Cuándo |
|------|------|--------|
| ANTES | `np_audit_input` | Prompt costoso o ambiguo |
| DESPUÉS | `np_verify_response` | Respuesta con claims técnicos |

También: `np_coverage`, `np_agent_risks`, `np_suggest_prompt` (antes, opcional).

## Comportamiento

**Antes:**
1. `np_audit_input` con el prompt del usuario
2. Resumir estructura, riesgo_loop, cobertura

**Después:**
1. `np_verify_response` con la respuesta de la IA
2. Resumir verificados, contradichos, alucinación **medible**
3. Si sin claims medibles → decirlo en claro

**Siempre:**
- Una pasada por fase; no loops
- `np_suggest_prompt` → copiar, no ejecutar
- Pagos/prod → `np_agent_risks`

No prometas ahorro ni cero alucinaciones sin datos del informe.
