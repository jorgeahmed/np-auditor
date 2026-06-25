# NP Auditor — Claude Code / Claude Desktop

Mismo MCP stdio que Cursor. Solo cambia el archivo de config.

## 1. Instalar MCP

Requisito: [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

Verifica:

```bash
~/Projects/np-auditor/mcp-server/.venv/bin/python -c "import np_auditor_mcp; print('ok')"
```

## 2. Claude Desktop

Edita `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/Users/TU/Projects/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "HOME_HUB_ROOT": "/Users/TU/home-hub",
        "NP_BRAIN_HOME": "/Users/TU/home-hub/storage/pnp/local/p-np"
      }
    }
  }
}
```

Plantilla: [`config/examples/claude-desktop.json`](../../config/examples/claude-desktop.json)

Reinicia Claude Desktop.

## 3. Claude Code (CLI)

En el proyecto o `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/Users/TU/Projects/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "HOME_HUB_ROOT": "/Users/TU/home-hub",
        "NP_BRAIN_HOME": "/Users/TU/home-hub/storage/pnp/local/p-np"
      }
    }
  }
}
```

Plantilla: [`config/examples/claude-code-settings.json`](../../config/examples/claude-code-settings.json)

## 4. Instrucciones del agente

Copia el skill Cursor o añade en `CLAUDE.md` del repo:

```markdown
Antes de prompts largos usa np_audit_input.
Tras respuestas con claims usa np_verify_response.
Pagos/prod → np_agent_risks.
```

Referencia: [`skill/np-auditor/SKILL.md`](../../skill/np-auditor/SKILL.md)

## 5. Probar

En el chat: *"Audita este prompt con NP Auditor: Objetivo: …"*

Debe invocar las tools MCP (icono herramientas).
