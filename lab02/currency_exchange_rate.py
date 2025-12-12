#!/usr/bin/env python3
"""lab02: Currency exchange rate client.

This script talks to the provided Currency Exchange Rate service (Docker).
It requests an exchange rate for a given date and saves the API response as JSON.

Usage example:
  python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-01-01

Environment:
  API_KEY       - required (or pass via --api-key)
  API_BASE_URL  - optional, default: http://localhost:8080

Output:
  ./data/rate_<FROM>_<TO>_<DATE>.json
Errors:
  prints a clear message to console + writes details to ./error.log
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

import requests


SERVICE_DEFAULT_BASE_URL = "http://localhost:8080"
REQUEST_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class Config:
    base_url: str
    api_key: str
    from_currency: str
    to_currency: str
    request_date: date


def project_root() -> Path:
    """Assumes the script lives in <root>/lab02/ and returns <root>."""
    return Path(__file__).resolve().parents[1]


def setup_logging(root: Path) -> logging.Logger:
    """Log errors to <root>/error.log. Keep console output user-friendly."""
    logger = logging.getLogger("currency_exchange_rate")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if script is imported / re-run in same process.
    if logger.handlers:
        return logger

    log_path = root / "error.log"
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    )
    logger.addHandler(file_handler)

    return logger


def load_dotenv_if_present(root: Path) -> None:
    """Minimal .env loader (no external deps).

    The support project suggests creating a .env file with API_KEY.
    We read it if present and fill missing environment variables.
    """
    env_path = root / ".env"
    if not env_path.exists():
        return

    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        # Silently ignore .env parsing issues; CLI/env vars will still work.
        return


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Get currency exchange rate for a specific date from the lab02 service."
    )
    parser.add_argument(
        "--from",
        dest="from_currency",
        required=True,
        help="Currency to convert from (e.g., USD)",
    )
    parser.add_argument(
        "--to",
        dest="to_currency",
        required=True,
        help="Currency to convert to (e.g., EUR)",
    )
    parser.add_argument(
        "--date",
        dest="request_date",
        required=True,
        help="Date in YYYY-MM-DD (valid in range 2025-01-01..2025-09-15)",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("API_BASE_URL", SERVICE_DEFAULT_BASE_URL),
        help=f"Service base URL (default: {SERVICE_DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("API_KEY", ""),
        help="API key for the service (default: env API_KEY)",
    )
    return parser.parse_args(argv)


def validate_and_build_config(args: argparse.Namespace) -> Config:
    from_currency = args.from_currency.strip().upper()
    to_currency = args.to_currency.strip().upper()

    try:
        req_date = date.fromisoformat(args.request_date.strip())
    except ValueError as e:
        raise ValueError(
            "Invalid --date. Use format YYYY-MM-DD, e.g. 2025-01-01"
        ) from e

    # Lab constraint (data availability in the service)
    if req_date < date(2025, 1, 1) or req_date > date(2025, 9, 15):
        raise ValueError(
            "Date out of allowed period. Use a date from 2025-01-01 to 2025-09-15."
        )

    base_url = args.base_url.rstrip("/")
    api_key = (args.api_key or "").strip()
    if not api_key:
        raise ValueError(
            "Missing API key. Set API_KEY in environment/.env or pass --api-key."
        )

    return Config(
        base_url=base_url,
        api_key=api_key,
        from_currency=from_currency,
        to_currency=to_currency,
        request_date=req_date,
    )


def request_exchange_rate(cfg: Config) -> Dict[str, Any]:
    url = f"{cfg.base_url}/"

    params = {
        "from": cfg.from_currency,
        "to": cfg.to_currency,
        "date": cfg.request_date.isoformat(),
    }
    data = {"key": cfg.api_key}

    resp = requests.post(url, params=params, data=data, timeout=REQUEST_TIMEOUT_SECONDS)

    # HTTP-level error
    if resp.status_code != 200:
        raise RuntimeError(
            f"HTTP {resp.status_code} from service. Body: {resp.text[:500]}"
        )

    try:
        payload = resp.json()
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Service returned non-JSON response: {resp.text[:500]}") from e

    # API-level error
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError(f"API error: {payload.get('error')}")

    return payload


def ensure_data_dir(root: Path) -> Path:
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def output_filename(cfg: Config) -> str:
    return f"rate_{cfg.from_currency}_{cfg.to_currency}_{cfg.request_date.isoformat()}.json"


def save_json(data: Dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv: Optional[list[str]] = None) -> int:
    root = project_root()

    # Allow .env in project root (as described in the support project's README)
    load_dotenv_if_present(root)

    logger = setup_logging(root)

    try:
        args = parse_args(argv)
        cfg = validate_and_build_config(args)

        payload = request_exchange_rate(cfg)

        data_dir = ensure_data_dir(root)
        out_path = data_dir / output_filename(cfg)
        save_json(payload, out_path)

        # Friendly console output
        rate_info = payload.get("data") if isinstance(payload, dict) else None
        if isinstance(rate_info, dict) and "rate" in rate_info:
            print(
                f"OK: {cfg.from_currency}->{cfg.to_currency} on {cfg.request_date.isoformat()} = {rate_info['rate']}\n"
                f"Saved: {out_path}"
            )
        else:
            print(f"OK: saved response to {out_path}")

        return 0

    except requests.RequestException as e:
        msg = (
            "Network/request error while calling the API. "
            "Is the service running on the given --base-url?"
        )
        print(f"ERROR: {msg}")
        logger.exception("%s Details: %s", msg, e)
        return 2

    except Exception as e:
        print(f"ERROR: {e}")
        logger.exception("Unhandled error: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
