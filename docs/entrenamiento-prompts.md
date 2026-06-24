# ¿Auditar un prompt entrena el sistema?

**No.** Usar NP Auditor **no** amplía el catálogo de checks por sí solo.

Auditar = **una evaluación** de tu prompt o respuesta en ese momento. El producto mejora en el tiempo porque el proveedor actualiza el backend de verificación; eso ocurre **fuera** de este repo y no depende de tus prompts de prueba.

---

## Qué obtienes al auditar

- Score de estructura (objetivo, criterio, paths)
- Riesgo de loop (heurístico)
- Riesgos de contexto (pagos, prod)
- Sugerencia de prompt para copiar (`/np` o `np_suggest_prompt`)

---

## Versión pública del manifest

[`manifests/dims-subset.json`](../manifests/dims-subset.json) lista un **subset** de capacidades verificadas (IDs + descripción corta). Es la referencia de versión (`0.1.N`), no el código que las implementa.

---

## Para operadores del piloto

Detalle técnico del motor: documentación privada en el entorno del operador (home-hub), no en GitHub.
