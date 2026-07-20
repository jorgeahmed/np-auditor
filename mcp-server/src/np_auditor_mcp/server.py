"""NP Auditor MCP — stdio server (beta local o API remota)."""

from __future__ import annotations

import json
import os

from mcp.server.fastmcp import FastMCP

from np_auditor_mcp.client import run_command

mcp = FastMCP("np-auditor")

# Tiers acumulativos del plan freemium (ver README / paquetes):
#   free     → SAST (banco de firmas completo)
#   pro      → + calidad de código + alucinaciones de IA
#   team     → + SCA (dependencias vs. OSV.dev)
#   business → + IaC (Terraform/Kubernetes)
_NIVEL_TIER = {"free": 0, "pro": 1, "team": 2, "business": 3, "enterprise": 3, "full": 3}
_UPSELL = "→ disponible en un tier superior: github.com/jorgeahmed/np-auditor#paquetes"


def _tier_actual() -> int:
    """Nivel de acceso: NP_AUDITOR_TIER explícito, o full si hay API key B2B."""
    tier = os.environ.get("NP_AUDITOR_TIER", "").strip().lower()
    if tier:
        return _NIVEL_TIER.get(tier, 0)
    if os.environ.get("NP_AUDITOR_API_KEY", "").strip():
        return _NIVEL_TIER["full"]
    return _NIVEL_TIER["free"]


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
    y totales del banco (1000+ dims). Sin LLM.
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
def np_select_model(prompt: str, prefer_nvidia: bool = False) -> str:
    """Elige el modelo OpenClaw óptimo para un prompt (Ollama local o NVIDIA NIM).

    Sin LLM — reglas sobre estructura del prompt (~instantáneo).
    Frontier NVIDIA: deepseek-v4-flash/pro, kimi-k2.6, glm-5.1, nemotron-3-super.
    DeepSeek R1 NO está en NVIDIA NIM; solo local (deepseek-r1:14b).
    """
    if prefer_nvidia:
        os.environ["NP_ROUTER_PREFER_NVIDIA"] = "1"
    data = run_command("select-model", prompt)
    return data.get("formatted") or json.dumps(data, ensure_ascii=False)


@mcp.tool()
def np_audit_code(repo_url_o_ruta_local: str) -> str:
    """Audita código: vulnerabilidades (SAST), secretos hardcodeados,
    dependencias vulnerables (SCA vs. OSV.dev), infraestructura como código
    (Terraform/Kubernetes), calidad (complejidad, código muerto,
    duplicación) y alucinaciones de IA (nombres/imports usados pero nunca
    definidos -- señal de que un LLM inventó una referencia inexistente).

    Acepta una URL https:// de un repo externo (lo clona a un directorio
    temporal, escanea y borra el clon) o una ruta local ya existente en
    disco (la escanea directo). Nunca ejecuta el código auditado. Puede
    tardar hasta unos minutos en repos grandes (consulta en vivo a OSV.dev).
    """
    data = run_command("auditcode", repo_url_o_ruta_local)
    if data.get("error"):
        return f"Error: {data['error']}"

    nivel = _tier_actual()
    lines = [
        f"── NP Auditor · código — {data.get('repo_url', repo_url_o_ruta_local)} ──",
        f"Archivos: {data.get('total_archivos_py', 0)} Python · "
        f"{data.get('total_archivos_php', 0)} PHP · {data.get('total_archivos_js', 0)} JS/TS",
    ]

    dimensiones = data.get("dimensiones") or []
    lines.append("")
    if not dimensiones:
        lines.append("Código: sin coincidencias con el banco de firmas SAST.")
    else:
        lines.append("Vulnerabilidades de código:")
        for d in dimensiones:
            lines.append(f"  [{d.get('cwe')}] {d.get('nombre')}: {d.get('conteo')} ocurrencia(s)")

    total_paquetes = data.get("total_paquetes_analizados", 0)
    dependencias = data.get("dependencias") or []
    sca_disponible = data.get("sca_disponible", True)
    lines.append("")
    if nivel < _NIVEL_TIER["team"]:
        lines.append(f"SCA (dependencias vs. OSV.dev): {_UPSELL}")
    elif total_paquetes == 0:
        lines.append("SCA: sin lockfile para analizar (package-lock.json/requirements.txt/composer.lock)")
    elif not sca_disponible:
        lines.append("SCA: no se pudo consultar OSV.dev (sin red/timeout)")
    elif not dependencias:
        lines.append(f"SCA: {total_paquetes} paquete(s) analizados, sin vulnerabilidades conocidas")
    else:
        lines.append(f"SCA: {len(dependencias)} vulnerabilidad(es) en {total_paquetes} paquete(s) analizados")
        for dep in dependencias[:6]:
            cve = f" ({dep.get('cve')})" if dep.get("cve") else ""
            lines.append(f"  · {dep.get('paquete')}@{dep.get('version')}{cve}: {dep.get('severidad') or '?'}")

    iac = data.get("iac") or []
    lines.append("")
    if nivel < _NIVEL_TIER["business"]:
        lines.append(f"IaC (Terraform/Kubernetes): {_UPSELL}")
    elif not iac:
        lines.append("IaC: sin misconfiguraciones (o sin Terraform/Kubernetes en el repo)")
    else:
        lines.append(f"IaC: {len(iac)} misconfiguracion(es)")
        for h in iac[:6]:
            lines.append(f"  · [{h.get('severidad')}] {h.get('regla')} ({h.get('referencia_cis')}): {h.get('archivo')}:{h.get('linea')}")

    calidad = data.get("calidad") or []
    lines.append("")
    if nivel < _NIVEL_TIER["pro"]:
        lines.append(f"Calidad de código: {_UPSELL}")
    elif not calidad:
        lines.append("Calidad: sin archivos Python para analizar")
    else:
        bloat_avg = sum(c.get("bloat_score", 0) for c in calidad) / len(calidad)
        criticos = sorted(
            (c for c in calidad if c.get("bloat_score", 0) >= 0.5),
            key=lambda c: c.get("bloat_score", 0), reverse=True,
        )
        lines.append(f"Calidad: {len(calidad)} archivo(s) · bloat promedio {bloat_avg:.2f} · {len(criticos)} candidato(s) a refactor")
        for c in criticos[:5]:
            lines.append(f"  · {c.get('archivo')}: bloat {c.get('bloat_score')}, complejidad máx {c.get('complejidad_max')}, doc {c.get('documentacion_cobertura_pct')}%")

    alucinaciones = data.get("alucinaciones") or []
    lines.append("")
    if nivel < _NIVEL_TIER["pro"]:
        lines.append(f"Alucinaciones de IA: {_UPSELL}")
    elif not alucinaciones:
        lines.append("Alucinaciones de IA: sin nombres indefinidos detectados")
    else:
        lines.append(f"Alucinaciones de IA: {len(alucinaciones)} nombre(s)/import(s) indefinidos")
        for a in alucinaciones[:6]:
            lines.append(f"  · {a.get('archivo')}:{a.get('linea')} — `{a.get('nombre')}` ({a.get('tipo')})")

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
