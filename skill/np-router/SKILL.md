---
name: np-router
description: >-
  En cada mensaje de Telegram (no slash NP Brain), invocar np_select_model ANTES
  de razonar. Usar el openclaw_model devuelto. Frontier NVIDIA solo si tier lo indica.
  DeepSeek R1 es local; NVIDIA usa V4 flash/pro.
---

# NP Model Router (OpenClaw + Telegram)

## Flujo obligatorio

1. Si el mensaje empieza con `/cerebro`, `/organismo`, `/promptlab`, etc. → ejecutar script Jarvis, **no** escalar LLM.
2. Si no → `np_select_model(prompt)`.
3. Si `clarify_first=true` → pedir objetivo y criterio de éxito; no usar modelo grande.
4. Responder usando el modelo indicado en `openclaw_model`.
5. Tras respuestas técnicas con claims → `np_verify_response` (una pasada).

## NVIDIA vs local

- **Local default:** `ollama/qwen3.5:4b` (rápido) o `9b` (agente).
- **NVIDIA frontier:** solo si tier `frontier_nvidia` / `ultra_nvidia` o usuario pide "nvidia/nim".
- **DeepSeek R1:** solo Ollama (`deepseek-r1:14b`). No existe en NIM.

## No hacer

- No auditar en loop (audit → suggest → re-audit).
- No usar frontier NVIDIA para "hola" o status corto.
- No inventar modelos; usar solo output de `np_select_model`.
