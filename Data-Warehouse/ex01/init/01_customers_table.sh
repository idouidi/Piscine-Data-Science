#!/bin/bash
set -e

CSV_DIR="/data/customer"

if [ ! -d "$CSV_DIR" ]; then
    echo "[INIT] No data directory found at $CSV_DIR, skipping import."
    exit 0
fi

echo "[INIT] Creating customers table if not exists..."

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<'SQL'

CREATE TABLE IF NOT EXISTS customers (
    event_time   TIMESTAMPTZ,
    event_type   VARCHAR(50),
    product_id   INTEGER,
    price        NUMERIC(10,2),
    user_id      BIGINT,
    user_session UUID
);

SQL

for CSV_FILE in "$CSV_DIR"/*.csv; do

    # Skip if no CSV files found
    [ -f "$CSV_FILE" ] || continue

    echo "[INIT] Importing $CSV_FILE into customers table..."

    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<SQL

CREATE TEMP TABLE customers_tmp (
    event_time   TEXT,
    event_type   TEXT,
    product_id   TEXT,
    price        TEXT,
    user_id      TEXT,
    user_session TEXT
);

COPY customers_tmp
FROM '$CSV_FILE'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ','
);

INSERT INTO customers (
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
)
SELECT
    NULLIF(TRIM(event_time), '')::TIMESTAMPTZ,
    NULLIF(TRIM(event_type), ''),
    NULLIF(TRIM(product_id), '')::INTEGER,
    NULLIF(TRIM(price), '')::NUMERIC(10,2),
    NULLIF(TRIM(user_id), '')::BIGINT,
    NULLIF(TRIM(user_session), '')::UUID
FROM customers_tmp;

DROP TABLE customers_tmp;

SQL

    echo "[INIT] $CSV_FILE imported successfully."

done

echo "[INIT] All CSV files imported into customers table."