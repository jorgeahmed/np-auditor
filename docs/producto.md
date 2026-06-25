# NP Auditor — qué es (para usuarios)

NP Auditor revisa **prompts** y **respuestas** de agentes de IA **antes** de que gastes tokens o ejecutes algo riesgoso.

No es otro chatbot. Es un **examinador**: estructura del input, riesgos visibles, claims medibles en la salida.

---

## Qué hace (5 tools)

| Tool | Para qué |
|------|----------|
| `np_audit_input` | Estructura, cobertura, organismo (~502 dims), riesgo loop |
| `np_coverage` | Mapa dominios/topics KNOWN · PARTIAL · UNKNOWN |
| `np_verify_response` | Claims verificables vs alucinación |
| `np_agent_risks` | Checklist pagos / prod / general |
| `np_suggest_prompt` | Versión mejorada para **copiar** |

En Cursor: **`/np`** + pegas tu prompt (ver [uso-terminal.md](uso-terminal.md)).

---

## Cómo se conecta (beta)

El cliente MCP en este repo se conecta a un **servicio de análisis** configurado por el operador:

- **Local:** `HOME_HUB_ROOT` + `NP_BRAIN_HOME`
- **Remoto (beta):** `NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY` — ver [api-beta.md](api-beta.md)

---

## Qué NO prometemos

- No “optimizamos con otro LLM” en el audit de input (latencia ~1 s).
- No garantizamos cero errores del agente — señalamos riesgos **medibles** en lo que podemos verificar.
- No publicamos el motor de verificación en este repositorio.

---

## Más info

- Instalación: [docs/install/README.md](install/README.md)
- Uso terminal + apagar MCP: [uso-terminal.md](uso-terminal.md)
- Beta: [beta.md](beta.md)
- Actualizaciones del manifest: [actualizaciones.md](actualizaciones.md)

Documentación operativa interna del proveedor **no** forma parte de este repo.
