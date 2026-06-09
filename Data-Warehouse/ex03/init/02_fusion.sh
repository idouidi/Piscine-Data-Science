#!/bin/bash
set -e

echo "[MERGE] Enriching customer with items (clean mode)..."

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<'SQL'

-- 1. AJOUT DES COLONNES (manquantes dans ta table)
ALTER TABLE customer
ADD COLUMN IF NOT EXISTS category_id BIGINT;

ALTER TABLE customer
ADD COLUMN IF NOT EXISTS category_code VARCHAR(255);

ALTER TABLE customer
ADD COLUMN IF NOT EXISTS brand VARCHAR(255);

-- 2. DEDUP ITEMS
WITH items_dedup AS (
    SELECT DISTINCT ON (product_id)
        product_id,
        category_id,
        category_code,
        brand
    FROM items
    ORDER BY product_id
)

-- 3. UPDATE
UPDATE customer c
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM items_dedup i
WHERE c.product_id = i.product_id;

ANALYZE customer;

SQL

echo "[MERGE] Done."