# Documentación NP Auditor

| Doc | Para quién | Contenido |
|-----|------------|-----------|
| [install/README.md](install/README.md) | Todos | **Cursor · Claude · Antigravity · OpenAI** |
| [publicacion-diaria.md](publicacion-diaria.md) | Operador | Sync automático 1×/día + GitHub |
| [producto.md](producto.md) | Producto / negocio | MCP, 3 ramas, rotación, Telegram |
| [mvp-plan.md](mvp-plan.md) | Técnico | Tools, arquitectura, gaps |
| [beta.md](beta.md) | Testers | Instalación beta, feedback |

---

## Proceso completo (home-hub)

Ver en el monorepo operador:

- `projects/p-np/PROCESS.md` — flujo único
- `projects/p-np/REPO-GITHUB.md` — publicar este repo

---

## Estructura repo

```
np-auditor/
├── mcp-server/     → pip install -e .
├── skill/          → Cursor skill
├── manifests/      → dims públicas
└── docs/           → esta carpeta
```
