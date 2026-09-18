#!/bin/sh
set -eu
: "${POSTGRES_DB:?POSTGRES_DB is required}"
: "${POSTGRES_USER:?POSTGRES_USER is required}"
BACKUP_DIR="${BACKUP_DIR:-/backups}"
STAMP=`date +%Y%m%d-%H%M%S`
mkdir -p "$BACKUP_DIR"
pg_dump -Fc -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_DIR/postgres-$STAMP.dump"
find "$BACKUP_DIR" -type f -name 'postgres-*.dump' -mtime +7 -delete
