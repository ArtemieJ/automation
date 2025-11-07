#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <source_dir> [destination_dir=/backup]"
  echo "Example: $0 /var/www /backup"
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 2
fi

SOURCE_DIR="$1"
DEST_DIR="${2:-/backup}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Eroare: directorul sursă nu există: $SOURCE_DIR" >&2
  exit 3
fi

if [[ ! -d "$DEST_DIR" ]]; then
  echo "Eroare: directorul destinație nu există: $DEST_DIR" >&2
  echo "Creează-l sau specifică altul existent (ex: /home/user/backups)." >&2
  exit 4
fi

if [[ ! -w "$DEST_DIR" ]]; then
  echo "Eroare: nu am permisiune de scriere în: $DEST_DIR" >&2
  exit 5
fi

SRC_BASENAME="$(basename "$SOURCE_DIR")"
DATE_STR="$(date +%Y-%m-%d_%H-%M-%S)"
ARCHIVE_NAME="${SRC_BASENAME}_${DATE_STR}.tar.gz"
ARCHIVE_PATH="${DEST_DIR%/}/${ARCHIVE_NAME}"

PARENT_DIR="$(dirname "$SOURCE_DIR")"
ITEM_NAME="$(basename "$SOURCE_DIR")"

echo "Pornesc backup: '$SOURCE_DIR' -> '$ARCHIVE_PATH' ..."
tar -czf "$ARCHIVE_PATH" -C "$PARENT_DIR" "$ITEM_NAME"

if [[ -f "$ARCHIVE_PATH" ]]; then
  SIZE_BYTES=$(stat -c%s "$ARCHIVE_PATH" 2>/dev/null || stat -f%z "$ARCHIVE_PATH" 2>/dev/null || echo "?")
  echo "Backup finalizat: $ARCHIVE_PATH (mărime: ${SIZE_BYTES} bytes)"
  exit 0
else
  echo "Eroare: arhiva nu a fost creată: $ARCHIVE_PATH" >&2
  exit 6
fi
