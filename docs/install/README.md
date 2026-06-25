# Instalación multi-plataforma

## Para agentes LLM (recomendado en beta)

El usuario pide a **Claude, Antigravity o Cursor** que instale por él.

| Recurso | Formato | Uso |
|---------|---------|-----|
| [PROMPT-usuario.md](PROMPT-usuario.md) | Markdown | Usuario copia prompt al chat |
| [AGENT-beta-remote.md](AGENT-beta-remote.md) | Markdown | Agente sigue pasos (tester sin motor) |
| [AGENT-operator-local.md](AGENT-operator-local.md) | Markdown | Agente instala operador con motor |
| [agent-install-manifest.json](agent-install-manifest.json) | **JSON** | Spec machine-readable (pasos, templates, errores) |
| [config/examples/beta-remote-*.json](../config/examples/) | **JSON** | Plantillas MCP con placeholders |

---

## Para humanos

NP Auditor usa **un solo MCP** (`np-auditor-mcp`) y **cinco tools**.

| Plataforma | Guía humana | JSON ejemplo |
|------------|-------------|--------------|
| **Cursor** | [cursor.md](cursor.md) | `config/examples/cursor-mcp.json` |
| **Claude** | [claude.md](claude.md) | `config/examples/claude-desktop.json` |
| **Antigravity** | [antigravity.md](antigravity.md) | `config/examples/antigravity-mcp.json` |
| **OpenAI** | [openai.md](openai.md) | `skill/openai/instructions.md` |
| **Beta remota** | [api-beta.md](../api-beta.md) | `config/examples/beta-remote-cursor.json` |

## Requisitos (todas las plataformas)

- [uv](https://docs.astral.sh/uv/) — gestor Python (evita `pip`/`pip3` del sistema en macOS)
- Python ≥ 3.10 (uv lo resuelve al crear el venv)
- Beta **local:** `HOME_HUB_ROOT` + `NP_BRAIN_HOME`
- Beta **remota:** `NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY`

## Instalación común

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

Verifica:

```bash
~/Projects/np-auditor/mcp-server/.venv/bin/python -c "import np_auditor_mcp; print('ok')"
```

En MCP config, `"command"` = ruta absoluta a `mcp-server/.venv/bin/np-auditor-mcp`.

Actualizaciones: `./scripts/update.sh` tras `git pull`.
