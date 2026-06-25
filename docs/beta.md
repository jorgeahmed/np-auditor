# NP Auditor — Programa beta

## Perfil que buscamos

- Usas **Cursor**, **Claude** o **Antigravity** con agentes a diario
- Te preocupa **quemar tokens** en prompts vagos o loops
- Te interesa saber si la IA **inventa** en temas que importan (verify post-respuesta)

## Compromiso (2 semanas)

1. Instalar MCP + skill (te guiamos, ~15 min) — ver [beta-onboarding-tester.md](beta-onboarding-tester.md)
2. **Antes** de prompts importantes → `np_audit_input` (una pasada)
3. **Después** de respuestas con afirmaciones técnicas → `np_verify_response` (una pasada)
4. Una call de feedback de 20 min al final

## Qué recibes

- Acceso beta **gratis 60 días**
- Soporte directo del equipo
- Precio **founder** si pasas a pago tras beta

## Feedback que necesitamos

1. ¿Entendiste los informes (antes y después) sin ser técnico?
2. ¿Te ahorró al menos una iteración inútil?
3. ¿Verify te ayudó a detectar respuestas dudosas?
4. ¿Pagarías por esto? ¿Cuánto? (rango)
5. ¿Qué feature falta?

## Reportar issues

Abre issue en GitHub con:

- `prompt` (redactado) + output de `np_audit_input` si aplica
- `respuesta` (redactada) + output de `np_verify_response` si aplica
- qué esperabas vs qué obtuviste

## KPIs internos (no compartir con testers)

- Instalación OK en < 10 min
- ≥ 5 audits/semana/usuario
- ≥ 2/3 dirían “lo usaría pagando”
