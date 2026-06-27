SELECT
    'row_count' AS check_name,
    COUNT(*) AS check_value
FROM staging.stg_daily_weather;

SELECT
    'duplicate_location_date_rows' AS check_name,
    COUNT(*) AS failed_rows
FROM (
    SELECT
        location_id,
        weather_date,
        COUNT(*) AS row_count
    FROM staging.stg_daily_weather
    GROUP BY location_id, weather_date
    HAVING COUNT(*) > 1
) AS duplicates;

SELECT
    'null_key_rows' AS check_name,
    COUNT(*) AS failed_rows
FROM staging.stg_daily_weather
WHERE location_id IS NULL
   OR weather_date IS NULL
   OR city IS NULL
   OR country IS NULL;

SELECT
    'invalid_metric_ranges' AS check_name,
    COUNT(*) AS failed_rows
FROM staging.stg_daily_weather
WHERE temperature_avg_c < -90
   OR temperature_avg_c > 60
   OR temperature_max_c < -90
   OR temperature_max_c > 70
   OR temperature_min_c < -100
   OR temperature_min_c > 60
   OR relative_humidity_pct < 0
   OR relative_humidity_pct > 100
   OR wind_speed_m_s < 0
   OR precipitation_mm < 0
   OR solar_radiation_kwh_m2_day < 0;

SELECT
    'missing_metric_values' AS check_name,
    COUNT(*) AS failed_rows
FROM staging.stg_daily_weather
WHERE temperature_avg_c IS NULL
   OR temperature_max_c IS NULL
   OR temperature_min_c IS NULL
   OR relative_humidity_pct IS NULL
   OR wind_speed_m_s IS NULL
   OR precipitation_mm IS NULL
   OR solar_radiation_kwh_m2_day IS NULL;
