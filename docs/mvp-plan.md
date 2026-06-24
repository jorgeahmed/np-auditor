# NP Auditor — Plan MVP (B2C · local · GitHub-ready)

> **Copia canónica para GitHub.** Índice: [INDEX.md](INDEX.md)

**Producto:** auditor de inputs para usuarios con agentes (Cursor, OpenClaw, etc.)  
**Versión:** MVP 0.1 · local first · beta cerrada  
**Fecha:** 2026-06-22

---

## 1. Qué vendemos (una frase)

> **Antes de que el agente queme tokens o mueva plata, NP Auditor te dice qué tan claro está tu input, qué tan confiable es la respuesta y qué riesgos vesibles hay — medido, no opinión.**

---

## 2. Alcance MVP (qué entra / qué no)

### Entra en v0.1 (demo beta)

| Capacidad | Tool MCP | Tokens LLM | Latencia |
|-----------|----------|------------|----------|
| Auditar estructura del prompt | `np_audit_input` | 0 | ~1 s |
| Verificar claims de una respuesta | `np_verify_response` | 0 | ~1 s |
| Score alucinación (measurable) | incluido en verify | 0 | ~1 s |
| Riesgos agente (genérico) | `np_agent_risks` | 0 | ~1 s |
| Informe legible B2C | markdown footer | 0 | — |
| Skill Cursor | `np-auditor` | 0 | — |

### Entra en v0.2 (post-beta)

| Capacidad | Notas |
|-----------|-------|
| Eval async de variantes de prompt | Ollama local, ~minutos |
| Rama pagos (`agent_pay_*`) | Piloto B2B (Santi) |
| Cron actualización manifests | Servidor privado |
| API cloud + API key | Sin código motor |

### Fuera del MVP

- Entrenamiento de dims nuevas en cliente (Enterprise)
- Certificación bancaria / compliance
- Garantía “cero fraude”
- Motor IA10Vatios expuesto en GitHub

---

## 3. Arquitectura (local → GitHub → cloud)

```
┌─────────────────────────────────────────────────────────────────┐
│  CLIENTE (Cursor / Claude / OpenClaw)                           │
│  ~/.cursor/mcp.json  →  np-auditor-mcp (stdio)                  │
│  Skill: np-auditor                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │ JSON-RPC stdio
┌────────────────────────────▼────────────────────────────────────┐
│  REPO PÚBLICO (GitHub) — np-auditor/ (raíz repo)              │
│  • mcp-server/     servidor MCP fino (~500 LOC)                 │
│  • skill/          SKILL.md instalable                          │
│  • manifests/      subset dims verificables (sin .py)           │
│  • docs/           install, beta, FAQ                           │
└────────────────────────────┬────────────────────────────────────┘
                             │ subprocess / HTTP (v0.2)
┌────────────────────────────▼────────────────────────────────────┐
│  MOTOR PRIVADO (NO en GitHub)                                   │
│  storage/pnp/local/p-np/                                        │
│  • prompt_lab/   analyze, features, coverage                    │
│  • np_verify/    verify claims vs banco                         │
│  • sensores/     344+ dims                                      │
│  • scripts/np-auditor-bridge.sh                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Regla de oro

- **GitHub:** cliente MCP + schemas + manifests públicos + skill.
- **Privado:** sensores, motor, entrenamiento, banco completo.
- **Cliente recibe:** informes + dim ids + scores, nunca `src/sensores/*.py`.

---

## 4. Tools MCP (contrato v0.1)

### `np_audit_input`

**Input:** `{ "prompt": "...", "context": "cursor|openclaw|payment" }`  
**Output:**

```json
{
  "estructura_score": 0.8,
  "sugerencias": ["Añade criterio de éxito medible"],
  "skills_match": [],
  "coverage": [{"dominio": "...", "status": "KNOWN|UNKNOWN"}],
  "riesgo_loop": "low|medium|high",
  "footer": "── NP Auditor · input OK con mejoras ──"
}
```

`riesgo_loop`: heurística (prompt vago + sin criterio + tarea abierta = medium/high).

### `np_verify_response`

**Input:** `{ "claims": [...], "response_text": "..." }`  
**Output:**

```json
{
  "measurable": 3,
  "verified": 2,
  "contradicted": 1,
  "hallucination_rate": 0.33,
  "footer": "..."
}
```

### `np_agent_risks`

**Input:** `{ "prompt": "...", "domain": "payment|prod|general" }`  
**Output:** checklist de riesgos declarados (v0.1 estático + cobertura organismo; v0.2 dims medidas).

---

## 5. Infraestructura requerida

### Beta local (cada tester)

| Componente | Requisito | Obligatorio |
|------------|-----------|-------------|
| macOS / Linux | reciente | sí |
| Node.js | ≥ 20 | sí (MCP) |
| Python | 3.12 vía `uv` | sí (motor local) |
| Cursor | con MCP | sí |
| Ollama | qwen3.5:4b+ | opcional v0.1 |
| OpenClaw | — | opcional |
| `NP_BRAIN_HOME` | path al motor | sí (dev) |
| `NP_AUDITOR_MODE` | `local` \| `cloud` | local en beta |

### Tu máquina (operador)

| Componente | Uso |
|------------|-----|
| home-hub + p-np | motor |
| `./scripts/pnp-py.sh` | runner |
| `projects/p-np/np-auditor/` | repo a publicar (copiar raíz `np-auditor/`) |
| Logs | `storage/pnp/logs/np-auditor/` |

### Cloud v0.2 (cuando haya beta validada)

| Servicio | Función |
|----------|---------|
| API Gateway | auth, rate limit |
| Worker train | cron dims (privado) |
| CDN | manifests firmados |
| Postgres | beta keys, usage |
| **No** subir | `storage/pnp/local/p-np/src/` |

---

## 6. Qué nos hace falta (gap list)

| # | Gap | Prioridad | Esfuerzo |
|---|-----|-----------|----------|
| 1 | Servidor MCP publicable | P0 | 2–3 d |
| 2 | Bridge `np-auditor-bridge.sh` | P0 | 0.5 d |
| 3 | Skill Cursor `np-auditor` | P0 | 0.5 d |
| 4 | Manifest público dims (subset) | P0 | 1 d |
| 5 | Heurística `riesgo_loop` | P1 | 0.5 d |
| 6 | Instrumentar tokens/latency | P1 | 1 d |
| 7 | Informe B2C (markdown template) | P1 | 0.5 d |
| 8 | Fixtures `agent_pay_*` | P2 (B2B) | 3 d |
| 9 | CI GitHub Actions | P1 | 0.5 d |
| 10 | API cloud | P2 | 1–2 sem |

---

## 7. Fases de entrega

### Fase 0 — Esta semana (MVP local)

- [x] `np-auditor/` scaffold en `projects/p-np/`
- [ ] MCP stdio + 3 tools
- [ ] Bridge a motor local
- [ ] SKILL.md + README install
- [ ] Probar en home-hub

### Fase 1 — Beta cerrada (2–3 testers)

- [ ] Repo GitHub público (solo package)
- [ ] Formulario feedback (Notion/issue template)
- [ ] 3 sesiones onboarding 30 min
- [ ] Métricas: audits/día, NPS, top sugerencias

### Fase 2 — Piloto pagos (Santi)

- [ ] Rama `agent-risk/payment`
- [ ] 10 escenarios medidos
- [ ] Informe PDF + MCP ampliado

### Fase 3 — Cloud

- [ ] API + manifests sin motor en cliente
- [ ] Pricing beta → pro

---

## 8. Programa beta testers

### Perfil ideal (3–5 personas)

1. **Builder con agente + Cursor** (dev indie)
2. **Founder fintech/crypto** (Santi — pagos agenticos)
3. **DevOps / platform** (miedo prod/borrados)
4. **Power user OpenClaw** (cron + tokens)
5. **Consultor IA** (valida pitch B2C)

### Qué les pedimos

- Instalar MCP + skill (15 min)
- Usar **3 días** antes de cada prompt “grande” → `np_audit_input`
- Tras respuesta del agente → `np_verify_response` (opcional)
- 1 call feedback 20 min al final de semana 1

### Qué les damos

- Acceso beta gratis 60 días
- Soporte directo (Telegram/WhatsApp)
- Informe agregado de su uso (anónimo si quieren)
- Precio fundador locked si convierten

### KPIs beta

| Métrica | Meta v0.1 |
|---------|-----------|
| Instalaciones completadas | 3/5 |
| Audits/usuario/semana | ≥ 5 |
| “Lo usaría pagando” | ≥ 2/3 |
| Time-to-first-audit | < 10 min |

---

## 9. Publicación GitHub (checklist)

```
np-auditor/
├── README.md              ← install 3 pasos
├── LICENSE                ← MIT (cliente) / motor privado
├── packages/mcp-server/
├── skill/np-auditor/
├── manifests/dims-v0.json
├── docs/install.md
├── docs/beta.md
└── .github/workflows/ci.yml
```

**`.gitignore` del repo público:** nunca `storage/`, `p-np/`, `.env`, keys.

**Variable obligatoria en beta local:**

```bash
export NP_BRAIN_HOME="$HOME/Projects/home-hub/storage/pnp/local/p-np"
```

En cloud v0.2: `NP_AUDITOR_API_KEY` reemplaza path local.

---

## 10. Mensaje comercial MVP (B2C)

**Titular:** *Audita tu prompt antes de quemar tokens.*

**Bullets:**

- Gratis en beta: estructura del input en 1 segundo
- Score de alucinación cuando el agente responde
- Mapa de riesgos antes de loops caros
- Medible y auditable — no caja negra

**No prometer en v0.1:** 3× tokens, 4× alucinaciones (solo tras benchmark publicado).

---

## 11. Comandos operativos (MVP)

```bash
# Desarrollo
cd ~/Projects/home-hub
./scripts/np-auditor-bridge.sh audit "Objetivo: crear hook red..."
./scripts/np-auditor-bridge.sh verify '{"claims":[...]}'

# MCP (tras install)
npx @np-auditor/mcp   # stdio

# Tests
./scripts/pnp-py.sh -m pytest np-auditor/tests/
```

---

## 12. Decisión pendiente

| Opción | Pros | Contras |
|--------|------|---------|
| MCP Python (reusa pnp-py) | Rápido, un stack | Menos “npm standard” |
| MCP TypeScript + bridge | Estándar Cursor | Dos runtimes |

**Recomendación MVP:** Python MCP (`mcp` SDK) + bridge shell → publicar en 2–3 días.
