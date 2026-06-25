# Prompts para el usuario — copiar y pegar al agente

El usuario **no instala a mano**. Pega uno de estos prompts en Claude, Antigravity o Cursor y el agente sigue la guía + JSON.

Manifiesto machine-readable: [`agent-install-manifest.json`](agent-install-manifest.json)

---

## Beta tester — Claude Desktop / Claude Code

```
Instala NP Auditor para mí siguiendo EXACTAMENTE la guía del repo:
https://github.com/jorgeahmed/np-auditor/blob/main/docs/install/AGENT-beta-remote.md

También lee el manifiesto JSON:
https://github.com/jorgeahmed/np-auditor/blob/main/docs/install/agent-install-manifest.json

Soy beta tester REMOTO (sin motor local). NO uses HOME_HUB_ROOT ni NP_BRAIN_HOME.

Mis datos:
- Plataforma: Claude Desktop (macOS)   ← cambia si usas Claude Code
- API URL: https://TU-URL.trycloudflare.com
- API key: beta-TU-NOMBRE-001

Pasos:
1. Instala uv si falta
2. Clona en ~/Projects/np-auditor y ejecuta scripts/install-mcp.sh
3. Escribe ~/.cursor/mcp.json o claude_desktop_config.json con la plantilla beta-remote-*.json
4. Copia el skill correspondiente
5. Verifica curl /health y confirma las 5 MCP tools
6. Explícame en palabras simples: (a) auditar ANTES de un prompt importante (b) verificar DESPUÉS de una respuesta de la IA
```

---

## Beta tester — Antigravity

```
Instala NP Auditor siguiendo:
docs/install/AGENT-beta-remote.md
y agent-install-manifest.json
del repo https://github.com/jorgeahmed/np-auditor

Plataforma: Antigravity (Gemini CLI / IDE)
OS: macOS
API URL: https://TU-URL.trycloudflare.com
API key: beta-TU-NOMBRE-001

No tengo motor NP. Solo API remota.
Configura ~/.gemini/config/mcp_config.json y skill en ~/.gemini/skills/np-auditor/
Verifica MCP tools y curl /health al final.
```

---

## Beta tester — Cursor

```
Instala NP Auditor beta remota desde https://github.com/jorgeahmed/np-auditor

Guía: docs/install/AGENT-beta-remote.md
Manifiesto: docs/install/agent-install-manifest.json

Plataforma: Cursor
API URL: https://TU-URL.trycloudflare.com
API key: beta-TU-NOMBRE-001

Usa install-mcp.sh (uv, no pip). Config en ~/.cursor/mcp.json con plantilla config/examples/beta-remote-cursor.json.
Copia skill/np-auditor/SKILL.md a ~/.cursor/skills/np-auditor/
Reload Window al terminar.
```

---

## Operador (tú, con motor local)

```
Instala NP Auditor operador local:
docs/install/AGENT-operator-local.md

HOME_HUB_ROOT: /Users/plazaoriente/Projects/home-hub
NP_BRAIN_HOME: /Users/plazaoriente/Projects/home-hub/storage/pnp/local/p-np
Plataforma: Cursor

MCP apagado por defecto en chat. Smoke test con ./scripts/np-auditor-smoke.sh
```

---

## Una línea (comunidad)

```
Instala NP Auditor beta: clona github.com/jorgeahmed/np-auditor, sigue docs/install/AGENT-beta-remote.md, API URL=… key=…, plataforma=Claude/Antigravity/Cursor. Sin motor local.
```
