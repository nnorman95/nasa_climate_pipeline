SELECT
    'daily_mart_row_count' AS check_name,
    COUNT(*) AS check_value
FROM mart.mart_daily_climate_dashboard;

SELECT
    'summary_mart_row_count' AS check_name,
    COUNT(*) AS check_value
FROM mart.mart_location_climate_summary;

SELECT
    'daily_mart_null_key_rows' AS check_name,
    COUNT(*) AS failed_rows
FROM mart.mart_daily_climate_dashboard
WHERE location_id IS NULL
   OR city IS NULL
   OR country IS NULL
   OR weather_date IS NULL;

SELECT
    'summary_invalid_day_count' AS check_name,
    COUNT(*) AS failed_rows
FROM mart.mart_location_climate_summary
WHERE day_count <= 0;

SELECT
    'summary_rainy_days_over_day_count' AS check_name,
    COUNT(*) AS failed_rows
FROM mart.mart_location_climate_summary
WHERE rainy_day_count > day_count;

SELECT
    'monthly_mart_row_count' AS check_name,
    COUNT(*) AS check_value
FROM mart.mart_monthly_climate_summary;

SELECT
    'monthly_mart_invalid_day_count' AS check_name,
    COUNT(*) AS failed_rows
FROM mart.mart_monthly_climate_summary
WHERE day_count <= 0;

SELECT
    'monthly_mart_missing_avg_temperature' AS check_name,
    COUNT(*) AS warning_rows
FROM mart.mart_monthly_climate_summary
WHERE avg_temperature_c IS NULL;
