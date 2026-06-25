---
name: np-auditor
description: >-
  SOLO si el usuario escribe @np-auditor o ejecutó ./scripts/np-auditor-on.sh.
  Audita prompts fuera del chat por defecto. NO auto-invocar en cada mensaje.
disable-model-invocation: true
---
# NP Auditor (modo explícito)

Ver documentación completa en el repo home-hub: `docs/np-auditor-modelo-uso.md`

## Default: APAGADO en el chat

Auditar en terminal:

```bash
./scripts/np-auditor-audit.sh -f prompt.md --suggest
./scripts/np-auditor-off.sh   # quitar MCP del chat
./scripts/np-auditor-on.sh    # solo si lo pides explícito
```

## MCP tools (cuando ON)

- `np_audit_input` — estructura + cobertura + organismo
- `np_coverage` — mapa KNOWN/PARTIAL/UNKNOWN
- `np_agent_risks` — pagos/prod  
- `np_suggest_prompt` — copiar, no ejecutar
- `np_verify_response` — post-respuesta

**No loops de optimización.**
