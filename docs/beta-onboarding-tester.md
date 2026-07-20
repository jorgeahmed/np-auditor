# NP Auditor — onboarding beta tester

Plantilla para enviar por **DM** (nunca en canal público). Sustituye `{{NOMBRE}}`, `{{PLATAFORMA}}`, `{{API_URL}}`, `{{API_KEY}}`.

---

## Mensaje para el tester

Hola {{NOMBRE}},

Te doy acceso a la **beta cerrada de NP Auditor** (piloto 2 semanas).

### Qué es (y qué no es)

NP Auditor **no es otro chatbot** ni un agente que hace el trabajo por ti. Tiene **dos momentos**:

1. **Antes** — revisa lo que vas a pedirle a la IA (¿está claro? ¿es arriesgado?).
2. **Después** — revisa lo que la IA te respondió (¿dice cosas que chocan con lo medible?).

- ✅ Una pasada por fase (~1 s cada una), informe claro
- ❌ No optimiza en bucle dentro del chat
- ❌ No sustituye a tu agente (Claude, Cursor, Antigravity)
- ❌ No instala el “cerebro” en tu Mac — te conectas a nuestra API

### Tus credenciales (solo tuyas — no compartir)

```
API URL:  {{API_URL}}
API key:  {{API_KEY}}
```

Repo: https://github.com/jorgeahmed/np-auditor

---

### Paso 1 — Instalación (una vez)

Abre **{{PLATAFORMA}}** y pega este prompt al agente para que instale por ti:

```
Instala NP Auditor beta remota siguiendo EXACTAMENTE:
https://github.com/jorgeahmed/np-auditor/blob/main/docs/install/AGENT-beta-remote.md

Lee también:
https://github.com/jorgeahmed/np-auditor/blob/main/docs/install/agent-install-manifest.json

Soy beta tester REMOTO. NO uses HOME_HUB_ROOT ni NP_BRAIN_HOME.

Plataforma: {{PLATAFORMA}}
OS: (detecta el mío)
API URL: {{API_URL}}
API key: {{API_KEY}}

Usa scripts/install-mcp.sh (uv, nunca pip del sistema).
Configura MCP con config/examples/beta-remote-*.json (ruta absoluta al venv).
Copia el skill correspondiente.
Verifica: curl {{API_URL}}/health y que aparezcan 5 MCP tools.
Al terminar, explícame en palabras simples:
  (a) cómo auditar ANTES de un prompt importante
  (b) cómo verificar DESPUÉS de una respuesta de la IA
```

Plataformas válidas: `Claude Desktop`, `Claude Code`, `Cursor`, `Antigravity`.

---

### Paso 2 — Uso adecuado (importante)

#### Fase A — ANTES de pedirle trabajo a la IA

**Cuándo:** refactor grande, deploy, pagos, prompt largo o vago.

```
1. Escribes lo que quieres pedir
2. Pides UNA revisión previa (np_audit_input)
3. Lees el aviso (claridad, riesgos, cobertura)
4. Ajustas tu mensaje si hace falta
5. Entonces sí le pides el trabajo a tu agente
```

**Frase tipo:** *"Audita con np_audit_input (una sola pasada): [tu prompt]"*

**Qué mirar:**

| Te dice | Significa (en criollo) |
|---------|------------------------|
| Riesgo de loop alto | Tu pedido es vago — añade qué quieres lograr y cómo sabrás que salió bien |
| Cobertura / temas | Qué tipo de cosas el sistema conoce bien vs. dónde va más a ciegas |
| Riesgos pagos/prod | Alertas si tocas dinero, producción o acciones delicadas |

#### Fase B — DESPUÉS de que la IA responda

**Cuándo:** la respuesta trae afirmaciones fuertes — números, “siempre funciona”, pasos técnicos, garantías de prod.

```
1. La IA ya te contestó
2. Pides UNA verificación (np_verify_response) pegando esa respuesta
3. Lees si hay contradicciones en lo que SÍ se pudo medir
4. Tú decides si confías, pides aclaración o corriges
```

**Frase tipo:** *"Verifica con np_verify_response (una sola pasada) esta respuesta: [pega lo que dijo la IA]"*

**Qué mirar:**

| Te dice | Significa (en criollo) |
|---------|------------------------|
| Medibles / verificados | Cuántas afirmaciones se pudieron contrastar con el motor |
| Contradichos | La respuesta choca con lo medido — ojo, puede ser alucinación |
| Alucinación (medible) | % de error **solo sobre lo comprobable**, no sobre todo el texto |
| Sin claims medibles | Opiniones o temas fuera de alcance — no es “bien” ni “mal”, simplemente no se pudo medir |

**Importante:** verify **no** fact-checka internet ni cualquier dato del mundo. Contrasta con lo que el organismo (~20 000 dimensiones) puede medir. No promete cero errores en general.

#### Otras tools (opcionales)

| Situación | Qué decir |
|-----------|-----------|
| Ver dominios del prompt | *"np_coverage sobre: [prompt]"* |
| Pagos / prod / deploy | *"np_agent_risks domain=payment (o prod): [prompt]"* |
| Mejorar redacción | *"np_suggest_prompt — texto para copiar, no ejecutes"* |

#### Reglas (evitan mal uso)

1. **Una pasada por fase** — no encadenes audit → suggest → audit ni verify → verify → verify.
2. **`np_suggest_prompt` es para copiar** — pegas la versión mejorada en un mensaje nuevo.
3. **No audites cada mensaje** — solo lo importante (caro, riesgoso, vago).
4. **Verify después, no antes** — tiene sentido cuando ya hay respuesta que cuestionar.
5. **No publiques tu API key** en Discord, GitHub ni screenshots.
6. **~120 requests/hora** por key — uso normal de piloto.

#### Flujo completo (ejemplo)

```
Prompt importante → audit (1×) → ajustas → agente trabaja → respuesta con claims → verify (1×) → tú decides
```

---

### Paso 3 — Feedback (2 semanas)

1. ¿Entendiste los informes (antes y después) sin ser técnico?
2. ¿Te ahorró al menos una iteración inútil o una respuesta dudosa?
3. ¿Lo usarías pagando? ¿Cuánto? (rango)
4. ¿Usaste verify después de respuestas? ¿Fue útil?

Issues: https://github.com/jorgeahmed/np-auditor/issues (prompt + respuesta redactados + output del informe)

---

### Si no conecta

- Prueba: `curl {{API_URL}}/health` → debe decir `"ok": true`
- Si falla: avísame (beta — depende de que el servidor operador esté activo)
- Error 401 → key incorrecta · 429 → límite hora

Gracias por probar la beta.

---

## Ejemplo relleno — Julio Gonzalez

Credenciales en `config/np-auditor-beta-keys.local.txt` (operador).

## Ejemplo relleno — Abraham Chávez (tester #2)

Guía rápida lista para DM: `config/beta-testers/abraham-chavez-guia-rapida.md` (local, no commit).
