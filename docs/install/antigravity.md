# NP Auditor — Google Antigravity (IDE / CLI)

Antigravity usa **MCP** vía `~/.gemini/config/mcp_config.json` y skills en `~/.gemini/skills/`.

## 1. Instalar MCP (stdio local)

```bash
cd ~/Projects/home-hub/projects/p-np/np-auditor/mcp-server
pip install -e .
```

## 2. Config MCP compartida

Crea o edita `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "np-auditor-mcp",
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
cp ~/Projects/home-hub/projects/p-np/np-auditor/skill/antigravity/SKILL.md \
   ~/.gemini/skills/np-auditor/SKILL.md
```

Comprueba con `/skills` en Antigravity CLI.

## 4. Remoto (v0.2)

Antigravity Agent API soporta MCP **Streamable HTTP**. Cuando publiquemos endpoint cloud, registrar:

```json
{
  "type": "mcp_server",
  "name": "np-auditor",
  "url": "https://api.example.com/mcp",
  "headers": { "Authorization": "Bearer TOKEN" }
}
```

Beta local: **stdio** es suficiente.

## 5. Diferencia vs Cursor

| | Cursor | Antigravity |
|---|--------|-------------|
| Config | `~/.cursor/mcp.json` | `~/.gemini/config/mcp_config.json` |
| Skills | `.cursor/skills/` | `~/.gemini/skills/` |
| MCP tools | Igual | Igual |
