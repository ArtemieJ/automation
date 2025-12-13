#!/usr/bin/env python3
"""
currency_exchange_rate.py

Script care interacționează cu serviciul de curs valutar din lab02prep.
- Primește din linia de comandă: from_currency, to_currency, date (YYYY-MM-DD)
- Face request la API (http://localhost:8080)
- Salvează rezultatul în data/rate_FROM_TO_DATE.json
- În caz de eroare: afișează mesaj clar și salvează în error.log
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

# URL de bază pentru serviciu (poți suprascrie cu variabila de mediu CURRENCY_API_URL)
BASE_URL = os.getenv("CURRENCY_API_URL", "http://localhost:8080/")

# API key – trebuie să fie aceeași cu ce ai în .env din proiectul lab02prep
DEFAULT_API_KEY = os.getenv("API_KEY", "EXAMPLE_API_KEY")


def get_project_root() -> Path:
    """
    Returnează root-ul proiectului.
    Presupunem că scriptul este în <root>/lab02/currency_exchange_rate.py,
    deci root = părintele directorului curent.
    """
    return Path(__file__).resolve().parents[1]


def ensure_data_dir(root: Path) -> Path:
    """
    Creează directorul 'data' în root dacă nu există.
    """
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def log_error(root: Path, message: str) -> None:
    """
    Scrie un mesaj de eroare în fișierul error.log din root.
    Format: [YYYY-MM-DD HH:MM:SS] mesaj
    """
    log_path = root / "error.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def validate_date(date_str: str) -> None:
    """
    Verifică dacă data are formatul corect YYYY-MM-DD.
    Dacă nu, ridică ValueError.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must have format YYYY-MM-DD (e.g., 2025-03-01)")


def fetch_exchange_rate(from_currency: str, to_currency: str, date_str: str) -> dict:
    """
    Trimite request la API și întoarce obiectul 'data' din răspuns.
    Aruncă RuntimeError cu mesaj clar dacă apare vreo problemă.
    """
    params = {
        "from": from_currency,
        "to": to_currency,
        "date": date_str,
    }
    data = {
        "key": DEFAULT_API_KEY,
    }

    try:
        response = requests.post(BASE_URL, params=params, data=data, timeout=10)
    except requests.RequestException as e:
        raise RuntimeError(f"Request error: {e}")

    if response.status_code != 200:
        raise RuntimeError(f"HTTP error {response.status_code}: {response.text}")

    try:
        payload = response.json()
    except json.JSONDecodeError:
        raise RuntimeError("Invalid JSON received from API")

    # Structura răspunsului: {"error":"", "data":{...}}
    error_msg = payload.get("error")
    if error_msg:
        raise RuntimeError(f"API error: {error_msg}")

    if "data" not in payload:
        raise RuntimeError("API response does not contain 'data' field")

    return payload["data"]


def parse_args():
    """
    Parsează argumentele din linia de comandă.
    Exemplu:
        python lab02/currency_exchange_rate.py USD EUR 2025-03-01
    """
    parser = argparse.ArgumentParser(
        description="Get currency exchange rate from local API"
    )
    parser.add_argument(
        "from_currency",
        help="Currency to convert from (e.g. USD, EUR, MDL)",
    )
    parser.add_argument(
        "to_currency",
        help="Currency to convert to (e.g. USD, EUR, MDL)",
    )
    parser.add_argument(
        "date",
        help="Date in format YYYY-MM-DD (must be between 2025-01-01 and 2025-09-15)",
    )
    return parser.parse_args()


def main() -> None:
    root = get_project_root()
    args = parse_args()

    from_cur = args.from_currency.upper()
    to_cur = args.to_currency.upper()
    date_str = args.date

    try:
        # 1. Validăm data
        validate_date(date_str)

        # 2. Luăm cursul valutar de la API
        rate_data = fetch_exchange_rate(from_cur, to_cur, date_str)

    except Exception as e:
        # Orice eroare: afișăm în consolă + salvăm în error.log
        message = str(e)
        print(f"Error: {message}")
        log_error(root, message)
        sys.exit(1)

    # 3. Ne asigurăm că există directorul data/
    data_dir = ensure_data_dir(root)

    # 4. Construim numele fișierului: rate_FROM_TO_DATE.json
    filename = f"rate_{from_cur}_{to_cur}_{date_str}.json"
    output_path = data_dir / filename

    # 5. Salvăm datele în format JSON
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(rate_data, f, indent=2)

    # 6. Afișăm un mic rezumat în consolă
    print(
        f"Rate {rate_data['from']} -> {rate_data['to']} "
        f"on {rate_data['date']}: {rate_data['rate']}"
    )
    print(f"Saved to {output_path.relative_to(root)}")


if __name__ == "__main__":
    main()
