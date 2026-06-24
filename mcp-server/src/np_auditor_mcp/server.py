"""NP Auditor MCP — stdio server (beta local)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("np-auditor")


def _bridge() -> Path:
    root = os.environ.get("HOME_HUB_ROOT", "")
    if not root:
        raise RuntimeError("HOME_HUB_ROOT no configurado")
    script = Path(root) / "scripts" / "np-auditor-bridge.sh"
    if not script.is_file():
        raise RuntimeError(f"Bridge no encontrado: {script}")
    return script


def _run_bridge(args: list[str]) -> dict:
    script = _bridge()
    env = os.environ.copy()
    proc = subprocess.run(
        ["bash", str(script), *args],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
        cwd=os.environ.get("HOME_HUB_ROOT", "."),
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(proc.stderr or f"bridge exit {proc.returncode}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON inválido del bridge: {proc.stdout[:200]}") from e


@mcp.tool()
def np_audit_input(prompt: str, context: str = "general") -> str:
    """Audita un prompt antes de enviarlo al agente.

    Devuelve score de estructura, sugerencias, cobertura y riesgo de loop.
    No usa tokens LLM (motor local).
    """
    data = _run_bridge(["audit", prompt])
    lines = [
        "── NP Auditor · input ──",
        f"Estructura: {data.get('estructura_score', 0):.0%}",
        f"Riesgo loop: {data.get('riesgo_loop', '?')}",
    ]
    for s in data.get("sugerencias") or []:
        lines.append(f"  → {s}")
    for c in (data.get("coverage") or [])[:4]:
        lk = c.get("lookup") or {}
        lines.append(f"  · {c.get('dominio')}/{c.get('topic')}: {lk.get('status', '?')}")
    return "\n".join(lines)


@mcp.tool()
def np_verify_response(response_text: str = "", claims_json: str = "") -> str:
    """Verifica claims en una respuesta del agente.

    Pasa response_text (el modelo parsea JSON de claims) o claims_json como array JSON.
    Devuelve tasa de alucinación sobre claims medibles.
    """
    payload: dict = {}
    if claims_json.strip():
        payload["claims"] = json.loads(claims_json)
    else:
        payload["response_text"] = response_text
    data = _run_bridge(["verify", json.dumps(payload, ensure_ascii=False)])
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
    """Lista riesgos visibles del agente (payment / prod / general).

    Checklist heurístico + cobertura organismo. Beta v0.1.
    """
    os.environ["NP_AUDITOR_DOMAIN"] = domain
    data = _run_bridge(["risks", prompt])
    lines = [
        f"── NP Auditor · riesgos ({data.get('domain', domain)}) ──",
        f"Estructura: {data.get('estructura_score', 0):.0%}",
        "",
        "Riesgos:",
    ]
    risks = data.get("risks") or []
    if not risks:
        lines.append("  · (ninguno crítico detectado en v0.1)")
    for r in risks:
        lines.append(f"  · {r}")
    return "\n".join(lines)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
