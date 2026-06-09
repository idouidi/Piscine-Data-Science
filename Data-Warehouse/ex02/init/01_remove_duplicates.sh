#!/bin/bash
set -e

    echo "[INIT] removing duplicates from 'customer' table..."

    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << SQL

WITH tmp AS (
    SELECT
        ctid,
        event_time,
        LAG(event_time) OVER (
            PARTITION BY event_type, product_id, price, user_id, user_session
            ORDER BY event_time
        ) AS prev_time
    FROM customer
)

DELETE FROM customer c
USING tmp
WHERE c.ctid = tmp.ctid
  AND tmp.prev_time IS NOT NULL
  AND tmp.event_time - tmp.prev_time <= INTERVAL '1 second';

SQL

    echo "[INIT] duplicates removed successfully."