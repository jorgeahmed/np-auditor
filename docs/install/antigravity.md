# NP Auditor — Google Antigravity (IDE / CLI)

Antigravity usa **MCP** vía `~/.gemini/config/mcp_config.json` y skills en `~/.gemini/skills/`.

## 1. Instalar MCP (stdio local)

Requisito: [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

## 2. Config MCP compartida

Crea o edita `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/Users/TU/Projects/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "HOME_HUB_ROOT": "/Users/TU/Projects/home-hub",
        "NP_BRAIN_HOME": "/Users/TU/Projects/home-hub/storage/pnp/local/p-np"
      }
    }
  }
}
```

Plantilla: [`config/examples/antigravity-mcp.json`](../../config/examples/antigravity-mcp.json)

En el IDE: **Agent Panel → MCP Servers →** verifica que `np-auditor` aparece con tools.

## 3. Skill Antigravity

```bash
mkdir -p ~/.gemini/skills/np-auditor
cp ~/Projects/np-auditor/skill/antigravity/SKILL.md \
   ~/.gemini/skills/np-auditor/SKILL.md
```

Comprueba con `/skills` en Antigravity CLI.

## 4. Remoto (API beta)

Testers sin motor local instalan el MCP igual (`install-mcp.sh`) y usan:

```json
{
  "env": {
    "NP_AUDITOR_API_URL": "https://api.jorgelaveaga.com",
    "NP_AUDITOR_API_KEY": "beta-key-1"
  }
}
```

Detalle: [api-beta.md](../api-beta.md).

Antigravity Agent API también soporta MCP **Streamable HTTP** (roadmap endpoint cloud).

## 5. Diferencia vs Cursor

| | Cursor | Antigravity |
|---|--------|-------------|
| Config | `~/.cursor/mcp.json` | `~/.gemini/config/mcp_config.json` |
| Skills | `.cursor/skills/` | `~/.gemini/skills/` |
| MCP tools | Igual | Igual |
| Instalación MCP | `scripts/install-mcp.sh` | Igual |
