# NP Auditor — qué es (para usuarios)

NP Auditor revisa **prompts** y **respuestas** de agentes de IA en **dos momentos**:

1. **Antes** — ¿tu instrucción está clara y es segura?
2. **Después** — ¿lo que la IA respondió choca con lo que el sistema puede medir?

No es otro chatbot. Es un **examinador**: estructura del input, riesgos visibles, y verificación de afirmaciones medibles en la salida.

---

## Flujo de uso (recomendado)

```
ANTES                          DESPUÉS
──────                         ───────
Prompt importante              IA ya respondió
      ↓                              ↓
np_audit_input (1×)            np_verify_response (1×)
      ↓                              ↓
Ajustas y ejecutas             Decides si confías
```

**Regla:** una pasada por fase. No loops audit → suggest → audit ni verify repetido.

---

## Qué hace (5 tools)

| Tool | Cuándo | En criollo |
|------|--------|------------|
| `np_audit_input` | **Antes** del prompt | ¿Está claro? ¿Riesgo de dar vueltas? |
| `np_coverage` | **Antes** (opcional) | ¿Qué temas cubre tu prompt? |
| `np_agent_risks` | **Antes** (pagos/prod) | Checklist de riesgos visibles |
| `np_suggest_prompt` | **Antes** (opcional) | Versión mejorada para **copiar** |
| `np_verify_response` | **Después** de la respuesta | ¿Contradicciones / alucinación medible? |

---

## Verify (después de respuestas) — qué esperar

`np_verify_response` contrasta afirmaciones de la IA con el organismo (~502 dims entrenadas).

| Resultado | Significado |
|-----------|-------------|
| **Verificados** | Cuadran con lo medido |
| **Contradichos** | Chocan con lo medido — revisar con cuidado |
| **Alucinación (medible)** | % de error solo sobre claims comprobables |
| **Sin claims medibles** | Opiniones o temas fuera de alcance — no es veredicto |

No fact-checka internet ni garantiza cero errores en todo el texto.

---

## Cómo se conecta (beta)

- **Local:** `HOME_HUB_ROOT` + `NP_BRAIN_HOME`
- **Remoto (beta):** `NP_AUDITOR_API_URL` + `NP_AUDITOR_API_KEY` — [api-beta.md](api-beta.md)

Onboarding testers: [beta-onboarding-tester.md](beta-onboarding-tester.md)

---

## Qué NO prometemos

- No “optimizamos con otro LLM” en el audit (~1 s, $0 LLM en el path local).
- No garantizamos cero alucinaciones — señalamos contradicciones **medibles**.
- No publicamos el motor de verificación en este repositorio.

---

## Más info

- Instalación: [docs/install/README.md](install/README.md)
- Beta: [beta.md](beta.md)
- Actualizaciones: [actualizaciones.md](actualizaciones.md)
