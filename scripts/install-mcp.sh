#!/usr/bin/env bash
# Instala np-auditor-mcp en venv local (uv). Idempotente.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP="${ROOT}/mcp-server"

if [[ ! -f "${MCP}/pyproject.toml" ]]; then
  echo "Error: no encuentro ${MCP}/pyproject.toml" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: falta uv (gestor Python recomendado)." >&2
  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
  echo "  https://docs.astral.sh/uv/" >&2
  exit 1
fi

cd "${MCP}"
uv venv .venv --allow-existing
uv pip install -e .

BIN="${MCP}/.venv/bin/np-auditor-mcp"
if [[ ! -x "${BIN}" ]]; then
  echo "Error: no se generó ${BIN}" >&2
  exit 1
fi

"${MCP}/.venv/bin/python" -c "import np_auditor_mcp" >/dev/null

echo "NP Auditor MCP instalado."
echo ""
echo "  Binario: ${BIN}"
echo ""
echo "Pega esta ruta en \"command\" de tu config MCP (Cursor, Claude, etc.)."
echo "Plantillas: ${ROOT}/config/examples/"
