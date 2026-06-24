# Instalación multi-plataforma

NP Auditor usa **un solo MCP** (`np-auditor-mcp`) y **tres tools**.  
Solo cambia dónde pegas la config y el archivo de instrucciones.

| Plataforma | Guía | Config ejemplo |
|------------|------|----------------|
| **Cursor** | [cursor.md](cursor.md) | `config/examples/cursor-mcp.json` |
| **Claude Code / Desktop** | [claude.md](claude.md) | `config/examples/claude-desktop.json` |
| **Antigravity (Google)** | [antigravity.md](antigravity.md) | `config/examples/antigravity-mcp.json` |
| **OpenAI** | [openai.md](openai.md) | `skill/openai/instructions.md` |

## Instalación común (todas)

```bash
cd mcp-server && pip install -e .
export HOME_HUB_ROOT=~/Projects/home-hub
export NP_BRAIN_HOME=~/Projects/home-hub/storage/pnp/local/p-np
./scripts/np-auditor-smoke.sh   # desde home-hub
```

## Actualizaciones automáticas

Manifest y help Telegram se regeneran **máx 1×/día** cuando:

- Hay dims nuevas (EUREKA), o
- Completa un ciclo de rotación A→B→C

Ver [publicacion-diaria.md](publicacion-diaria.md).
