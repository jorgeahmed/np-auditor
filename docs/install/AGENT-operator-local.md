# AGENT: instalar NP Auditor — operador local

> **Audiencia:** agente LLM instalando para el **operador** con motor NP en la misma Mac.  
> **Manifiesto JSON:** [`agent-install-manifest.json`](agent-install-manifest.json) (adaptar env a local).

---

## Inputs obligatorios

| Variable | Ejemplo |
|----------|---------|
| `HOME_HUB_ROOT` | `/Users/juan/Projects/home-hub` |
| `NP_BRAIN_HOME` | `/Users/juan/Projects/home-hub/storage/pnp/local/p-np` |
| Plataforma | `cursor` \| `claude_desktop` \| `claude_code` \| `antigravity` |

Verificar que exista: `${NP_BRAIN_HOME}/src/prompt_lab/core.py`

---

## Instalación MCP (igual que beta)

```bash
INSTALL_ROOT="${HOME}/Projects/np-auditor"
git clone https://github.com/jorgeahmed/np-auditor.git "${INSTALL_ROOT}" 2>/dev/null || true
"${INSTALL_ROOT}/scripts/install-mcp.sh"
```

---

## Config MCP local (JSON)

Fusionar en el archivo de la plataforma (`config/examples/cursor-mcp.json` como base):

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/RUTA_ABSOLUTA/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "HOME_HUB_ROOT": "/RUTA_ABSOLUTA/home-hub",
        "NP_BRAIN_HOME": "/RUTA_ABSOLUTA/home-hub/storage/pnp/local/p-np"
      }
    }
  }
}
```

**No** incluir `NP_AUDITOR_API_URL` si usas bridge local.

---

## Modelo de uso (operador)

Default: **MCP apagado en chat**. Preferir terminal:

```bash
cd "${HOME_HUB_ROOT}"
./scripts/np-auditor-audit.sh -f prompt.md --suggest
./scripts/np-auditor-off.sh   # MCP off
./scripts/np-auditor-on.sh    # MCP on solo si explícito
```

Doc: `home-hub/docs/np-auditor-modelo-uso.md`

---

## Verificación

```bash
cd "${HOME_HUB_ROOT}"
./scripts/np-auditor-smoke.sh
```

Esperado: JSON de audit sin error.

---

## API remota (opcional, para servir testers)

Si el operador también expone beta:

```bash
export NP_AUDITOR_API_KEYS="key1,key2"
./scripts/np-auditor-api.sh
cloudflared tunnel --url http://127.0.0.1:8787
```

Ver `docs/api-beta.md`.
