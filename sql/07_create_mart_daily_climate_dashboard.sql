CREATE SCHEMA IF NOT EXISTS mart;

DROP TABLE IF EXISTS mart.mart_daily_climate_dashboard;

CREATE TABLE mart.mart_daily_climate_dashboard AS
SELECT
    f.location_id,
    d.city,
    d.country,
    d.latitude,
    d.longitude,
    f.weather_date,
    f.temperature_avg_c,
    f.temperature_max_c,
    f.temperature_min_c,
    ROUND(f.temperature_max_c - f.temperature_min_c, 2) AS temperature_range_c,
    f.relative_humidity_pct,
    f.wind_speed_m_s,
    f.precipitation_mm,
    f.solar_radiation_kwh_m2_day,
    CASE
        WHEN f.precipitation_mm > 0 THEN TRUE
        ELSE FALSE
    END AS is_rainy_day,
    CASE
        WHEN f.relative_humidity_pct >= 85 THEN TRUE
        ELSE FALSE
    END AS is_high_humidity_day,
    f.loaded_at
FROM fact.fact_daily_weather AS f
JOIN dim.dim_location AS d
    ON f.location_id = d.location_id;
