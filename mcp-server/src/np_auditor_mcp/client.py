"""Cliente NP Auditor — bridge local o API remota."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ESQUEMAS_API_PERMITIDOS = {"https"}


def _bridge_script() -> Path:
    root = os.environ.get("HOME_HUB_ROOT", "")
    if not root:
        raise RuntimeError("NP Auditor backend no configurado (HOME_HUB_ROOT)")
    script = Path(root) / "scripts" / "np-auditor-bridge.sh"
    if not script.is_file():
        raise RuntimeError("NP Auditor backend no disponible en esta instalación")
    return script


def _api_url() -> str:
    return os.environ.get("NP_AUDITOR_API_URL", "").strip().rstrip("/")


def _api_key() -> str:
    return os.environ.get("NP_AUDITOR_API_KEY", "").strip()


def _run_bridge(args: list[str], timeout: float = 120) -> dict:
    script = _bridge_script()
    env = os.environ.copy()
    proc = subprocess.run(
        ["bash", str(script), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        cwd=os.environ.get("HOME_HUB_ROOT", "."),
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(proc.stderr or "NP Auditor backend error") from None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError("Respuesta del backend inválida") from e


def _run_api(path: str, body: dict) -> dict:
    url = f"{_api_url()}{path}"
    esquema = urlparse(url).scheme
    if esquema not in ESQUEMAS_API_PERMITIDOS:
        raise RuntimeError(f"NP_AUDITOR_API_URL: esquema no permitido {esquema!r} (se requiere https)")
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    key = _api_key()
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(detail or f"API HTTP {e.code}") from e


def run_command(cmd: str, prompt: str = "", *, domain: str = "general", payload: dict | None = None) -> dict:
    """cmd: audit | coverage | risks | verify | suggest | select-model | auditcode"""
    if _api_url():
        routes = {
            "audit": ("/v1/audit", {"prompt": prompt}),
            "coverage": ("/v1/coverage", {"prompt": prompt}),
            "risks": ("/v1/risks", {"prompt": prompt, "domain": domain}),
            "suggest": ("/v1/suggest", {"prompt": prompt}),
            "verify": ("/v1/verify", payload or {}),
            "select-model": ("/v1/select-model", {"prompt": prompt}),
            "auditcode": ("/v1/auditcode", {"url": prompt}),
        }
        if cmd not in routes:
            raise RuntimeError(f"comando desconocido: {cmd}")
        path, body = routes[cmd]
        return _run_api(path, body)

    if cmd == "audit":
        return _run_bridge(["audit", prompt])
    if cmd == "coverage":
        return _run_bridge(["coverage", prompt])
    if cmd == "risks":
        os.environ["NP_AUDITOR_DOMAIN"] = domain
        return _run_bridge(["risks", prompt])
    if cmd == "suggest":
        return _run_bridge(["suggest", prompt])
    if cmd == "verify":
        return _run_bridge(["verify", json.dumps(payload or {}, ensure_ascii=False)])
    if cmd in ("select-model", "select_model"):
        return _run_bridge(["select-model", prompt])
    if cmd == "auditcode":
        return _run_bridge(["auditcode", prompt], timeout=240)
    raise RuntimeError(f"comando desconocido: {cmd}")
