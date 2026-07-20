# AGENT: instalar NP Auditor — beta remota (tester)

> **Audiencia:** agente LLM (Claude, Antigravity, Cursor Agent) instalando para un **beta tester**.  
> **Manifiesto JSON:** [`agent-install-manifest.json`](agent-install-manifest.json)  
> **NO** pidas `HOME_HUB_ROOT` ni `NP_BRAIN_HOME`. El motor vive en el servidor del operador.

---

## Inputs obligatorios (pedir al usuario si faltan)

| Variable | Ejemplo |
|----------|---------|
| `NP_AUDITOR_API_URL` | `https://api.jorgelaveaga.com` |
| `NP_AUDITOR_API_KEY` | `beta-maría-001` |
| Plataforma | `cursor` \| `claude_desktop` \| `claude_code` \| `antigravity` |
| OS | `darwin` \| `linux` |

Opcional: `INSTALL_ROOT` (default `~/Projects/np-auditor` expandido a ruta absoluta).

---

## Reglas para el agente instalador

1. **Nunca** uses `pip` / `pip3` del sistema en macOS.
2. **Siempre** usa `scripts/install-mcp.sh` (uv + venv).
3. En MCP config, `"command"` = ruta **absoluta** a `mcp-server/.venv/bin/np-auditor-mcp`.
4. En `env` del MCP **solo** (beta remota): `NP_AUDITOR_API_URL`, `NP_AUDITOR_API_KEY`.
5. **Merge** config existente; no borres otros `mcpServers`.
6. Tras instalar, ejecuta verificación (sección 6).

---

## Paso 1 — Prerrequisitos

```bash
# uv (si falta)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv --version
git --version
```

---

## Paso 2 — Clonar e instalar MCP

Sustituye `INSTALL_ROOT` por ruta absoluta (ej. `/Users/juan/Projects/np-auditor`):

```bash
INSTALL_ROOT="${HOME}/Projects/np-auditor"
git clone https://github.com/jorgeahmed/np-auditor.git "${INSTALL_ROOT}"
"${INSTALL_ROOT}/scripts/install-mcp.sh"
```

Salida esperada: línea `Binario: .../mcp-server/.venv/bin/np-auditor-mcp`

---

## Paso 3 — Verificar import

```bash
"${INSTALL_ROOT}/mcp-server/.venv/bin/python" -c "import np_auditor_mcp; print('ok')"
```

Debe imprimir `ok`.

---

## Paso 4 — Escribir config MCP (JSON)

Plantillas con placeholders en `config/examples/`:

| Plataforma | Archivo destino | Plantilla |
|------------|-----------------|-----------|
| Cursor | `~/.cursor/mcp.json` | `beta-remote-cursor.json` |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | `beta-remote-claude-desktop.json` |
| Claude Code | `~/.claude/settings.json` | `beta-remote-claude-code.json` |
| Antigravity | `~/.gemini/config/mcp_config.json` | `beta-remote-antigravity.json` |

Sustituir en JSON:

- `{{INSTALL_ROOT}}` → ruta absoluta sin `~`
- `{{NP_AUDITOR_API_URL}}` → URL del operador (sin `/` final)
- `{{NP_AUDITOR_API_KEY}}` → key del usuario

Ejemplo final (Cursor):

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/Users/juan/Projects/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "NP_AUDITOR_API_URL": "https://api.jorgelaveaga.com",
        "NP_AUDITOR_API_KEY": "beta-maría-001"
      }
    }
  }
}
```

Si el archivo ya existe, fusiona solo la clave `mcpServers.np-auditor`.

---

## Paso 5 — Copiar skill

```bash
INSTALL_ROOT="${HOME}/Projects/np-auditor"

# Cursor
mkdir -p "${HOME}/.cursor/skills/np-auditor"
cp "${INSTALL_ROOT}/skill/np-auditor/SKILL.md" "${HOME}/.cursor/skills/np-auditor/SKILL.md"

# Antigravity (si aplica)
mkdir -p "${HOME}/.gemini/skills/np-auditor"
cp "${INSTALL_ROOT}/skill/antigravity/SKILL.md" "${HOME}/.gemini/skills/np-auditor/SKILL.md"
```

---

## Paso 6 — Verificación (obligatoria)

```bash
# API del operador viva
curl -fsS "${NP_AUDITOR_API_URL}/health"
# → {"ok": true, "service": "np-auditor-api"}

# Smoke opcional vía API
curl -fsS -X POST "${NP_AUDITOR_API_URL}/v1/coverage" \
  -H "Authorization: Bearer ${NP_AUDITOR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test beta install"}' | head -c 200
```

En IDE: confirmar que MCP `np-auditor` lista **5 tools**:
`np_audit_input`, `np_coverage`, `np_verify_response`, `np_agent_risks`, `np_suggest_prompt`.

Reiniciar IDE (Claude Desktop restart / Cursor Reload Window).

---

## Paso 7 — Informar al usuario

Decir:

1. Instalación completa.
2. Cómo usar: antes de prompt caro → pedir `np_audit_input`.
3. **No** loops de re-audit automático.
4. Límite beta: ~120 req/h por key.
5. Si falla conexión: operador debe tener API + tunnel activos.

---

## Errores frecuentes

| Síntoma | Acción |
|---------|--------|
| `pip: command not found` | Usar `install-mcp.sh`, no pip |
| `HOME_HUB_ROOT` error | Quitar del JSON; solo API URL + key |
| HTTP 401 | Key incorrecta |
| HTTP 429 | Rate limit; esperar o contactar operador |
| Tunnel down | `curl /health` falla → operador |

---

## Uso post-instalación (resumen para el agente asistente)

### Fase ANTES (prompt)

| Tool | Cuándo invocar |
|------|----------------|
| `np_audit_input` | Antes de prompt costoso o ambiguo |
| `np_coverage` | Mapa dominios KNOWN/PARTIAL/UNKNOWN |
| `np_agent_risks` | Pagos, prod, deploy |
| `np_suggest_prompt` | Mejorar prompt — **solo copiar**, no ejecutar |

### Fase DESPUÉS (respuesta)

| Tool | Cuándo invocar |
|------|----------------|
| `np_verify_response` | Tras respuesta con afirmaciones técnicas, números o garantías |

Presentar verify al usuario en lenguaje claro:

- Medibles / verificados / contradichos
- % alucinación **solo sobre lo medible**
- "Sin claims medibles" = fuera de alcance, no es fallo

### Reglas

- Una pasada por fase (audit 1×, verify 1×)
- Verify **después** de que la IA respondió, no antes del prompt
- No loops audit → suggest → audit
