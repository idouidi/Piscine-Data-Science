#!/bin/bash
set -e

CSV_FILE="/data/items/items.csv"

if [ ! -f "$CSV_FILE" ]; then
    echo "[INIT] No CSV file found at $CSV_FILE, skipping import."
    exit 0
fi

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