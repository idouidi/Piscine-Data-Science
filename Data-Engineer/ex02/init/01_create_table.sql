CREATE TABLE IF NOT EXISTS data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(50),
    product_id INTEGER,
    price NUMERIC(10,2),
    user_id BIGINT,
    user_session UUID
);