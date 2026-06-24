---
name: np-auditor
description: >-
  Audita prompts antes de enviarlos al agente y verifica respuestas (alucinación
  medible). Usar cuando el usuario pide revisar un prompt, evitar loops de tokens,
  verificar claims, o evaluar riesgos de agente (pagos, prod).
---
# NP Auditor

Auditor de inputs — medible, no caja negra.

## Cuándo usar

- Antes de un prompt largo o costoso al agente
- Cuando el usuario menciona pagos, wallet, prod, deploy, borrados
- Tras una respuesta del agente para verificar claims
- Si el usuario quiere evitar "loops eternos" de tokens

## Flujo

1. **`np_audit_input`** — auditar el prompt del usuario antes de ejecutar
2. Si hay respuesta con afirmaciones verificables → **`np_verify_response`**
3. Si contexto pagos/prod → **`np_agent_risks`** con `domain=payment` o `prod`

## Reglas

- No prometer "3× tokens" sin datos de la sesión
- Presentar el informe en lenguaje claro (estructura %, riesgos, sugerencias)
- Si `riesgo_loop` es high → sugerir acotar objetivo y criterio de éxito antes de continuar
- Si verify muestra alucinación > 0 → citar footer y no presentar claims como hechos

## Ejemplo

Usuario: "Quiero que el agente pague invoices desde mi wallet"

1. `np_agent_risks(prompt, domain="payment")`
2. `np_audit_input(prompt, context="payment")`
3. Ayudar a reescribir con límite de monto + aprobación humana si faltan
