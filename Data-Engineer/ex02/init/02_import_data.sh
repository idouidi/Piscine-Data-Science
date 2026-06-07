#!/bin/bash
set -e

CSV_FILE="/data/data.csv"              # ← pointe vers le nouveau chemin

if [ ! -f "$CSV_FILE" ]; then
    echo "[INIT] No CSV file found at $CSV_FILE, skipping import."
    exit 0
fi

echo "[INIT] Importing $CSV_FILE into data_2022_oct..."

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << SQL
CREATE TEMP TABLE data_2022_oct_tmp (
    event_time   TEXT,
    event_type   TEXT,
    product_id   TEXT,
    price        TEXT,
    user_id      TEXT,
    user_session TEXT
);

COPY data_2022_oct_tmp
FROM '$CSV_FILE'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

INSERT INTO data_2022_oct
SELECT
    TRIM(event_time)::TIMESTAMPTZ,
    TRIM(event_type),
    TRIM(product_id)::INTEGER,
    TRIM(price)::NUMERIC(10,2),
    TRIM(user_id)::BIGINT,
    TRIM(user_session)::UUID
FROM data_2022_oct_tmp;

DROP TABLE data_2022_oct_tmp;
SQL

echo "[INIT] Import complete."