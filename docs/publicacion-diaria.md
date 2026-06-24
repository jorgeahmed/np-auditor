# Publicación diaria automática

Sí, **se puede**: el bot/repo público se actualiza **como máximo una vez al día**, solo si hubo trabajo en el ciclo.

---

## Cómo funciona

```mermaid
sequenceDiagram
  participant T as Entrenamiento 30m
  participant S as Estado cerebro
  participant D as Cron 24h
  participant P as np-auditor publish
  participant G as GitHub optional

  T->>S: EUREKA o ciclo A→B→C completo
  S->>S: pending=true
  D->>P: publish (si pending)
  P->>P: ¿último publish hace 24h?
  alt OK
    P->>P: sync manifest + telegram-help
    P->>G: git push si AUTO_PUSH=1
    P->>S: pending=false
  else ya publicado hoy
    P->>S: skip hasta mañana
  end
```

| Evento | Efecto |
|--------|--------|
| Dim nueva (EUREKA) | Marca `pending` |
| Ciclo rotación completo (vuelve a `agent-risk`) | Marca `pending` |
| Cron **24h** | Publica si `pending` y no publicó hoy |
| Segundo ciclo mismo día | Queda `pending` hasta el día siguiente |

---

## Qué se actualiza

| Archivo | Contenido |
|---------|-----------|
| `manifests/dims-subset.json` | Dims públicas desde banco |
| `manifests/release.json` | Versión, organismo, plataformas |
| `docs/telegram-help.txt` | Comandos Jarvis/Telegram |

Opcional: **git push** al repo `np-auditor`.

---

## Instalar cron (una vez)

```bash
cd ~/Projects/home-hub
./scripts/np-auditor-install-daily-publish.sh
```

Crea job OpenClaw `np-auditor-daily-publish` cada **24h**.

---

## Variables (`config/.env`)

```bash
# Activar push automático tras sync
NP_AUDITOR_AUTO_PUSH=1

# Repo dedicado (opcional): rsync + push ahí
NP_AUDITOR_PUBLISH_CLONE=~/Projects/np-auditor

NP_AUDITOR_GIT_REMOTE=origin
NP_AUDITOR_GIT_BRANCH=main
```

Sin `NP_AUDITOR_AUTO_PUSH=1` solo sincroniza archivos locales (sin git push).

---

## Comandos manuales

```bash
./scripts/np-auditor-publish.sh status    # pending / último publish
./scripts/np-auditor-publish.sh sync      # regenerar manifest ya
./scripts/np-auditor-publish.sh publish   # respeta límite 24h
./scripts/np-auditor-publish.sh publish --force   # ignorar 24h
./scripts/np-auditor-publish.sh pending --reason test
```

---

## Telegram

El cron puede anunciar resultado a tu chat (mismo `TELEGRAM_CHAT_ID` que otros crons).

El archivo `docs/telegram-help.txt` en el repo público refleja los comandos actuales del bot.
