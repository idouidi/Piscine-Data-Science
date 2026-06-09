#!/bin/bash
set -e

CSV_DIR="/data/items"

if [ ! -d "$CSV_DIR" ]; then
    echo "[INIT] No data directory found at $CSV_DIR, skipping import."
    exit 0
fi

for CSV_FILE in "$CSV_DIR"/*.csv; do

    # skip if no csv files found 
    [ -f "$CSV_FILE" ] || continue


    echo "[INIT] Creating table items and importing $CSV_FILE..."

    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << SQL

CREATE TABLE IF NOT EXISTS items (
    product_id    INTEGER,
    category_id   BIGINT,
    category_code VARCHAR(255),
    brand         VARCHAR(255)
);

CREATE TEMP TABLE items_tmp (
    product_id    TEXT,
    category_id   TEXT,
    category_code TEXT,
    brand         TEXT
);

COPY items_tmp
FROM '$CSV_FILE'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

INSERT INTO items
SELECT
    TRIM(product_id)::INTEGER,
    TRIM(category_id)::BIGINT,
    NULLIF(TRIM(category_code), ''),
    NULLIF(TRIM(brand), '')
FROM items_tmp;

DROP TABLE items_tmp;

SQL

    echo "[INIT] items imported successfully."

done

echo "[INIT] All CSV files imported."