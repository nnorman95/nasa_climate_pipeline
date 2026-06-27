SELECT
    location_id,
    city,
    country,
    DATE_TRUNC('month', weather_date)::DATE AS month_start,
    COUNT(*) AS day_count,
    ROUND(AVG(temperature_avg_c), 2) AS avg_temperature_c,
    ROUND(AVG(temperature_max_c), 2) AS avg_max_temperature_c,
    ROUND(AVG(temperature_min_c), 2) AS avg_min_temperature_c,
    ROUND(AVG(relative_humidity_pct), 2) AS avg_relative_humidity_pct,
    ROUND(AVG(wind_speed_m_s), 2) AS avg_wind_speed_m_s,
    ROUND(SUM(precipitation_mm), 2) AS total_precipitation_mm,
    COUNT(*) FILTER (WHERE is_rainy_day IS TRUE) AS rainy_day_count,
    COUNT(*) FILTER (WHERE is_high_humidity_day IS TRUE) AS high_humidity_day_count,
    ROUND(AVG(solar_radiation_kwh_m2_day), 2) AS avg_solar_radiation_kwh_m2_day
FROM {{ ref('mart_daily_climate_dashboard') }}
GROUP BY
    location_id,
    city,
    country,
    DATE_TRUNC('month', weather_date)::DATE
