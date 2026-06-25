# np-auditor-mcp

Servidor MCP stdio para NP Auditor (5 tools).

## Requisitos

- [uv](https://docs.astral.sh/uv/) — en macOS **no** uses `pip` del sistema (Python 3.9 / PEP 668).
- Python ≥ 3.10 (uv lo resuelve al crear el venv).

## Instalar

Desde la raíz del repo:

```bash
./scripts/install-mcp.sh
```

Manual:

```bash
cd mcp-server
uv venv .venv
uv pip install -e .
```

Verifica:

```bash
.venv/bin/python -c "import np_auditor_mcp; print('ok')"
```

## Config MCP

Usa la **ruta absoluta** al binario del venv (no está en el PATH global):

```
/path/to/np-auditor/mcp-server/.venv/bin/np-auditor-mcp
```

Plantillas: [`config/examples/`](../config/examples/).
