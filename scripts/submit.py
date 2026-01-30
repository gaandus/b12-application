#!/usr/bin/env python3
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

SIGNING_SECRET = "hello-there-from-b12"  # treat like a secret in practice
ENDPOINT = "https://b12.io/apply/submission"


def iso8601_utc_now() -> str:
    # ISO 8601 with milliseconds + Z, e.g. 2026-01-06T16:59:37.571Z
    dt = datetime.now(timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def build_canonical_json(payload: dict) -> bytes:
    # No extra whitespace, keys sorted, UTF-8 encoded
    s = json.dumps(payload, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
    return s.encode("utf-8")


def hmac_sha256_hex(key: str, message_bytes: bytes) -> str:
    digest = hmac.new(key.encode("utf-8"), message_bytes, hashlib.sha256).hexdigest()
    return digest


def http_post_json(url: str, body_bytes: bytes, signature_hex: str) -> bytes:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Signature-256": f"sha256={signature_hex}",
        "User-Agent": "b12-apply-ci/1.0",
    }
    req = urllib.request.Request(url=url, data=body_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        raise RuntimeError(f"HTTPError {e.code}: {e.reason}\n{err_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URLError: {e.reason}") from e


def main() -> int:
    name = os.environ.get("B12_NAME", "").strip()
    email = os.environ.get("B12_EMAIL", "").strip()
    resume_link = os.environ.get("B12_RESUME_LINK", "").strip()
    repository_link = os.environ.get("GITHUB_SERVER_URL", "").strip() and (
        f"{os.environ.get('GITHUB_SERVER_URL').rstrip('/')}/{os.environ.get('GITHUB_REPOSITORY', '').strip()}"
    )
    action_run_link = os.environ.get("GITHUB_SERVER_URL", "").strip() and (
        f"{os.environ.get('GITHUB_SERVER_URL').rstrip('/')}/{os.environ.get('GITHUB_REPOSITORY', '').strip()}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '').strip()}"
    )

    missing = [k for k, v in {
        "B12_NAME": name,
        "B12_EMAIL": email,
        "B12_RESUME_LINK": resume_link,
        "repository_link": repository_link,
        "action_run_link": action_run_link,
    }.items() if not v]

    if missing:
        print(f"Missing required values: {', '.join(missing)}", file=sys.stderr)
        return 2

    payload = {
        "timestamp": iso8601_utc_now(),
        "name": name,
        "email": email,
        "resume_link": resume_link,
        "repository_link": repository_link,
        "action_run_link": action_run_link,
    }

    body = build_canonical_json(payload)
    sig_hex = hmac_sha256_hex(SIGNING_SECRET, body)

    raw = http_post_json(ENDPOINT, body, sig_hex)

    # Expect JSON like: {"success": true, "receipt": "..."}
    try:
        resp = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print("Non-JSON response:", raw.decode("utf-8", errors="replace"), file=sys.stderr)
        raise

    if resp.get("success") is True and "receipt" in resp:
        print(resp["receipt"])
        return 0

    print("Unexpected response:", resp, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
