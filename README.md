# NP Auditor

Auditor de inputs para agentes de IA — **medible, auditable, sin caja negra**.

Antes de que tu agente entre en un loop caro o ejecute algo riesgoso, NP Auditor revisa:

- **Estructura del prompt** (objetivo, criterio de éxito)
- **Confiabilidad de la respuesta** (claims verificados vs alucinados)
- **Riesgos del agente** (pagos, prod, acciones amplias)

## Estado

**Beta cerrada · MVP 0.1 · local first**

Requiere motor NP Brain en local (`NP_BRAIN_HOME`) durante la beta. Cloud API en v0.2.

## Instalación rápida

### 1. Requisitos

- Cursor con MCP
- Python ≥ 3.10
- Motor NP en la Mac del operador (`NP_BRAIN_HOME`)

### 2. Variables

```bash
export NP_BRAIN_HOME="/path/to/home-hub/storage/pnp/local/p-np"
export HOME_HUB_ROOT="/path/to/home-hub"
```

### 3. Instalar MCP

```bash
cd mcp-server
pip install -e .
```

### 4. Cursor (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "np-auditor-mcp",
      "env": {
        "NP_BRAIN_HOME": "/path/to/storage/pnp/local/p-np",
        "HOME_HUB_ROOT": "/path/to/home-hub"
      }
    }
  }
}
```

### 5. Skill Cursor

Copia `skill/np-auditor/` a `.cursor/skills/np-auditor/` en tu proyecto.

## Tools

| Tool | Descripción |
|------|-------------|
| `np_audit_input` | Audita prompt antes de enviarlo al agente |
| `np_verify_response` | Verifica claims / alucinación |
| `np_agent_risks` | Riesgos payment / prod / general |

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
| [docs/INDEX.md](docs/INDEX.md) | Índice completo |
| [docs/producto.md](docs/producto.md) | Producto, rotación, Telegram |
| [docs/mvp-plan.md](docs/mvp-plan.md) | Plan técnico MVP |
| [docs/beta.md](docs/beta.md) | Programa beta |

## Licencia

MIT — cliente MCP y skill. El motor de sensores no se distribuye en este repo.
