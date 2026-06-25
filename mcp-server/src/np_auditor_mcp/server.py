"""NP Auditor MCP — stdio server (beta local o API remota)."""

from __future__ import annotations

import json
import os

from mcp.server.fastmcp import FastMCP

from np_auditor_mcp.client import run_command

mcp = FastMCP("np-auditor")


@mcp.tool()
def np_audit_input(prompt: str, context: str = "general") -> str:
    """Audita un prompt antes de enviarlo al agente.

    Devuelve score de estructura, sugerencias, cobertura, organismo y riesgo de loop.
    No usa tokens LLM en el path local (~1 s).
    """
    _ = context
    data = run_command("audit", prompt)
    lines = [
        "── NP Auditor · input ──",
        f"Organismo: {data.get('organismo_dims', '?')} dims",
        f"Estructura: {data.get('estructura_score', 0):.0%}",
        f"Riesgo loop: {data.get('riesgo_loop', '?')}",
    ]
    for s in data.get("sugerencias") or []:
        lines.append(f"  → {s}")
    for c in (data.get("coverage") or [])[:6]:
        lk = c.get("lookup") or {}
        lines.append(f"  · {c.get('dominio')}/{c.get('topic')}: {lk.get('status', '?')}")
    return "\n".join(lines)


@mcp.tool()
def np_coverage(prompt: str) -> str:
    """Mapa de cobertura del organismo para un prompt.

    Muestra topics detectados, dominios activos, KNOWN/PARTIAL/UNKNOWN
    y totales del banco (502+ dims). Sin LLM.
    """
    data = run_command("coverage", prompt)
    lines = [
        "── NP Auditor · coverage ──",
        f"Organismo: {data.get('organismo_dims', '?')} dims",
    ]
    res = data.get("resumen") or {}
    lines.append(
        f"Topics: {res.get('topics_total', 0)} · "
        f"KNOWN {res.get('known', 0)} · PARTIAL {res.get('partial', 0)} · "
        f"UNKNOWN {res.get('unknown', 0)}"
    )
    activos = data.get("dominios_activos") or []
    if activos:
        por = data.get("por_dominio") or {}
        lines.append("Dominios activos:")
        for d in activos[:8]:
            lines.append(f"  · {d}: {por.get(d, '?')} dims en banco")
    for c in (data.get("topics") or [])[:8]:
        lk = c.get("lookup") or {}
        st = lk.get("status", "?")
        extra = ""
        if st == "KNOWN":
            extra = f" → {lk.get('id', '')}"
        elif st == "PARTIAL":
            extra = f" → {lk.get('n', 0)} matches"
        lines.append(f"  · {c.get('dominio')}/{c.get('topic')}: {st}{extra}")
    return "\n".join(lines)


@mcp.tool()
def np_verify_response(response_text: str = "", claims_json: str = "") -> str:
    """Verifica claims en una respuesta del agente."""
    payload: dict = {}
    if claims_json.strip():
        payload["claims"] = json.loads(claims_json)
    else:
        payload["response_text"] = response_text
    data = run_command("verify", payload=payload)
    m = data.get("measurable") or 0
    hr = data.get("hallucination_rate") or 0
    lines = [
        "── NP Auditor · verify ──",
        f"Medibles: {m} · Verificados: {data.get('verified', 0)} · "
        f"Contradichos: {data.get('contradicted', 0)}",
        f"Alucinación (medible): {hr:.0%}" if m else "Sin claims medibles",
    ]
    footer = data.get("footer")
    if footer:
        lines.append(footer)
    return "\n".join(lines)


@mcp.tool()
def np_agent_risks(prompt: str, domain: str = "general") -> str:
    """Lista riesgos visibles del agente (payment / prod / general)."""
    data = run_command("risks", prompt, domain=domain)
    lines = [
        f"── NP Auditor · riesgos ({data.get('domain', domain)}) ──",
        f"Estructura: {data.get('estructura_score', 0):.0%}",
        f"Organismo: {data.get('organismo_dims', '?')} dims",
        "",
        "Riesgos:",
    ]
    risks = data.get("risks") or []
    if not risks:
        lines.append("  · (ninguno crítico detectado)")
    for r in risks:
        lines.append(f"  · {r}")
    return "\n".join(lines)


@mcp.tool()
def np_suggest_prompt(prompt: str) -> str:
    """Genera un prompt mejorado listo para COPIAR al Composer."""
    data = run_command("suggest", prompt)
    if data.get("error"):
        raise RuntimeError(data["error"])
    suggested = data.get("prompt_sugerido", "")
    cambios = data.get("cambios") or []
    antes = data.get("estructura_antes", 0)
    despues = data.get("estructura_despues", 0)
    lines = [
        "── COPIAR AL COMPOSER (no ejecutar automáticamente) ──",
        "",
        suggested,
        "",
        "── FIN PROMPT SUGERIDO ──",
        f"Cambios: {', '.join(cambios) if cambios else 'ninguno'}",
        f"Estructura: {antes:.0%} → {despues:.0%}",
        "",
        "Pega el bloque anterior en un chat nuevo cuando quieras ejecutar.",
    ]
    return "\n".join(lines)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
