# NP Auditor — OpenAI (ChatGPT / API / Agents)

## Beta local (MCP vía host compatible)

OpenAI integra MCP en productos que soporten **conectores MCP**. Instala el binario stdio con uv:

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

Configura según el producto apuntando a:

```
command: /path/to/np-auditor/mcp-server/.venv/bin/np-auditor-mcp
env: HOME_HUB_ROOT, NP_BRAIN_HOME
```

## Instrucciones del agente

Copia [`skill/openai/instructions.md`](../../skill/openai/instructions.md) en:

- Custom instructions del GPT
- System prompt del **Agents SDK**
- Workflow de **Codex** / herramientas custom

## Agents SDK (function tools)

Si no hay MCP nativo, expón las capacidades como functions que llamen al bridge (operador con home-hub):

```bash
# Equivalente shell (operador)
./scripts/np-auditor-bridge.sh audit "Objetivo: ..."
./scripts/np-auditor-bridge.sh coverage "Objetivo: ..."
./scripts/np-auditor-bridge.sh verify '{"claims":[...]}'
NP_AUDITOR_DOMAIN=payment ./scripts/np-auditor-bridge.sh risks "..."
```

## Cloud / API beta (recomendado para OpenAI puro)

| Modo | Variable |
|------|----------|
| Local MCP | `NP_BRAIN_HOME` + binario en `.venv` |
| Cloud API | `NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY` |

Ver [api-beta.md](../api-beta.md). El tester instala MCP con `install-mcp.sh` y apunta al endpoint HTTP.

## Diferencia vs Cursor / Claude

| Capa | Igual | Distinto |
|------|-------|----------|
| Motor + bridge | ✅ | — |
| 5 tools semánticas | ✅ | — |
| Config file | — | Formato por producto OpenAI |
| Instrucciones | — | `instructions.md` vs SKILL.md |

No hay que reescribir el motor; solo conectar el transporte (MCP stdio hoy, HTTP vía env mañana).
