# NP Auditor — uso en terminal (auditar y apagar)

Guía operativa para **home-hub**. El MCP en Cursor va **apagado por defecto** para evitar loops de optimización en el chat.

---

## Comando slash (recomendado — como `/btw` en Claude)

En Cursor escribe **`/`** y elige:

| Comando | Qué hace |
|---------|----------|
| **`/np`** | Audita el prompt que pegues — **una pasada**, no ejecuta |
| **`/btw`** | Alias mismo flujo |

Archivos: `.cursor/commands/np.md` y `btw.md`

**Ventaja:** no necesitas tener el MCP encendido todo el día; cuando dudas, `/np` + prompt y listo.

MCP off por defecto en Settings sigue siendo OK; el comando le dice al agente cuándo auditar.

## Apagar NP Auditor en Cursor (3 formas)

### 1. Botón en Cursor (la que usaste) — recomendado

1. **Cursor Settings** → **MCP** (o **Features → MCP**)
2. Localiza **`np-auditor`**
3. **Desactiva** el toggle
4. **Reload Window** (`Cmd+Shift+P` → Developer: Reload Window)

No hace falta borrar nada; Cursor deja de cargar el servidor MCP.

### 2. Script (repo home-hub)

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-off.sh
# Reload Window en Cursor
```

Quita `np-auditor` de `.cursor/mcp.json` y guarda backup en `.cursor/mcp.np-auditor.backup.json`.

### 3. Manual

Edita `.cursor/mcp.json` y deja `"mcpServers": {}` vacío. Reload Window.

---

## Encender MCP en chat (solo si lo pides explícito)

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-on.sh
# Reload Window
```

O vuelve a activar el toggle en **Cursor Settings → MCP**.

**Regla:** una auditoría por prompt, luego `./scripts/np-auditor-off.sh` otra vez.

---

## Auditar un prompt FUERA del chat

### Paso 1 — Escribe el prompt en un archivo

```bash
nano /tmp/mi-prompt.md
```

### Paso 2 — Audita en terminal

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-audit.sh -f /tmp/mi-prompt.md --suggest
```

Obtienes:

- Estructura %, riesgo loop, riesgos payment
- Bloque **COPIAR AL COMPOSER**

### Paso 3 — Copia al Composer

Chat **nuevo** en Cursor → pegas el bloque → Enter. **Sin** NP Auditor en ese chat.

---

## Comandos útiles

| Comando | Qué hace |
|---------|----------|
| `./scripts/np-auditor-session-check.sh` | Prueba motor al inicio (bridge + agent-risk) |
| `./scripts/np-auditor-audit.sh -f X.md --suggest` | Auditoría completa en terminal |
| `./scripts/np-auditor-suggest.sh --copy-only -f X.md` | Solo prompt sugerido |
| `./scripts/np-auditor-off.sh` | MCP off en proyecto |
| `./scripts/np-auditor-on.sh` | MCP on en proyecto |
| `./scripts/np-auditor-smoke.sh` | Smoke test rápido |

Log de sesión (opcional): `.cursor/np-auditor-session.log`

---

## Hooks Cursor (proyecto)

Si usas el repo con `.cursor/hooks.json`:

- **sessionStart** → corre `session-check` en background
- **beforeSubmitPrompt** → aviso si el prompt es muy largo (>80 palabras)

Los hooks **no** auditan solos; te recuerdan usar la terminal.

---

## Modelo mental

```
Terminal (audit) → tú copias → Composer (ejecutar) → (opcional) verify una vez
```

Ver también: [entrenamiento-prompts.md](entrenamiento-prompts.md)
