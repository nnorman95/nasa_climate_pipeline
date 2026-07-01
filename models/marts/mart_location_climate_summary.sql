SELECT
    location_id,
    city,
    country,
    MIN(weather_date) AS period_start,
    MAX(weather_date) AS period_end,
    COUNT(*) AS day_count,

    ROUND(AVG(temperature_avg_c), 2) AS avg_temperature_c,
    ROUND(MIN(temperature_min_c), 2) AS min_temperature_c,
    ROUND(MAX(temperature_max_c), 2) AS max_temperature_c,
    ROUND(AVG(temperature_range_c), 2) AS avg_temperature_range_c,

    ROUND(AVG(relative_humidity_pct), 2) AS avg_relative_humidity_pct,
    SUM(CASE WHEN is_high_humidity_day THEN 1 ELSE 0 END) AS high_humidity_day_count,

    ROUND(AVG(wind_speed_m_s), 2) AS avg_wind_speed_m_s,
    ROUND(SUM(precipitation_mm), 2) AS total_precipitation_mm,
    SUM(CASE WHEN is_rainy_day THEN 1 ELSE 0 END) AS rainy_day_count,

    ROUND(AVG(solar_radiation_kwh_m2_day), 2) AS avg_solar_radiation_kwh_m2_day
FROM {{ ref('mart_daily_climate_dashboard') }}
GROUP BY
    location_id,
    city,
    country
