# cursor.md — NP Auditor

**Proyecto:** cliente MCP + skills para auditar agentes de IA  
**Motor:** `~/Projects/home-hub/storage/pnp/local/p-np` (no incluido en este repo)  
**Última actualización:** 2026-07-16

---

## 1. Qué es NP Auditor

NP Auditor es un **examinador medible** para agentes de IA — no es otro chatbot.

Revisa en **dos momentos**:

1. **Antes** — estructura del prompt, riesgos, cobertura del organismo
2. **Después** — afirmaciones de la respuesta vs lo que el sistema puede medir

```
Prompt importante          IA ya respondió
       ↓                          ↓
np_audit_input (1×)      np_verify_response (1×)
       ↓                          ↓
Ajustas y ejecutas       Decides si confías
```

**Auditar ≠ entrenar.** Usar el auditor no modifica el organismo ni crea dimensiones.

### Relación con otros componentes

| Componente | Rol respecto a NP Auditor |
|---|---|
| **np-auditor** (este repo) | Cliente público: MCP stdio, skills, manifests, docs |
| **home-hub** | Bridge, API HTTP, scripts terminal, hooks Cursor |
| **NP Brain** (`NP_BRAIN_HOME`) | Motor: prompt_lab, sensores, banco ~20k dims |

El **motor de verificación no se distribuye** en GitHub. Este repo es MIT (cliente + skill).

---

## 2. Reglas inviolables

### R-AUD-01 — Dos fases, una pasada cada una

- **ANTES:** `np_audit_input` (y opcionales) — una sola vez por prompt
- **DESPUÉS:** `np_verify_response` — una sola vez por respuesta
- Prohibido: loops audit → suggest → re-audit → verify repetido

### R-AUD-02 — Solo invocar cuando el usuario lo pide

El skill tiene `disable-model-invocation: true`. Invocar **solo** si el usuario pide
explícitamente auditar, verificar, o `@np-auditor`. No auditar cada mensaje.

### R-AUD-03 — Suggest = copiar, no ejecutar

`np_suggest_prompt` devuelve un bloque para **pegar manualmente** en Composer.
Nunca ejecutar el prompt sugerido automáticamente.

### R-AUD-04 — Scores solo del MCP

No inventar porcentajes ni veredictos. Usar únicamente el output de las tools.

### R-AUD-05 — Verify: medible vs no medible

| Resultado | Significado |
|---|---|
| **Verificados** | Cuadran con lo medido en el organismo |
| **Contradichos** | Chocan con lo medido — revisar con cuidado |
| **Alucinación (medible)** | % de error solo sobre claims comprobables |
| **Sin claims medibles** | Opiniones o temas fuera de alcance — **no es fallo** |

### R-AUD-06 — MCP apagado por defecto (operador local)

Evita loops de optimización en el agente. Auditar en **terminal** o con MCP on
solo cuando se pide explícitamente.

---

## 3. Arquitectura

```
Agente (Cursor / Claude / Antigravity)
        │
        ▼
  MCP stdio (np-auditor-mcp)          ← este repo
        │
        ├── [Remoto] POST /v1/*  →  home-hub/np-auditor-api.sh
        │
        └── [Local]  bash HOME_HUB_ROOT/scripts/np-auditor-bridge.sh
                              │
                              ▼
                    NP Brain (NP_BRAIN_HOME)
                    prompt_lab · sensores · banco
```

### Backend dual

| Modo | Variables | Quién |
|---|---|---|
| **Local** | `HOME_HUB_ROOT` + `NP_BRAIN_HOME` | Operador con Mac + motor |
| **Remoto** | `NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY` | Beta tester sin motor |

Si `NP_AUDITOR_API_URL` está definido, tiene **prioridad** sobre el bridge local.

### Versión pública del organismo

`manifests/release.json` — subset verificable sin código de sensores:

| Campo | Valor actual |
|---|---|
| Versión | `0.1.20338` |
| Dims organismo | 20 338 |
| Agent risk dims | 50 (6 publicados como muestra en `dims-subset.json`) |
| Fixtures prompt_lab | 10 |

---

## 4. MCP Tools (6)

| Tool | Fase | Qué hace |
|---|---|---|
| `np_audit_input` | **Antes** | Score estructura, sugerencias, cobertura, riesgo loop |
| `np_coverage` | **Antes** (opc.) | Mapa KNOWN / PARTIAL / UNKNOWN por dominio |
| `np_agent_risks` | **Antes** (pagos/prod) | Checklist riesgos (`general`, `payment`, `prod`) |
| `np_suggest_prompt` | **Antes** (opc.) | Prompt mejorado para **copiar** |
| `np_select_model` | **Antes** | Elige modelo OpenClaw (Ollama / NVIDIA NIM) |
| `np_verify_response` | **Después** | Verifica claims o `response_text` completo |

**Sin LLM** en el path local (~1 s, $0 tokens).

Implementación: `mcp-server/src/np_auditor_mcp/server.py` + `client.py`.

---

## 5. Estructura del proyecto

```
~/Projects/np-auditor/
│
├── cursor.md                          # ← ESTE ARCHIVO
├── README.md                          # Punto de entrada humano
│
├── mcp-server/                        # Servidor MCP stdio (Python ≥3.10)
│   ├── pyproject.toml                 # np-auditor-mcp v0.1.0
│   └── src/np_auditor_mcp/
│       ├── server.py                  # 6 tools FastMCP
│       └── client.py                  # Bridge local o API HTTP
│
├── skill/                             # Instrucciones para agentes
│   ├── np-auditor/SKILL.md            # Cursor (principal)
│   ├── np-router/SKILL.md             # OpenClaw / Telegram
│   ├── antigravity/SKILL.md           # Gemini CLI
│   └── openai/instructions.md         # Agentes OpenAI
│
├── scripts/
│   ├── install-mcp.sh                 # uv venv + pip install -e .
│   └── update.sh                      # git pull + reinstall
│
├── manifests/
│   ├── release.json                   # Versión pública
│   └── dims-subset.json               # Subset dominios + fixtures
│
├── config/examples/                   # Plantillas MCP por plataforma
│   ├── cursor-mcp.json                # Local
│   └── beta-remote-cursor.json        # Remoto
│
└── docs/
    ├── INDEX.md                       # Índice maestro
    ├── producto.md                    # Qué es (usuario)
    ├── api-beta.md                    # API HTTP remota
    ├── uso-terminal.md                # Terminal + MCP on/off
    └── install/
        ├── cursor.md                  # Instalación Cursor (detalle)
        ├── AGENT-beta-remote.md       # Guía agente instalador
        └── agent-install-manifest.json
```

### Lo que NO está aquí (vive en home-hub)

```
~/Projects/home-hub/scripts/
├── np-auditor-bridge.sh       # Puente principal local
├── np-auditor-api.sh          # Servidor HTTP /v1/*
├── np-auditor-audit.sh        # Auditar en terminal
├── np-auditor-suggest.sh      # Suggest en terminal
├── np-auditor-on.sh           # Activar MCP en mcp.json
├── np-auditor-off.sh          # Desactivar MCP
├── np-auditor-session-check.sh
└── np-auditor-smoke.sh
```

Docs operador: `home-hub/docs/np-auditor-modelo-uso.md`,
`home-hub/docs/np-auditor-arquitectura-hoy-v1.md`.

---

## 6. Instalación

### Requisitos

- [uv](https://docs.astral.sh/uv/) — **no** usar `pip` del sistema en macOS
- Python ≥ 3.10 (uv lo gestiona en el venv)
- Motor local **o** API key remota

### Cliente MCP

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
# Binario: mcp-server/.venv/bin/np-auditor-mcp
```

### Variables (operador local)

```bash
export HOME_HUB_ROOT=~/Projects/home-hub
export NP_BRAIN_HOME=$HOME_HUB_ROOT/storage/pnp/local/p-np
```

### Cursor (`~/.cursor/mcp.json`)

Ruta **absoluta** al binario del venv:

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

Plantilla: [`config/examples/cursor-mcp.json`](config/examples/cursor-mcp.json)

### Skill Cursor

```bash
cp -r skill/np-auditor ~/.cursor/skills/np-auditor
# o en el proyecto: .cursor/skills/np-auditor/
```

### Beta remota (sin motor local)

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/path/to/np-auditor-mcp",
      "env": {
        "NP_AUDITOR_API_URL": "https://tu-tunnel.trycloudflare.com",
        "NP_AUDITOR_API_KEY": "tu-key"
      }
    }
  }
}
```

Detalle: [`docs/api-beta.md`](docs/api-beta.md)

---

## 7. Comandos operativos

### Instalación y actualización

```bash
~/Projects/np-auditor/scripts/install-mcp.sh
~/Projects/np-auditor/scripts/update.sh    # git pull + reinstall
```

### Terminal (operador — preferido)

```bash
cd ~/Projects/home-hub

./scripts/np-auditor-session-check.sh              # al iniciar sesión
./scripts/np-auditor-audit.sh -f prompt.md --suggest
./scripts/np-auditor-suggest.sh --copy-only <<'EOF'
tu prompt aquí...
EOF
./scripts/np-auditor-smoke.sh                      # smoke test
./scripts/np-auditor-off.sh                        # MCP off (recomendado)
./scripts/np-auditor-on.sh                         # MCP on bajo demanda
```

### API remota (operador)

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-api.sh start
# + Cloudflare tunnel para testers
```

---

## 8. Modelo de uso por perfil

| Perfil | Flujo recomendado |
|---|---|
| **Operador local** | Terminal + MCP off. `np-auditor-audit.sh` o `/np` |
| **Beta tester remoto** | MCP on con API key. Sin motor en su Mac |
| **Agente instalador** | [`docs/install/AGENT-beta-remote.md`](docs/install/AGENT-beta-remote.md) |
| **OpenClaw / Telegram** | Skill `np-router` + `np_select_model` |

### Cuándo auditar

| Situación | Acción |
|---|---|
| Prompt caro, vago o riesgoso | `np_audit_input` |
| Pagos, producción, deploy | `np_agent_risks` (domain: `payment` / `prod`) |
| Respuesta con claims técnicos | `np_verify_response` |
| `riesgo_loop=high` | Pedir objetivo y criterio de éxito al usuario |
| Chat casual | **No auditar** |

---

## 9. Skills disponibles

| Skill | Plataforma | Archivo |
|---|---|---|
| `np-auditor` | Cursor | `skill/np-auditor/SKILL.md` |
| `np-router` | OpenClaw / Telegram | `skill/np-router/SKILL.md` |
| `antigravity` | Gemini CLI | `skill/antigravity/SKILL.md` |
| OpenAI | GPT agents | `skill/openai/instructions.md` |

`np-router` es para routing de modelos en Telegram — no sustituye `np-auditor` en Cursor.

---

## 10. Estado actual

| Métrica | Valor |
|---|---|
| Versión cliente | `0.1.20338` |
| Organismo público | 20 338 dims |
| Plataformas | Cursor, Claude, Antigravity, OpenAI |
| Licencia | MIT (cliente + skill) |
| Motor | Privado en home-hub |

---

## 11. Para agentes Cursor

Al iniciar sesión en este repo:

1. Leer **este archivo** (`cursor.md`).
2. Leer `skill/np-auditor/SKILL.md` si vas a usar las tools.
3. Verificar backend: `HOME_HUB_ROOT` + `NP_BRAIN_HOME` **o** API remota.
4. **No** auto-invocar tools — solo si el usuario lo pide.
5. **No** loops audit/suggest/verify.
6. Presentar verify en lenguaje claro, no JSON crudo.
7. `np_suggest_prompt` → usuario pega manualmente.
8. **No** commit/push salvo petición explícita del humano.

### Docs de referencia

| Doc | Contenido |
|---|---|
| [`docs/producto.md`](docs/producto.md) | Qué es para usuarios |
| [`docs/install/cursor.md`](docs/install/cursor.md) | Instalación Cursor detallada |
| [`docs/uso-terminal.md`](docs/uso-terminal.md) | Terminal + MCP on/off |
| [`docs/api-beta.md`](docs/api-beta.md) | API remota |
| [`docs/entrenamiento-prompts.md`](docs/entrenamiento-prompts.md) | Auditar ≠ entrenar |
| [`docs/actualizaciones.md`](docs/actualizaciones.md) | Mantenimiento |

---

*NP Auditor — examinar antes, verificar después. Nada más.*
