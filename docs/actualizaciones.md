# Cómo recibir actualizaciones (instaladores MCP)

## Resumen

| Modo | Quién actualiza | Cuándo |
|------|-----------------|--------|
| **Beta local** (hoy) | Tú, con `git pull` + `update.sh` | Horas después del push a GitHub |
| **Cloud** (v0.2) | Servidor NP | Automático, sin acción tuya |

Publicamos en GitHub **como máximo 1× al día** cuando hay dims nuevas o ciclo de producto completo. El push suele ocurrir en la ventana del cron (24h); tú puedes actualizar **cuando quieras** después.

---

## Instalación recomendada (permite actualizar)

Requisito: [uv](https://docs.astral.sh/uv/) (no `pip` del sistema en macOS).

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

Configura MCP con la ruta del venv:

`/Users/TU/Projects/np-auditor/mcp-server/.venv/bin/np-auditor-mcp`

Ver [install/cursor.md](install/cursor.md).

**No copies** la carpeta a mano: sin `.git` no hay `update.sh`.

---

## Actualizar (manual, ~30 s)

```bash
~/Projects/np-auditor/scripts/update.sh
```

Hace `git pull`, reinstala el MCP en `mcp-server/.venv`, y muestra la versión (`manifests/release.json`).

Luego **recarga Cursor** (Reload Window) para que el servidor MCP arranque de nuevo.

---

## Actualizar automático (opcional)

En macOS/Linux, cron local del usuario (ejemplo: revisar cada 6 h):

```bash
crontab -e
# Añade (ajusta ruta):
0 */6 * * * /Users/TU/Projects/np-auditor/scripts/update.sh >> /tmp/np-auditor-update.log 2>&1
```

Solo descarga cambios; **sigues necesitando recargar el IDE** si cambió el código MCP. Los manifests nuevos los lee el bridge desde tu motor local en beta — el manifest público es la referencia de versión.

---

## Saber si hay versión nueva sin pull

Compara tu `release.json` local con el remoto:

```bash
curl -fsSL https://raw.githubusercontent.com/jorgeahmed/np-auditor/main/manifests/release.json | python3 -m json.tool
```

Campo `version` (ej. `0.1.502`) y `published_utc`.

---

## GitHub Releases (opcional)

Puedes activar **Watch → Custom → Releases** en el repo para email cuando etiquetemos una release. En v0.1 usamos commits en `main`; las releases etiquetadas llegarán en v0.2.

---

## Beta local vs cloud

- **Beta local:** las **dimensiones del organismo** viven en tu motor (`storage/pnp/local/p-np`). GitHub publica el *subset* verificable; no sincroniza tu banco privado automáticamente.
- **Cloud (API):** el MCP llama HTTP; instala igual con `install-mcp.sh` y configura `NP_AUDITOR_API_URL` + key.
