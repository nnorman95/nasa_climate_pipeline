CREATE SCHEMA IF NOT EXISTS dim;

DROP TABLE IF EXISTS dim.dim_location;

CREATE TABLE dim.dim_location AS
SELECT DISTINCT
    location_id,
    city,
    country,
    latitude,
    longitude
FROM staging.stg_daily_weather;
