# NP Auditor — OpenAI (ChatGPT / API / Agents)

## Beta local (MCP vía host compatible)

OpenAI integra MCP en productos que soporten **conectores MCP**. El servidor es el mismo binario stdio:

```bash
pip install -e mcp-server/
# command: np-auditor-mcp
# env: HOME_HUB_ROOT, NP_BRAIN_HOME
```

Configura según el producto (ChatGPT desktop connectors, etc.) apuntando al comando anterior.

## Instrucciones del agente

Copia [`skill/openai/instructions.md`](../../skill/openai/instructions.md) en:

- Custom instructions del GPT
- System prompt del **Agents SDK**
- Workflow de **Codex** / herramientas custom

## Agents SDK (function tools)

Si no hay MCP nativo, expón las 3 capacidades como functions que llamen al bridge:

```bash
# Equivalente shell (operador)
./scripts/np-auditor-bridge.sh audit "Objetivo: ..."
./scripts/np-auditor-bridge.sh verify '{"claims":[...]}'
NP_AUDITOR_DOMAIN=payment ./scripts/np-auditor-bridge.sh risks "..."
```

## Cloud v0.2 (recomendado para OpenAI puro)

| Modo | Variable |
|------|----------|
| Local MCP | `NP_BRAIN_HOME` |
| Cloud API | `NP_AUDITOR_API_KEY` |

Endpoint HTTP unificado para ChatGPT, API y Antigravity remoto — roadmap Fase 2.

## Diferencia vs Cursor / Claude

| Capa | Igual | Distinto |
|------|-------|----------|
| Motor + bridge | ✅ | — |
| 3 tools semánticas | ✅ | — |
| Config file | — | Formato por producto OpenAI |
| Instrucciones | — | `instructions.md` vs SKILL.md |

No hay que reescribir el motor; solo conectar el transporte (MCP stdio hoy, HTTP mañana).
