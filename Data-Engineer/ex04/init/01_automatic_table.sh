#!/bin/bash
set -e

CSV_DIR="/data"

if [ ! -d "$CSV_DIR" ]; then
    echo "[INIT] No data directory found at $CSV_DIR, skipping import."
    exit 0
fi

for CSV_FILE in "$CSV_DIR"/*.csv; do

    # skip if no csv files found (glob returns literal string)
    [ -f "$CSV_FILE" ] || continue

    # extract table name from filename without extension
    TABLE_NAME=$(basename "$CSV_FILE" .csv)

    echo "[INIT] Creating table '$TABLE_NAME' and importing $CSV_FILE..."

    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << SQL

CREATE TABLE IF NOT EXISTS $TABLE_NAME (
    product_id    INTEGER,
    category_id   BIGINT,
    category_code VARCHAR(255),
    brand         VARCHAR(255)
);

CREATE TEMP TABLE ${TABLE_NAME}_tmp (
    product_id    TEXT,
    category_id   TEXT,
    category_code TEXT,
    brand         TEXT
);

COPY ${TABLE_NAME}_tmp
FROM '$CSV_FILE'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

INSERT INTO $TABLE_NAME
SELECT
    TRIM(product_id)::INTEGER,
    TRIM(category_id)::BIGINT,
    NULLIF(TRIM(category_code), ''),
    NULLIF(TRIM(brand), '')
FROM ${TABLE_NAME}_tmp;

DROP TABLE ${TABLE_NAME}_tmp;

SQL

    echo "[INIT] '$TABLE_NAME' imported successfully."

done

echo "[INIT] All CSV files imported."