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
    event_time   TIMESTAMPTZ,
    event_type   VARCHAR(50),
    product_id   INTEGER,
    price        NUMERIC(10,2),
    user_id      BIGINT,
    user_session UUID
);

CREATE TEMP TABLE ${TABLE_NAME}_tmp (
    event_time   TEXT,
    event_type   TEXT,
    product_id   TEXT,
    price        TEXT,
    user_id      TEXT,
    user_session TEXT
);

COPY ${TABLE_NAME}_tmp
FROM '$CSV_FILE'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

INSERT INTO $TABLE_NAME
SELECT
    TRIM(event_time)::TIMESTAMPTZ,
    TRIM(event_type),
    TRIM(product_id)::INTEGER,
    TRIM(price)::NUMERIC(10,2),
    TRIM(user_id)::BIGINT,
    TRIM(user_session)::UUID
FROM ${TABLE_NAME}_tmp;

DROP TABLE ${TABLE_NAME}_tmp;

SQL

    echo "[INIT] '$TABLE_NAME' imported successfully."

done

echo "[INIT] All CSV files imported."