# NP Auditor — Cursor

## 1. Motor local (beta)

El operador debe tener home-hub con motor en:

`storage/pnp/local/p-np/`

Testers **sin motor** usan API remota: [api-beta.md](../api-beta.md).

## 2. Modelo de uso (importante)

**Por defecto MCP apagado en chat** — evita loops de optimización.

```bash
./scripts/np-auditor-session-check.sh          # al iniciar sesión
./scripts/np-auditor-audit.sh -f prompt.md --suggest   # auditar en terminal
./scripts/np-auditor-off.sh                    # MCP off (recomendado)
./scripts/np-auditor-on.sh                     # MCP on solo si lo pides
```

Doc: `docs/np-auditor-modelo-uso.md` (en home-hub)

## 3. Instalar MCP (opcional)

Requisito: [uv](https://docs.astral.sh/uv/). No uses `pip` del sistema en macOS.

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

## 4. Cursor MCP

`~/.cursor/mcp.json` o `.cursor/mcp.json` del proyecto:

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

Plantilla: [`config/examples/cursor-mcp.json`](../../config/examples/cursor-mcp.json)

## 5. Skill

Copia `skill/np-auditor/` → `.cursor/skills/np-auditor/` (proyecto o global).

## 6. Smoke test

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-smoke.sh
```

## 7. Tools

| Fase | Tool | Cuándo |
|------|------|--------|
| **Antes** | `np_audit_input` | Antes de prompt caro |
| **Antes** | `np_coverage` | Mapa dominios KNOWN/PARTIAL/UNKNOWN |
| **Antes** | `np_agent_risks` | Pagos / prod |
| **Antes** | `np_suggest_prompt` | Prompt mejorado **solo copiar** |
| **Después** | `np_verify_response` | Tras respuesta con afirmaciones técnicas |

## 8. Prompt sugerido sin agente

Terminal:

```bash
./scripts/np-auditor-suggest.sh --copy-only <<'EOF'
tu prompt aquí...
EOF
```

MCP: tool `np_suggest_prompt` — copia el bloque al Composer manualmente.

## 9. Actualizaciones

Instala con `git clone` (no copia manual). Tras cada publicación en GitHub:

```bash
~/Projects/np-auditor/scripts/update.sh
```

Detalle: [docs/actualizaciones.md](../actualizaciones.md)
