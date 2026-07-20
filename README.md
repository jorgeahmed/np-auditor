# NP Auditor

Auditor de inputs para agentes de IA — **medible, auditable, sin caja negra**.

Antes de que tu agente entre en un loop caro o ejecute algo riesgoso, NP Auditor revisa:

- **Antes:** estructura del prompt, riesgos, cobertura
- **Después:** afirmaciones de la respuesta vs lo medible (alucinación comprobable)

## Estado

**Beta cerrada · organismo ~20 000 dims · local o API remota**

## ¿Cómo empiezo?

| Perfil | Guía | Formato |
|--------|------|---------|
| **Beta tester** (pides a Claude/Antigravity/Cursor que instale) | [docs/install/PROMPT-usuario.md](docs/install/PROMPT-usuario.md) | Prompt copy-paste |
| **Agente instalador** | [docs/install/AGENT-beta-remote.md](docs/install/AGENT-beta-remote.md) | Markdown + JSON |
| **Manifiesto machine-readable** | [docs/install/agent-install-manifest.json](docs/install/agent-install-manifest.json) | JSON |
| **Operador** (motor en tu Mac) | [docs/install/AGENT-operator-local.md](docs/install/AGENT-operator-local.md) | Markdown |

Requiere API key del operador **o** motor local — ver [api-beta.md](docs/api-beta.md).

## Instalación rápida (humano)

### 1. Requisitos

- Cursor con MCP
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Python ≥ 3.10 (uv lo gestiona en el venv)
- Motor NP en la Mac del operador (`NP_BRAIN_HOME`) **o** API key remota

En macOS **no** uses `pip` del sistema: suele ser Python 3.9 y PEP 668 bloquea installs globales.

### 2. Clonar e instalar MCP

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

El script crea `mcp-server/.venv/` e imprime la ruta del binario.

### 3. Variables (beta local)

```bash
export NP_BRAIN_HOME="/path/to/home-hub/storage/pnp/local/p-np"
export HOME_HUB_ROOT="/path/to/home-hub"
```

### 4. Cursor (`~/.cursor/mcp.json`)

Usa la **ruta absoluta** al binario del venv (no está en el PATH global):

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/path/to/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "NP_BRAIN_HOME": "/path/to/storage/pnp/local/p-np",
        "HOME_HUB_ROOT": "/path/to/home-hub"
      }
    }
  }
}
```

Plantilla: [`config/examples/cursor-mcp.json`](config/examples/cursor-mcp.json)

### 5. Skill Cursor

Copia `skill/np-auditor/` a `.cursor/skills/np-auditor/` en tu proyecto.

## Tools

| Tool | Descripción |
|------|-------------|
| `np_audit_input` | Audita prompt (estructura, cobertura, organismo) |
| `np_coverage` | Mapa KNOWN/PARTIAL/UNKNOWN por dominio |
| `np_verify_response` | Verifica claims / alucinación |
| `np_agent_risks` | Riesgos payment / prod / general |
| `np_select_model` | Elige modelo OpenClaw (Ollama local o NVIDIA NIM) |
| `np_suggest_prompt` | Prompt mejorado para copiar |
| `np_audit_code` | Audita un repo externo: SAST (341 firmas, CWE), secretos hardcodeados, dependencias vulnerables (SCA vs. OSV.dev) e infraestructura como código (Terraform/Kubernetes) |

## Paquetes

El MCP se descarga gratis y funciona completo en su tier **Free**. Los motores
adicionales de `np_audit_code` se activan por tier (`NP_AUDITOR_TIER`, o
automáticamente con API key B2B):

| Tier | `np_audit_code` incluye |
|------|-------------------------|
| **Free** (default) | SAST — banco completo de 341 firmas verificadas (CWE) |
| **Pro** | + calidad de código + alucinaciones de IA |
| **Team** | + SCA — dependencias vs. OSV.dev en vivo |
| **Business / Enterprise** | + IaC — Terraform/Kubernetes · API remota · white-label |

Los tiers de pago se activan con el operador — contacto abajo. Las demás 6
tools (prompt, cobertura, riesgos, verificación, modelo, sugerencia) están
disponibles en todos los tiers.

## Beta remota (API)

Sin motor local: [docs/api-beta.md](docs/api-beta.md) — `NP_AUDITOR_API_URL` + API key.
La auditoría completa de código vía API (`/v1/auditcode`) está limitada por plan
del tenant — hoy, un solo cliente B2B tiene acceso al sistema completo.

## Manifest

Subset público de dimensiones: [`manifests/dims-subset.json`](manifests/dims-subset.json)

## Instalación multi-plataforma

| Plataforma | Guía |
|------------|------|
| Cursor | [docs/install/cursor.md](docs/install/cursor.md) |
| Claude | [docs/install/claude.md](docs/install/claude.md) |
| Antigravity | [docs/install/antigravity.md](docs/install/antigravity.md) |
| OpenAI | [docs/install/openai.md](docs/install/openai.md) |

Actualizaciones automáticas: [docs/publicacion-diaria.md](docs/publicacion-diaria.md)

## Documentación

| Doc | Contenido |
|-----|-----------|
| [docs/INDEX.md](docs/INDEX.md) | Índice |
| [docs/producto.md](docs/producto.md) | Qué es (usuario) |
| [docs/beta.md](docs/beta.md) | Programa beta |

Arquitectura interna del motor **no** se publica en este repositorio.

## Licencia

MIT — cliente MCP y skill. El motor de sensores no se distribuye en este repo.
