# NP Auditor — ¿los prompts entrenan dimensiones?

## Respuesta corta

**No.** Auditar un prompt **no crea dims nuevas** en el organismo.

Las dimensiones solo entran por **medición en código** (R1: `sensor_profundo` / `destilacion`), vía scripts como `run_agent_risk_train_v1.py` y el cron `pnp-entrenamiento-auto`.

---

## Qué hicieron nuestros prompts de prueba

| Prompt | Estructura | Dims nuevas | Gaps registrados |
|--------|------------|-------------|------------------|
| Deploy + pagos USDC (viejo) | 100% → 85% | **0** | **0** |
| Deploy + pagos (reescrito) | 85% | **0** | **0** |
| Smoke / mi-prompt.md | ~80% | **0** | **0** |

**Organismo:** sigue en **352 dims** · **agent-risk 6/6** (meta producto: **10**).

---

## Por qué no hubo entrenamiento

1. **`np-auditor-audit.sh`** llama al bridge → `analyze_request` → heurísticas + cobertura. **No ejecuta sensores.**

2. **Cobertura organismo** usa keywords (`nernst`, `hook`, `verify`, …). Prompts operativos (deploy, USDC, Telegram) **no coincidían** con esos topics → cobertura vacía → **0 gaps** en `prompt_lab.gaps`.

3. **Entrenamiento automático** (`run_entrenamiento_auto_v1.py` cada 30m) solo corre experimentos de **semillas pendientes** en la rama activa (`agent-ops` ahora). Muchos ticks con `n_intentos: 0` = no hay semillas pendientes para esa rama.

4. **Publicación GitHub** marcada `pending` (ciclo rotación completo) pero cron 24h aún no publicó.

---

## Qué sí registra un audit (puente a futuro)

Con `sync_limbico=True` (default en audit), si el prompt menciona un topic **UNKNOWN**, se acumula en:

```
cerebro estado → extras.prompt_lab.gaps
```

Eso alimenta **inbox v2** (priorizar qué entrenar), **no** entrena solo.

Tras ampliar hints de cobertura para `usdc` / `deploy` / `agent_risk`, los audits de pago **sí** aparecerán en cobertura como KNOWN/PARTIAL (dims ya medidas).

---

## Qué falta para seguir entrenando

| Prioridad | Acción | Script / cron |
|-----------|--------|----------------|
| P0 | +4 dims agent-risk (6→10) | `run_agent_risk_train_v1.py` |
| P1 | Semillas en rama `agent-ops` (hooks, SAST) | explorador + semillas |
| P1 | Fixtures gold estables (8) | `pnp-prompt-lab.sh` |
| P2 | Cron publicación diaria | `./scripts/np-auditor-install-daily-publish.sh` |
| P2 | Inbox gaps → semillas automáticas | fase v2 |

---

## Cómo entrenar de verdad (operador)

```bash
cd ~/Projects/home-hub

# Agent-risk (+dims medidas)
./scripts/pnp-py.sh run_agent_risk_train_v1.py

# Tick entrenamiento (semillas rama activa)
./scripts/pnp-entrenamiento-auto.sh tick

# Prompt Lab fixture (eval, no entrena banco)
./scripts/pnp-prompt-lab.sh eval agent_pay_no_cap --backend gold
```

---

## Resumen

| Acción | ¿Entrena dims? |
|--------|----------------|
| `np-auditor-audit.sh` | No — examina prompt |
| `np_suggest_prompt` | No — reescribe reglas |
| `run_agent_risk_train_v1.py` | **Sí** |
| Cron entrenamiento-auto | **Sí**, si hay semillas pendientes |
| Prompt Lab eval | No — benchmark fixtures |

Los prompts de esta sesión **validaron** el producto (estructura, riesgos, coste tokens); **no** ampliaron el organismo. Siguiente paso de producto: **+4 dims agent-risk** y semillas **agent-ops**.
