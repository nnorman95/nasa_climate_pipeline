SELECT
    location_id,
    weather_date,
    COUNT(*) AS row_count
FROM {{ ref('mart_daily_climate_dashboard') }}
GROUP BY
    location_id,
    weather_date
HAVING COUNT(*) > 1
