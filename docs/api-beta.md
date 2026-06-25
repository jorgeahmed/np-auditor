# NP Auditor — API beta (v0.2)

HTTP remoto para testers **sin** instalar `NP_BRAIN_HOME` en su máquina.

## Requisitos (operador)

- Mac con home-hub + motor NP Brain
- API key generada por el operador

## Arrancar servidor

```bash
export HOME_HUB_ROOT=~/Projects/home-hub
export NP_BRAIN_HOME=~/Projects/home-hub/storage/pnp/local/p-np
export NP_AUDITOR_API_KEYS="beta-key-1,beta-key-2"   # coma-separadas
./scripts/np-auditor-api.sh
```

Por defecto: `http://127.0.0.1:8787`

### Exponer con Cloudflare Tunnel (recomendado)

```bash
cloudflared tunnel --url http://127.0.0.1:8787
```

Entrega la URL pública a cada tester con su API key.

## Endpoints

| Método | Ruta | Body JSON |
|--------|------|-----------|
| GET | `/health` | — |
| POST | `/v1/audit` | `{"prompt": "..."}` |
| POST | `/v1/coverage` | `{"prompt": "..."}` |
| POST | `/v1/risks` | `{"prompt": "...", "domain": "payment\|prod\|general"}` |
| POST | `/v1/verify` | `{"response_text": "..."}` o `{"claims": [...]}` |
| POST | `/v1/suggest` | `{"prompt": "..."}` |

## Autenticación

Header:

```
Authorization: Bearer <NP_AUDITOR_API_KEY>
```

o

```
X-NP-Auditor-Key: <NP_AUDITOR_API_KEY>
```

## MCP con API remota (tester)

El tester **sí** instala el cliente MCP en su máquina (stdio local → HTTP remoto):

```bash
git clone https://github.com/jorgeahmed/np-auditor.git ~/Projects/np-auditor
~/Projects/np-auditor/scripts/install-mcp.sh
```

En `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "np-auditor": {
      "command": "/Users/TU/Projects/np-auditor/mcp-server/.venv/bin/np-auditor-mcp",
      "env": {
        "NP_AUDITOR_API_URL": "https://tu-tunel.trycloudflare.com",
        "NP_AUDITOR_API_KEY": "beta-key-1"
      }
    }
  }
}
```

Sin `HOME_HUB_ROOT` ni `NP_BRAIN_HOME` en la máquina del tester.

## Límites beta

- ~120 requests/hora por API key (configurable `NP_AUDITOR_API_RATE_PER_HOUR`)
- Sin garantía SLA — uso piloto
- El motor no se distribuye; solo JSON de audit

## curl de prueba

```bash
curl -s -X POST http://127.0.0.1:8787/v1/coverage \
  -H "Authorization: Bearer beta-key-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Deploy USDC payment agent to prod without cap"}' | jq .
```
