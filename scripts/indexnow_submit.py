#!/usr/bin/env python3
"""Submit URLs to the IndexNow API for osvaldovega.cl.

This script is meant for local validation and dry-run testing. It does not
perform any network request when --dry-run is used.
"""

from __future__ import annotations

import argparse
import json
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen

HOST = "osvaldovega.cl"
KEY = "b828fb822ffc45d8a20DEAEC7DAE54de"
KEY_LOCATION = "https://osvaldovega.cl/b828fb822ffc45d8a20DEAEC7DAE54de.txt"
INDEXNOW_URL = "https://api.indexnow.org/IndexNow"


def validate_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"URL inválida: {raw_url!r}. Debe empezar con http:// o https://")
    if parsed.netloc != HOST:
        raise ValueError(f"Host inválido: {parsed.netloc!r}. Solo se permiten URLs de {HOST}")
    return raw_url


def build_payload(urls: list[str]) -> dict:
    return {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }


def submit(urls: list[str], dry_run: bool = False) -> int:
    payload = build_payload(urls)
    data = json.dumps(payload).encode("utf-8")

    if dry_run:
        print("URLs enviadas:")
        for url in urls:
            print(f"- {url}")
        print("\nPayload completo:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("\nHTTP status: DRY-RUN (sin red)")
        return 0

    request = Request(
        INDEXNOW_URL,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "osvaldovega-cl-indexnow/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=20) as response:
            status = getattr(response, "status", response.getcode())
            message = response.read().decode("utf-8", errors="replace")
            print("URLs enviadas:")
            for url in urls:
                print(f"- {url}")
            print(f"\nHTTP status: {status}")
            print(f"Interpretación: {interpret_status(status)}")
            if message:
                print(f"Respuesta: {message}")
            return 0 if status == 200 else 1
    except Exception as exc:  # pragma: no cover - depends on network behavior
        status = getattr(exc, "code", None)
        if status is None:
            status = "ERROR"
        print("URLs enviadas:")
        for url in urls:
            print(f"- {url}")
        print(f"\nHTTP status: {status}")
        print(f"Interpretación: {interpret_status(status)}")
        print(f"Error: {exc}")
        return 1


def interpret_status(status):
    status_map = {
        200: "200 OK",
        400: "400 bad request",
        403: "403 key inválida/no encontrada",
        422: "422 URL/host inválido",
        429: "429 demasiadas solicitudes",
    }
    if status in status_map:
        return status_map[status]
    if status == "ERROR":
        return "error de red o de conexión"
    return f"estado HTTP {status}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enviar URLs a IndexNow para osvaldovega.cl")
    parser.add_argument("urls", nargs="+", help="URLs de osvaldovega.cl a enviar")
    parser.add_argument("--dry-run", action="store_true", help="Muestra el payload sin ejecutar la petición real")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        valid_urls = [validate_url(url) for url in args.urls]
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    return submit(valid_urls, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
