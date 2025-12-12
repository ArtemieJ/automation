# lab02 – Currency Exchange Rate (Python client)

## Dependencies

You need **Python 3.9+** and **pip**.

Install the only required library:

```bash
pip install requests
```

(Optionally you can use a virtualenv.)

## Service setup (support project)

From the project root:

```bash
cp sample.env .env
# edit .env and set API_KEY if you changed it

docker-compose up --build
```

The API should be available at `http://localhost:8080`.

## How to run

From the project root:

```bash
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-01-01
```

If your service runs on another URL:

```bash
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-01-01 --base-url http://localhost:8080
```

If you don’t want to use `.env`, you can pass the key directly:

```bash
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-01-01 --api-key EXAMPLE_API_KEY
```

### Output files

On success, the script creates a **`data/`** directory in the project root (if missing) and saves the JSON response as:

```
data/rate_<FROM>_<TO>_<DATE>.json
```

Example:

```
data/rate_USD_EUR_2025-01-01.json
```

### Error handling

- Prints a clear error message to the console
- Writes detailed errors (with stack trace) to **`error.log`** in the project root

## Script structure

`lab02/currency_exchange_rate.py` contains:

- **CLI parsing** (`parse_args`) using `argparse`.
- **Validation** (`validate_and_build_config`):
  - currency codes are normalized to uppercase
  - date is validated in `YYYY-MM-DD`
  - date is checked to be within `2025-01-01 .. 2025-09-15`
  - API key must exist (from `.env`, environment, or `--api-key`)
- **API call** (`request_exchange_rate`):
  - `POST` request to `/` with query parameters: `from`, `to`, `date`
  - API key is sent in the POST body as `key`
  - handles non-200 HTTP responses and API `error` field
- **Saving JSON** (`ensure_data_dir`, `output_filename`, `save_json`) into `data/`.
- **Logging** (`setup_logging`) to `error.log`.

## Test runs (5 dates, equal interval)

Example (period `2025-01-01 .. 2025-09-15`, ~64-day interval):

```bash
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-01-01
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-03-06
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-05-09
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-07-12
python lab02/currency_exchange_rate.py --from USD --to EUR --date 2025-09-14
```
