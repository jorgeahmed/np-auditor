# NP Auditor

Auditor de inputs para agentes de IA — **medible, auditable, sin caja negra**.

Antes de que tu agente entre en un loop caro o ejecute algo riesgoso, NP Auditor revisa:

- **Estructura del prompt** (objetivo, criterio de éxito)
- **Confiabilidad de la respuesta** (claims verificados vs alucinados)
- **Riesgos del agente** (pagos, prod, acciones amplias)

## Estado

**Beta cerrada · organismo 502 dims · local o API remota**

Requiere motor NP Brain en local (`NP_BRAIN_HOME`) **o** API beta con key — ver [api-beta.md](docs/api-beta.md).

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
| `np_audit_input` | Audita prompt (estructura, cobertura, organismo) |
| `np_coverage` | Mapa KNOWN/PARTIAL/UNKNOWN por dominio |
| `np_verify_response` | Verifica claims / alucinación |
| `np_agent_risks` | Riesgos payment / prod / general |
| `np_suggest_prompt` | Prompt mejorado para copiar |

## Beta remota (API)

Sin motor local: [docs/api-beta.md](docs/api-beta.md) — `NP_AUDITOR_API_URL` + API key.

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
