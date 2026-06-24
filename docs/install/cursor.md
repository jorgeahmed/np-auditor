# NP Auditor — Cursor

## 1. Motor local (beta)

El operador debe tener home-hub con motor en:

`storage/pnp/local/p-np/`

## 2. Instalar MCP

```bash
cd ~/Projects/home-hub/projects/p-np/np-auditor/mcp-server
pip install -e .
```

## 3. Cursor MCP

`~/.cursor/mcp.json` o `.cursor/mcp.json` del proyecto:

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

Plantilla: [`config/examples/cursor-mcp.json`](../../config/examples/cursor-mcp.json)

## 4. Skill

Copia `skill/np-auditor/` → `.cursor/skills/np-auditor/` (proyecto o global).

## 5. Smoke test

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-smoke.sh
```

## 6. Tools

| Tool | Cuándo |
|------|--------|
| `np_audit_input` | Antes de prompt caro |
| `np_verify_response` | Tras respuesta con claims |
| `np_agent_risks` | Pagos / prod |
