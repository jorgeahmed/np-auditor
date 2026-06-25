# Documentación NP Auditor

| Doc | Para quién | Contenido |
|-----|------------|-----------|
| [install/README.md](install/README.md) | Todos | Instalación humana + **agente LLM** |
| [install/PROMPT-usuario.md](install/PROMPT-usuario.md) | Testers | Prompts copy-paste para Claude/Antigravity |
| [install/agent-install-manifest.json](install/agent-install-manifest.json) | Agentes | Manifiesto JSON de instalación |
| [producto.md](producto.md) | Usuario | Qué es, flujo antes/después |
| [beta-onboarding-tester.md](beta-onboarding-tester.md) | Testers | Onboarding + uso en criollo |
| [uso-terminal.md](uso-terminal.md) | Usuario | Auditar, `/np`, apagar MCP |
| [actualizaciones.md](actualizaciones.md) | Usuario | `git pull` / update.sh |
| [beta.md](beta.md) | Testers | Piloto y feedback |
| [entrenamiento-prompts.md](entrenamiento-prompts.md) | Usuario | FAQ: auditar ≠ entrenar |
| [api-beta.md](api-beta.md) | Testers / operador | API HTTP remota |

**Operadores del piloto:** documentación del motor vive en el entorno privado (home-hub), no aquí.

---

## Repo

```
np-auditor/
├── scripts/install-mcp.sh   → uv venv + MCP (recomendado)
├── mcp-server/              → .venv/bin/np-auditor-mcp
├── skill/                   → Cursor skill + /np
├── manifests/               → versión pública verificable
└── docs/                    → esta carpeta
```
