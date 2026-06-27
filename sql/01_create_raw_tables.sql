CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.nasa_power_responses (
    id BIGSERIAL PRIMARY KEY,
    location_id TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    latitude NUMERIC(9, 4) NOT NULL,
    longitude NUMERIC(9, 4) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    response_json JSONB NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
