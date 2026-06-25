#!/usr/bin/env bash
# Actualiza NP Auditor desde GitHub (manifests + MCP). Ejecutar tras publicación diaria.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="${NP_AUDITOR_GIT_REMOTE:-origin}"
BRANCH="${NP_AUDITOR_GIT_BRANCH:-main}"

if [[ ! -d "${ROOT}/.git" ]]; then
  echo "Error: instala con git clone, no copiando archivos sueltos." >&2
  echo "  git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor" >&2
  exit 1
fi

read_version() {
  python3 -c "
import json, sys
from pathlib import Path
p = Path('${ROOT}') / 'manifests' / 'release.json'
if not p.is_file():
    print('?', end='')
    sys.exit(0)
print(json.loads(p.read_text()).get('version', '?'), end='')
" 2>/dev/null || echo "?"
}

cd "${ROOT}"
OLD="$(read_version)"
git fetch "${REMOTE}" "${BRANCH}"
git pull "${REMOTE}" "${BRANCH}"
NEW="$(read_version)"

if [[ -d mcp-server ]]; then
  "${ROOT}/scripts/install-mcp.sh"
fi

echo "NP Auditor actualizado: ${OLD} → ${NEW}"
if [[ "${OLD}" != "${NEW}" ]]; then
  echo ""
  echo "Reinicia el MCP en tu IDE:"
  echo "  Cursor → Cmd+Shift+P → Developer: Reload Window"
  echo "  (o cierra y abre Cursor)"
else
  echo "Sin cambio de versión en release.json (ya estabas al día)."
fi
